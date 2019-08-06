from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from movies.models import MaoyanMovie
from movies.spider import MovieSpider


# Create your views here.

def index(request):
    movies_lst = MaoyanMovie.objects.all().order_by('id')
    if movies_lst:
        paginator = Paginator(movies_lst, 10)
        if request.method == 'GET':
            page = request.GET.get('page')
            movies = paginator.get_page(page)
            return render(request, 'index.html', {'movies': movies, 'paginator': paginator, 'is_paginated': True})
    return render(request, 'index.html')


def spider(request):
    if request.method == 'POST':
        spd = MovieSpider()
        spd.run_spider()
        return redirect('index')


def show_pages(request, movies_lst):
    if movies_lst:
        paginator = Paginator(movies_lst, 10)
        if request.method == 'GET':
            page = request.GET.get('page')
            movies = paginator.get_page(page)
            return movies, paginator


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        condition = request.GET.get('condition')
        # search in database
        if condition == 'movie_name':
            movies_lst = MaoyanMovie.objects.all().filter(name=query)
            return render(request, 'search.html', {'movies': movies_lst})
        elif condition == 'release_year':
            movies_lst = MaoyanMovie.objects.all().filter(release_time__year__gt=query).order_by('release_time')
            movies, paginator = show_pages(request, movies_lst)
            return render(request, 'search.html', {'movies': movies, 'paginator': paginator, 'is_paginated': True})
        elif condition == 'stars':
            movies_lst = MaoyanMovie.objects.all().filter(stars__contains=query)
            movies, paginator = show_pages(request, movies_lst)
            return render(request, 'search.html', {'movies': movies, 'paginator': paginator, 'is_paginated': True})
        elif condition == 'score':
            movies_lst = MaoyanMovie.objects.all().filter(score__gt=query).order_by('-score')
            movies, paginator = show_pages(request, movies_lst)
            return render(request, 'search.html', {'movies': movies, 'paginator': paginator, 'is_paginated': True})
    return render(request, 'search.html')
