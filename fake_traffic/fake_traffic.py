import asyncio
import logging

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

logger = logging.getLogger("__name__")


class FakeTraffic:
    def __init__(
        self,
        country="US",
        language="en-US",
        category="h",
        headless=True,
        tabs=3,
    ):
        """Internet traffic generator. Utilizes real-time google search trends by specified parameters.
        country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
        language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
        category = category of interest of a user (defaults to 'h'):
                'all' (all), 'b' (business), 'e' (entertainment),
                'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories);
        headless = True/False (defaults to True);
        tabs = limit the number of tabs in browser (defaults to 3).
        """
        self.country = country
        self.language = language
        self.category = category
        self.headless = headless
        self.browser = None
        self.semaphore = asyncio.Semaphore(tabs)

    async def abrowse(self, url):
        async with self.semaphore:
            page = await self.browser.new_page()
            await stealth_async(page)
            try:
                resp = await page.goto(url, wait_until="load")
                logger.info(f"{resp.status} {resp.url}")
            except Exception as ex:
                logger.warning(
                    f"{type(ex).__name__}: {ex} {url if url not in str(ex) else ''}"
                )
            await page.close()

    async def acrawl(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                args=["--disable-blink-features=AutomationControlled"],
                headless=self.headless,
            )
            context = await browser.new_context(
                locale=self.language,
                viewport={"width": 1920, "height": 1080},
            )
            self.browser = context

            page = await self.browser.new_page()
            await stealth_async(page)

            # google trends
            try:
                await page.goto(
                    f"https://trends.google.com/trends/trendingsearches/realtime?geo={self.country}&hl={self.language}&category={self.category}",
                    wait_until="networkidle",
                )
                elements = await page.query_selector_all("//div[@class='title']")
                keywords = [
                    x for e in elements for x in (await e.inner_text()).split(" • ")
                ]
                logger.info(f"google_trends() GOT {len(keywords)} keywords")
            except Exception as ex:
                keywords = []
                logger.warning(f"google_trends() {type(ex).__name__}: {ex}")

            # google search
            for keyword in keywords:
                try:
                    await page.goto("https://www.google.com", wait_until="load")
                    await page.fill('textarea[name="q"]', keyword)
                    await page.press('textarea[name="q"]', "Enter")
                    for _ in range(30):
                        # Check for a popup window and close it
                        if len(self.browser.pages) > 1:
                            await self.browser.pages[1].close()
                        # Scroll to the bottom of the page
                        await page.mouse.wheel(0, 1000)
                        await asyncio.sleep(0.25)
                        elements = await page.query_selector_all(
                            "//div[starts-with(@class, 'g ')]//span/a[@href]"
                        )
                        if len(elements) > 100:
                            break
                    result_urls = [
                        await link.get_attribute("href") for link in elements
                    ]
                    logger.info(
                        f"google_search() {keyword=} GOT {len(result_urls)} results"
                    )
                except Exception as ex:
                    result_urls = []
                    logger.warning(f"google_search() {type(ex).__name__}: {ex}")

                # browse urls in parallel
                tasks = [asyncio.create_task(self.abrowse(url)) for url in result_urls]
                await asyncio.gather(*tasks)

    def crawl(self):
        asyncio.run(self.acrawl())


if __name__ == "__main__":
    fake_traffic = FakeTraffic(
        country="US",
        language="en-US",
        category="h",
        headless=True,
        tabs=3,
    )
    fake_traffic.crawl()
