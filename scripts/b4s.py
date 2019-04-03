from search.models import Word, Website, WordWebsite

def run():
    w = Word.objects.all()
    print(w)
