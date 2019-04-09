from django.shortcuts import render, redirect
from search.models import Word, Website, WordWebsite

def index(request):
    search = request.GET.get('search', '')
    join_table = WordWebsite.objects.select_related('word', 'website')
    find_word = join_table.filter(word__word=search)
    sort_webs = find_word.order_by('-website__click', '-count')
    return render(request, 'index.html', {'sort_webs': sort_webs})

def click(request):
    url = request.POST.get('url')
    web = Website.objects.filter(url=url)
    web.update(click=web[0].click + 1)
    return redirect(url)
