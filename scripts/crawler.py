from search.models import Website
from django.db import transaction
import requests
import tldextract
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter
from scripts import add_word
import datetime

@transaction.atomic
def crawl(url, domain, depth=0):
    ''' Webpage Crawling '''

    # End of crawling
    if depth == -1:
        return

    # Skip existing URL that haven't crawl for a long time
    web = Website.objects.filter(url=url)
    if web and (datetime.date.today() - web[0].date) <  datetime.timedelta(7, 0, 0):
        return

    # Crawling start
    print("Crawling at: ", url)
    data = requests.get(url, allow_redirects=False, verify=False)

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

        # Skip AJAX
        if "#" in href:
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
