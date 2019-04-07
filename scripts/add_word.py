from search.models import Word, Website, WordWebsite
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

class NameDuplicate(Exception):
  def __init__(self, name):
    self.name = name

url = "https://www.wikipedia.org/"
data = requests.get(url)
soup = BeautifulSoup(data.content, 'html.parser')

# Delete javascript tag and css tag
for script in soup(["script", "style"]):
  script.decompose()

# Get text and clean it
text = soup.get_text(" ", strip=True)
text = re.sub('[^a-z]+', ' ', text.lower())
text = text.split()

# Add website
try:
  if Website.objects.filter(url__exact=url):
    web = Website.objects.filter(url__exact=url)[0]
    raise NameDuplicate(url)

  else:
    web = Website(title=soup.title.string, url=url)
    web.save()

except NameDuplicate as n:
  print('NameDuplicate: There is an existing ' + n.name + ' url')

# Count each words
counts = Counter(text)

# Add word and number word
for i, j in counts.items():
  try:
    if Word.objects.filter(word__exact=i):
      wd = Word.objects.filter(word__exact=i)[0]
      raise NameDuplicate(i)

    else:
      wd = Word(word=i)
      wd.save()

  except NameDuplicate as n:
    print('NameDuplicate: There is an existing ' + n.name + ' word')

  try:
    if WordWebsite.objects.filter(word_id=wd.id, website_id=web.id):
      raise NameDuplicate('')

    else:
      ww = WordWebsite(word=wd, website=web, count=j)
      ww.save()

  except NameDuplicate as n:
    print('NameDuplicate: There is an existing ' + n.name + 'object')

print('Success')