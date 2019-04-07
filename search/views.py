from django.shortcuts import render
from search.models import Word, Website, WordWebsite

def index(request):
    search = request.GET.get('search', '')
    webs = WordWebsite.objects.select_related('word', 'website').filter(word__word=search).order_by('-count')
    return render(request, 'index.html', {'webs': webs})
