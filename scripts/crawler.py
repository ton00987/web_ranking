from search.models import Word, Website, WordWebsite
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://rottenpotatoesvxx.herokuapp.com/"
base = urljoin(url, '/')
database = []

def crawl(url):
    ''' Webpage Crawling '''
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
        elif base in new_url:
            database.append(new_url)
            crawl(new_url)


def get_text(html):
    ''' Remove CSS and Javascript tag and get text from HTML. '''
    for script in html(["script", "style"]):
        script.decompose()
    text = html.get_text(" ", strip=True).split()
    print(text)

crawl(url)