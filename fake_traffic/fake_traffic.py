import warnings
from random import uniform, choice, randint, sample, shuffle
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from time import sleep
from itertools import islice, zip_longest

import requests
from lxml import html
from duckduckgo_search import DDGS
from google_searching import ggl
from google_trends import daily_trends, realtime_trends

from .version import __version__


THREADS = 2
MIN_WAIT = 1
MAX_WAIT = 60
DEBUG = False

BLACKLIST = (
    "bit.ly",
    "clickserve",
    "https://t.co",
    "itunes.apple.com",
    "javascript:",
    "l.facebook.com",
    "legal.twitter.com",
    "login",
    "Login",
    "mail.",
    "mailto:",
    "mediawiki",
    "messenger.com",
    "policies",
    "s.click",
    "showcaptcha?",
    "signup",
    "smart-captcha/",
    "Special:",
    "support.",
    "t.umblr.com",
    "tel:",
    "tg://",
    "whatsapp://",
    "zendesk",
    "_click_",
    "/auth/",
    "/authorize?",
    "/captcha",
    "/chat",
    "/click",
    "/feed?",
    "/join?",
    "/joinchat",
    "/help",
    "/privacy",
    "/registration",
    "/share",
    "/showcaptcha",
    "/stat/",
    "/support",
    "/terms",
    "/tos",
    "/tweet",
    ".cs",
    ".css",
    ".gif",
    ".iso",
    ".jpg",
    ".jpeg",
    ".ico",
    ".js",
    ".json",
    ".png",
    ".svg",
    ".xml",
)
USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
]
URLS_CACHE = set()


