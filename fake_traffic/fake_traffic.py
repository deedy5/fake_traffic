import logging
import subprocess
from collections import deque
from random import choice, randint, shuffle, uniform
from time import sleep
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


# playwright install chromium
res = subprocess.run(
    "playwright install chromium",
    shell=True,
    check=True,
    capture_output=True,
    text=True,
)
logging.info(res.stdout)

BLACKLIST = (
    ".cs",
    ".css",
    ".gif",
    ".ico",
    ".iso",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".png",
    ".svg",
    ".xml",
    "/auth/",
    "/authorize?",
    "/captcha",
    "/chat",
    "/click",
    "/feed?",
    "/help",
    "/join?",
    "/joinchat",
    "/privacy",
    "/registration",
    "/share",
    "/showcaptcha",
    "/stat/",
    "/support",
    "/terms",
    "/tos",
    "/tweet",
    "Login",
    "Special:",
    "_click_",
    "bit.ly",
    "clickserve",
    "https://t.co",
    "itunes.apple.com",
    "javascript:",
    "l.facebook.com",
    "legal.twitter.com",
    "login",
    "mail.",
    "mailto:",
    "mediawiki",
    "messenger.com",
    "policies",
    "s.click",
    "showcaptcha?",
    "signup",
    "smart-captcha/",
    "support.",
    "t.umblr.com",
    "tel:",
    "tg://",
    "whatsapp://",
    "zendesk",
)


class FakeTraffic:
    def __init__(
        self,
        country="US",
        language="en-US",
        category="h",
        min_wait=1,
        max_wait=10,
        headless=True,
    ):
        """ Imitating an Internet user by mimicking popular web traffic (internet traffic generator).    
        country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
        language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
        category = сategory of interest of a user (defaults to 'h'):
                'all' (all), 'b' (business), 'e' (entertainment), 
                'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories);
        min_wait = minimal delay between requests (defaults to 1),
        max_wait = maximum delay between requests (defaults to 10),
        headless = True/False (defaults to True).
        """
        self.country = country
        self.language = language
        self.category = category
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.headless = headless
        self.urls_queue = deque()
        self.trends = set()
        self.page = self.initialize_browser()

    def close(self):
        self.page.close()
        self.page.context.close()
        self.page.browser.close()

    @staticmethod
    def url_in_blacklist(url):
        if any(x in url for x in BLACKLIST):
            logging.info(f"{url}, STATUS: in BLACKLIST")
            return True

    @staticmethod
    def url_fix(url):
        if "https://" not in url and "http://" not in url:
            url = f"https://{url}"
        url = url.split("#")[0].split("?")[0]
        return url

    def initialize_browser(self):
        """Initialize browser"""
        try:
            p = sync_playwright().__enter__()
            browser = p.chromium.launch(headless=self.headless, slow_mo=100)
            context = browser.new_context(
                locale=self.language,
                viewport={"width": 1920, "height": 1080},
            )
            page = context.new_page()
            stealth_sync(page)
            return page
        except Exception as ex:
            logging.warning(f"{type(ex).__name__}: {ex}")

    def get_url(self, url):
        url = self.url_fix(url)
        if not self.url_in_blacklist(url):
            try:
                resp = self.page.goto(url)
                self.page.wait_for_load_state("networkidle")
                logging.info(f"{resp.url} {resp.status}")
                return self.page
            except Exception as ex:
                logging.warning(f"{url} {type(ex).__name__}: {ex}")

    def google_search(self, query):
        self.page.goto("https://www.google.com")
        self.page.fill('textarea[name="q"]', query)
        self.page.press('textarea[name="q"]', "Enter")
        self.page.wait_for_load_state("networkidle")
        result_urls = self.page.query_selector_all(
            "//div[starts-with(@class, 'g ')]//span/a[@href]"
        )
        result_urls = [link.get_attribute("href") for link in result_urls]
        logging.info(
            f"google_search() {query=} GOT {len(result_urls)} results"
        )
        return result_urls

    def google_trends(self):
        url = f"https://trends.google.com/trends/trendingsearches/realtime?geo={self.country}&hl={self.language}&category={self.category}"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        elements = self.page.query_selector_all("//div[@class='title']")
        trends = [x for e in elements for x in e.inner_text().split(" • ")]
        logging.info(f"google_trends() GOT {len(trends)} trends")
        return trends

    def parse_urls(self, page, base_url):
        try:
            elements = page.query_selector_all("a")
            urls = [
                urljoin(base_url, x) for e in elements if (x := e.get_attribute("href"))
            ]
            return urls
        except Exception as ex:
            logging.warning(f"parse_urls() {type(ex).__name__}: {ex}")
            return []

    def recursive_browse(self, url, depth):
        if depth:
            resp = self.get_url(url)
            if resp:
                urls = self.parse_urls(resp, resp.url)
                if urls:
                    url = choice(urls)
                    sleep(uniform(self.min_wait, self.max_wait))
                    self.recursive_browse(url, depth - 1)

    def crawl(self):
        while True:
            if not self.urls_queue:
                if not self.trends:
                    self.trends = self.google_trends()
                shuffle(self.trends)
                trend = self.trends.pop()
                search_results = self.google_search(trend)
                self.urls_queue = deque(search_results)

            url = self.urls_queue.popleft()
            depth = randint(3, 10)
            self.recursive_browse(url, depth)


if __name__ == "__main__":
    fake_traffic = FakeTraffic(
        country="US",
        language="en-US",
        category="h",
        min_wait=1,
        max_wait=10,
        headless=True,
    )
    fake_traffic.crawl()
