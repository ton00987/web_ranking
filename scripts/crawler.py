from search.models import Word, Website, WordWebsite
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import Counter
from scripts import add_word


def crawl(url, root, depth=0):
    ''' Webpage Crawling '''
    if depth == -1:
        return

    print("Crawling at: ", url)
    data = requests.get(url)

    # Check HTML status
    if data.status_code != 200:
        return

    html = BeautifulSoup(data.content, 'html.parser')
    get_text(html, url, root)

    a_tag = html.find_all('a')
    for a in a_tag:
        new_url = urljoin(url, a.get('href'))
        if Website.objects.filter(url=new_url):
            continue
        elif '#' in new_url:
            continue
        elif not new_url.startswith("http"):
            continue
        if root in new_url:
            crawl(new_url, root, depth - 1)

def get_text(html, url, root):
    ''' Remove CSS and Javascript tag and get text from HTML. '''
    for script in html(["script", "style"]):
        script.decompose()

    text = html.get_text(" ", strip=True)
    text = re.sub('[^a-z]+', ' ', text.lower())
    text = text.split()
    add_word.insert_db(html, url, text, root)


file = open('scripts/url_list.txt', 'r')
for line in file:
    url = line.replace('\n', '')
    root = urljoin(url, '/')
    crawl(url, root)