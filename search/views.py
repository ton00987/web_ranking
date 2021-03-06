from django.shortcuts import render, redirect
from django.db.models import F, Count
from search.models import Word, Website, Have

def index(request):
    ''' Search by word order by reference, click and count '''
    search = request.GET.get('search', '')
    join_table = Have.objects.select_related('word', 'website')
    find_word = join_table.filter(word__word=search)
    sort_webs = find_word.annotate(weight=Count('website__website')*20 \
        + F('website__click')*4 + F('count')).order_by('-weight')
    return render(request, 'index.html', {'sort_webs': sort_webs})

def click(request):
    url = request.POST.get('url')
    web = Website.objects.filter(url=url)
    web.update(click=web[0].click + 1)
    return redirect(url)
