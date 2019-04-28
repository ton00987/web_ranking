from search.models import *
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from scripts import crawler
from datetime import date


def remove_script(html):
    ''' Remove CSS and Javascript tag. '''
    for script in html(["script", "style"]):
        script.decompose()
    return html


def get_title(html):
    ''' Get title from HTML. '''
    title = html.title.string
    return title


def get_words(html):
    ''' Get words from HTML. '''
    words = html.get_text(" ", strip=True)
    words = re.sub('[^a-z]+', ' ', words.lower())
    words = words.split()
    return words


def add_website(title, url):
    ''' Add or update website to database. '''
    web_obj, created = Website.objects.update_or_create(
        url=url,
        defaults={'title':title, 'date':date.today()}
    )
    show(created, url, ' url')
    return web_obj


def add_word(word):
    ''' Add or get word to database. '''
    word_obj, created = Word.objects.get_or_create(word=word)
    show(created, word, ' word')
    return word_obj


def add_have(word, website, count):
    ''' Add many to many relationship
    between word and website to database. '''
    created = Have.objects.get_or_create(
        word=word, website=website,
        defaults={'count':count}
    )[1]
    obj_name = word.word + ' and ' + website.url
    show(created, obj_name, ' relationship')


def add_ref(from_web, to_web):
    ''' Add many to many relationship
    between website and referenced website to database. '''
    from_web_obj = add_website(None, from_web)
    to_web_obj = add_website(None, to_web)
    from_web_obj.ref.add(to_web_obj)


def insert_db(html, url):
    html = remove_script(html)
    title = get_title(html)
    words = get_words(html)

    web_obj = add_website(title, url)

    # Count each word
    counts = Counter(words)

    for word, num in counts.items():
        word_obj = add_word(word)
        add_have(word_obj, web_obj, num)


def show(status, obj_name, type_obj):
    if status:
        print('Add ' + obj_name + type_obj)
    else:
        print('There is an existing ' + obj_name + type_obj)
