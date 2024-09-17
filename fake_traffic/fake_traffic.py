import asyncio
import logging

from playwright.async_api import async_playwright

logger = logging.getLogger("__name__")


class FakeTraffic:
    def __init__(
        self,
        country="US",
        language="en-US",
        keywords=None,
        headless=True,
        tabs=3,
    ):
        """Internet traffic generator. Utilizes real-time google search trends by specified parameters.
        country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
        language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
        keywords = comma separated queries for Google searches, if not specified, Google trending is used,
        headless = True/False (defaults to True);
        tabs = limit the number of tabs in browser (defaults to 3).
        """
        self.country = country
        self.language = language
        self.keywords = [k.strip() for k in keywords.split(",")] if keywords else []
        self.headless = headless
        self.browser = None
        self.semaphore = asyncio.Semaphore(tabs)

    async def abrowse(self, url):
        async with self.semaphore:
            page = await self.browser.new_page()
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

            if not self.keywords:
                # google trends
                try:
                    await page.goto(
                        f"https://trends.google.com/trends/trendingsearches/realtime?geo={self.country}&hl={self.language}&status=active",
                        wait_until="load",
                    )
                    elements = await page.query_selector_all("//tbody//tr/td[2]/div[1]")
                    self.keywords = [await e.inner_text() for e in elements]
                    logger.info(f"google_trends() GOT {len(self.keywords)} keywords")
                except Exception as ex:
                    logger.exception(f"google_trends() {type(ex).__name__}: {ex}")

            # google search
            for keyword in self.keywords:
                search_urls = []
                try:
                    await page.goto("https://www.google.com", wait_until="load")
                    await page.fill('textarea[name="q"]', keyword)
                    await page.press('textarea[name="q"]', "Enter")
                    # pagination
                    for _ in range(3):
                        await page.wait_for_load_state("domcontentloaded")
                        # parse urls
                        elements = await page.locator(
                            "xpath=//div[starts-with(@class, 'g ')]//span/a[@href] | //a[.//div[@role='heading']]"
                        ).all()
                        page_urls = [await e.get_attribute("href") for e in elements]
                        page_urls = [
                            x for x in page_urls if "https://www.youtube.com" not in x
                        ]
                        search_urls.extend(page_urls)
                        # click the "Next" button
                        await page.locator("xpath=//td[@role='heading']").last.click()
                    logger.info(
                        f"google_search() {keyword=} GOT {len(search_urls)} results"
                    )
                except Exception as ex:
                    logger.warning(f"google_search() {type(ex).__name__}: {ex}")

                # browse urls in parallel
                tasks = [asyncio.create_task(self.abrowse(url)) for url in search_urls]
                await asyncio.gather(*tasks)

    def crawl(self):
        asyncio.run(self.acrawl())


if __name__ == "__main__":
    fake_traffic = FakeTraffic(
        country="US",
        language="en-US",
        keywords=None,
        headless=True,
        tabs=3,
    )
    fake_traffic.crawl()
