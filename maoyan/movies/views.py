from django.shortcuts import render
from movies.spider import MovieSpider


# Create your views here.

def index(request):
    return render(request, 'movies/index.html')


def spider(request):
    spd = MovieSpider()
    spd.run_spider()
    return render(request, 'movies/spider.html')
