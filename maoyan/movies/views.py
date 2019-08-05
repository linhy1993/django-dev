from django.http import HttpResponse
from django.shortcuts import render, redirect
from movies.spider import MovieSpider
from movies.models import MaoyanMovie
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage


# Create your views here.

def index(request):
    movies_lst = MaoyanMovie.objects.all()
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
