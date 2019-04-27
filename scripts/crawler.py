from search.models import Website
import requests
import tldextract
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter
from scripts import add_word


def crawl(url, domain, depth=0):
    ''' Webpage Crawling '''

    # End of crawling
    if depth == -1:
        return ("Finish crawling!")

    # Crawling start
    print("Crawling at: ", url)
    data = requests.get(url)

    # HTML status checking
    if data.status_code != 200:
        return ("HTML status is not 200")

    # Skip existing URL
    if Website.objects.filter(url=url):
        return ("There is an existing url")

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
            pass
            # add to ref table


file = open("scripts/url_list.txt", "r")
for line in file:
    url = line.replace("\n", "")
    tld = tldextract.extract(url)
    domain = tld.domain + "." + tld.suffix
    crawl(url, domain)
