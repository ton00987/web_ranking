from search.models import Word, Website, WordWebsite
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://www.bbc.com/news"
hostname = urlparse(url).hostname
database = []

def crawl(url, depth=3):
    ''' Webpage Crawling '''
    if depth == -1:
        return

    print("Crawling at: ", url)
    data = requests.get(url)

    # Check HTML status
    if data.status_code != 200:
        return

    html = BeautifulSoup(data.content, 'html.parser')
    get_text(html)

    a_tag = html.find_all('a')
    for a in a_tag:
        new_url = urljoin(url, a.get('href'))
        if new_url in database:
            continue
        elif not new_url.startswith("http"):
            continue
        elif hostname in new_url:
            database.append(new_url)
            crawl(new_url, depth - 1)


def get_text(html):
    ''' Remove CSS and Javascript tag and get text from HTML. '''
    for script in html(["script", "style"]):
        script.decompose()
    text = html.get_text(" ", strip=True).split()
    print(text)

crawl(url)