def grouper(iterable, n):
    """Collect data into non-overlapping fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3) --> ABC DEF GNoneNone
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=None)


def debug_print(*agrs, **kwargs):
    if DEBUG:
        print(*agrs, **kwargs)


def get_yesterday():
    yesterday = datetime.now() - timedelta(1)
    return datetime.strftime(yesterday, "%Y%m%d")


def real_trends(country="US", language="en-US", category="h"):
    while True:
        try:
            try:
                trends = realtime_trends(
                    country=country,
                    language=language,
                    category=category,
                    num_results=20,
                )
                return trends
            except Exception:
                print("Google realtime trends error. Trying daily trends.")
                trends = daily_trends(
                    country=country, language=language
                ) + daily_trends(get_yesterday(), country=country, language=language)
                return trends
        except Exception:
            print("Google trends error. Sleep 25-35 sec")
            sleep(uniform(25, 35))


def url_in_blacklist(url):
    if any(x in url for x in BLACKLIST):
        debug_print(f"{url}, STATUS: in BLACKLIST")
        return True


def url_fix(url):
    url = url.strip(".")
    if "https://" not in url and "http://" not in url:
        url = f"https://{url}"
    try:
        url = url[: url.rindex("#")]
    except Exception:
        pass
    return url


def get_url(url):
    url = url_fix(url)
    if url not in URLS_CACHE and not url_in_blacklist(url):
        debug_print(f"{url}, STATUS: request")
        try:
            resp = requests.get(
                url, headers={"User-Agent": choice(USERAGENTS)}, timeout=4
            )
            URLS_CACHE.add(url)
            if resp.status_code == 200:
                debug_print(f"{resp.url}, STATUS: {resp.status_code}")
                if url_in_blacklist(resp.url):
                    return None
                return resp
            debug_print(resp.raise_for_status())
        except requests.ConnectionError:
            debug_print(f"{url}, STATUS: Connection error. Sleep 25-35 sec")
            sleep(uniform(25, 35))
        except Exception:
            debug_print(f"{url}, STATUS: ERROR")


def google_search(word, max_results=20):
    query = word.replace(" ", "+")
    search_ggl = ggl(query, max_results=max_results)
    search_ggl = search_ggl[:max_results]
    urls = [
        x["href"].replace("https://", "").replace("http://", "") for x in search_ggl
    ]
    return urls


def ddg_search(word, max_results=20):
    query = word.replace(" ", "+")
    search_ddg = list(islice(DDGS().text(query), max_results))
    urls = [
        x["href"].replace("https://", "").replace("http://", "") for x in search_ddg
    ]
    return urls


def parse_urls(response):
    try:
        tree = html.fromstring(response.text)
        tree.make_links_absolute(response.url)
        urls = tree.xpath("//a/@href")
        urls = [url for url in urls if not any(x in url for x in BLACKLIST)]
        return urls
    except Exception:
        return []


def recursive_browse(url, depth=randint(0, 5)):
    if not depth:
        get_url(url)
        return
    resp = get_url(url)
    if resp:
        recursive_urls = parse_urls(resp)
        if recursive_urls:
            url = choice(recursive_urls)
            sleep(uniform(MIN_WAIT, MAX_WAIT))
            recursive_browse(url, depth - 1)


def _thread(trend):
    if isinstance(trend, dict):
        word = " ".join(sample(trend["entity_names"], 2))
        article_urls = trend["article_urls"]
    else:
        word = trend
        article_urls = []
    print(f"*** Trend = {word} ***")

    google_urls, ddg_urls = [], []
    try:
        google_urls = google_search(word)
        print(f"'{word}': google_urls len = {len(google_urls)}")
        article_urls.extend(url for url in google_urls if url not in article_urls)
    except Exception:
        print("google search error")
    try:
        ddg_urls = ddg_search(word)
        print(f"'{word}': ddg_urls len = {len(ddg_urls)}")
        article_urls.extend(url for url in ddg_urls if url not in article_urls)
    except Exception:
        print("ddg search error")

    print(f"Recursive browsing {len(article_urls)} urls. Wait...", end="\n\n")
    for i, url in enumerate(article_urls, start=1):
        debug_print(f"{i}/{len(article_urls)} recursive browse")
        if i <= 10:
            min_depth, max_depth = 15, 25
        else:
            min_depth, max_depth = 0, 5
        recursive_browse(url, depth=randint(min_depth, max_depth))


def fake_traffic(
    country="US",
    language="en-US",
    category="h",
    threads=THREADS,
    min_wait=MIN_WAIT,
    max_wait=MAX_WAIT,
    debug=DEBUG,
):
    """Imitating an Internet user by mimicking popular web traffic (internet traffic generator).
    country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
    language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
    category = сategory of interest of a user (defaults to 'h'):
               'all' (all), 'b' (business), 'e' (entertainment),
               'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories);
    threads = number of threads (defaults to 1),
    min_wait = minimal delay between requests (defaults to 1),
    max_wait = maximum delay between requests (defaults to 30),
    debug = if True, then print the details of the requests (defaults to False).
    """

    global THREADS, MIN_WAIT, MAX_WAIT, DEBUG
    THREADS = threads
    MIN_WAIT = min_wait
    MAX_WAIT = max_wait
    DEBUG = debug

    print(f"*** Fake traffic {__version__} ***")
    if category not in ("all", "b", "e", "m", "s", "t", "h"):
        warnings.warn(
            """Wrong category, specify the correct category:\n'all' (all), 'b' (business), 'e' (entertainment),\n'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories);"""
        )
        return
    while True:
        print(f"\n{datetime.now()}")
        print(f"---GET TRENDS IN {country=} {language=} {category=}---")
        trends = real_trends(country=country, language=language, category=category)
        # trends = sample(trends, threads)
        shuffle(trends)
        for temp_trends in grouper(trends, threads):
            with ThreadPoolExecutor(threads) as executor:
                for i, trend in enumerate(temp_trends, start=1):
                    if trend:
                        print(f"Thread {i} start.")
                        executor.submit(_thread, trend)
                        sleep(uniform(25, 35))
        URLS_CACHE.clear()


if __name__ == "__main__":
    fake_traffic(country="US", language="en-US")
