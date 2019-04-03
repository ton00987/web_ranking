from search.models import Word, Website, WordWebsite
import requests
from bs4 import BeautifulSoup

url = "https://rottenpotatoesvxx.herokuapp.com/"
data = requests.get(url)
soup = BeautifulSoup(data.content, 'html.parser')
for script in soup(["script", "style"]):
    script.decompose()    # rip it out

# get text
text = soup.get_text(" ", strip=True).split()

print(text)
# x = soup.find_all('a')


# for i in x:
  # Website(url=i.get('href')).save()
