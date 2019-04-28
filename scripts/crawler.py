from search.models import Website
from django.db import transaction
import requests
import tldextract
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter
from scripts import add_word
import datetime


def recently_crawled_url(url):
    ''' Existing url that recently crawl. '''
    web = Website.objects.filter(url=url)
    return web and (datetime.date.today() - web[0].date)\
        < datetime.timedelta(7, 0, 0)


def special_char(href):
    ''' Ignored special characters'''
    chars = ["#", "mailto:"]
    for char in chars:
        if href.startswith(char):
            return True
    return False


def extension(href):
    ''' Ignored some extensions if not in list. '''
    extensions = [".html", ".com", ".org", ".net", ".int", ".edu", ".gov"]
    if re.search("\.[^.\/]+$", href):
        for extension in extensions:
            if href.endswith(extension):
                return False
        return True
    return False


@transaction.atomic
def crawl(url, domain, depth=0):
    ''' Webpage Crawling '''

    # End of crawling
    if depth == -1:
        return

    # Skip existing URL that recently crawl
    if recently_crawled_url(url):
        return

    # Crawling start
    print("Crawling at: ", url)
    try:
        data = requests.get(url)
    except:
        return

    # HTML status checking
    if data.status_code != 200:
        return

    # Get HTML
    html = BeautifulSoup(data.content, "html.parser")
    add_word.insert_db(html, url)

    # Continue crawling on next url
    a_tag = html.find_all("a", href=True)
    for a in a_tag:
        href = a.get("href")

        # Skip URL with special characters or some extensions
        if special_char(href) or extension(href):
            continue

        next_url = urljoin(url, href)

        # Skip URL without HTTP
        if not next_url.startswith("http"):
            continue

        # Crawling at next URL if same domain
        # Else, use as reference URL
        if domain in next_url:
            crawl(next_url, domain, depth - 1)
        else:
            add_word.add_ref(url, next_url)


start = datetime.datetime.now()
file = open("scripts/url_list.txt", "r")
for line in file:
    url = line.replace("\n", "")
    tld = tldextract.extract(url)
    domain = tld.domain + "." + tld.suffix
    crawl(url, domain, 1)
stop = datetime.datetime.now()
timedelta = stop - start
print("Finish! in ", timedelta)
