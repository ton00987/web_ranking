from search.models import Word, Website, WordWebsite
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from scripts import crawler

class NameDuplicate(Exception):
    def __init__(self, name):
        self.name = name

def insert_db(html, url, text, old_url):
    # Add website
    try:
        if Website.objects.filter(url__exact=url):
            web = Website.objects.filter(url__exact=url)[0]
            raise NameDuplicate(url)

        else:
            try:
                old_web = Website.objects.filter(url=old_url)[0]
            except:
                old_web = None

            if html.title.string != None:
                web = Website(title=html.title.string, url=url, root=old_web)
                web.save()
            else:
                return

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
                print('Add', i)

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
