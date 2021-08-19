from random import uniform, choice, randint, sample
from datetime import datetime
from time import sleep

import requests
from lxml import html
from duckduckgo_search import ddg
from google_searching import ggl
from google_trends import realtime_trends

__version__ = 0.6

def real_trends(country='US', language='en-US'):
    trends = realtime_trends(country=country, language=language, category='h', num_results=20)
    return trends

def get_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
    url = f"https://{url}" if ('https://' not in url) else url
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            print(resp.status_code, url)
            return resp
    except requests.exceptions.ConnectionError:
        print("Connection error. Sleep 30-60 sec.")
        sleep(uniform(30, 60))
    except:
        return None

def google_search(word, max_results=20):
    query  = word.replace(' ','+')
    search_ggl = ggl(query, max_results=max_results)
    urls = [x['href'].lstrip('https://') for x in search_ggl]
    return urls

def ddg_search(word, max_results=20):
    query  = word.replace(' ','+')
    search_ddg = ddg(query, max_results=max_results)
    urls = [x['href'].lstrip('https://') for x in search_ddg]
    return urls

def parse_urls(response):
    blacklist = ["https://t.co", "t.umblr.com", "messenger.com",
                 "itunes.apple.com", "l.facebook.com", "bit.ly",
                 "mediawiki", ".css", ".ico", ".xml", "intent/tweet",
                 "twitter.com/share", "signup", "login", "dialog/feed?",
                 ".json", ".svg", ".gif", "zendesk", "clickserve",
                 "mailto:", "smart-captcha/", "Login", "mail.google.com",
                 ".jpg", ".jpeg", ".png", ".iso",]
    try:
        tree = html.fromstring(response.text)
        tree.make_links_absolute(response.url)
        urls = tree.xpath('//a/@href')
        urls = [url for url in urls if not any(x in url for x in blacklist)]
        return urls
    except:
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
            sleep(uniform(1, 30))
            recursive_browse(url, depth-1)
    
def fake_traffic(country='US', language='en-US'):
    print('*** Fake traffic ***')
    while True:
        print(f'\n{datetime.now()}')
        print(f'------GET TRENDS IN {country=}------')
        trends = real_trends(country=country, language=language)
        trend = choice(trends)
        word = ' '.join(sample(trend['entity_names'], 2))
        article_urls = trend['article_urls']
        print(f"*** Trend = {word} ***")
        google_urls, ddg_urls = [], []
        try:
            google_urls = google_search(word)
            print(f"'{word}': google_urls len = {len(google_urls)}")
            article_urls.extend(url for url in google_urls if url not in article_urls)
        except:
            print('google search error')
        try:
            ddg_urls = ddg_search(word)
            print(f"'{word}': ddg_urls len = {len(ddg_urls)}")
            article_urls.extend(url for url in ddg_urls if url not in article_urls)
        except:
            print('ddg search error')
        print(f"Recursive browsing {len(article_urls)} urls. Wait...")
        for i, url in enumerate(article_urls, start=1):            
            print(f"{i}/{len(article_urls)} urls recursive browsing...")
            recursive_browse(url)
        sleep(uniform(1, 10))

if __name__ == '__main__':
    fake_traffic(country='US', language='en-US')
