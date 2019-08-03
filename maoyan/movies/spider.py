import re

import requests
from bs4 import BeautifulSoup
from movies.models import MaoyanMovie
from dateutil import parser


class MovieSpider(object):
    def __init__(self, truncate=True):
        self.results = []
        self.url = 'https://maoyan.com/board/4?offset='
        if truncate:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE `movies_maoyanmovie`")

    @staticmethod
    def clean_string(input_str):
        string = re.sub('\s+', ' ', input_str)
        output_str = string.strip()
        return output_str

    @staticmethod
    def parse_ymd(input_str):
        return parser.isoparse(input_str)

    def get_html(self):
        for i in range(0, 100, 10):
            if i == 100:
                i -= 1
            try:
                response = requests.get(url=self.url + f'{i}')
                print(self.url + f'{i}')
                if response.status_code == 200:
                    yield response.text
            except Exception:
                return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        movies_info = soup.find_all(name='div', attrs={"class": "board-item-content"})
        for movie in movies_info:
            name = movie.find(name='p', attrs={'name'}).get_text()
            stars = movie.find(name='p', attrs={'star'}).get_text()[3:]
            time = movie.find(name='p', attrs={'releasetime'}).get_text()[5:]
            release_time = re.sub(u"\\(.*?\\)", "", time)
            score = movie.find(name='p', attrs={'score'}).get_text()

            yield {
                'name': self.clean_string(name),
                'stars': self.clean_string(stars),
                'release_time': self.parse_ymd(release_time),
                'score': score
            }

    def run_spider(self):
        for html in self.get_html():
            for movie_info in self.parse_html(html):
                item = MaoyanMovie()
                item.name = movie_info['name']
                item.stars = movie_info['stars']
                item.release_time = movie_info['release_time']
                item.score = movie_info['score']
                item.save()
