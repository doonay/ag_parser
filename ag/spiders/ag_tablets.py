import scrapy
import json
from configparser import ConfigParser

settings = ConfigParser()
settings.read('settings.ini')
key = settings.get('DEFAULT', 'key')


class AgTabletsSpider(scrapy.Spider):
    name = 'ag_tablets'
    allowed_domains = ['ag.ru']
    # Это стартовая страница, откуда стартует обход всех остальных
    start_urls = ['https://ag.ru/api/games/lists/main?discover=true&ordering=-relevance&page=1&key=' + key]
    custom_settings = {'FEED_URI': "ag_%(time)s.json", 'FEED_FORMAT': 'json'}

    def parse(self, response):
        print("procesing:" + response.url)
        data = json.loads(response.body)
        for item in data.get('results', []):
            yield {
                # 'text': item.get('text'),
                # 'author': item.get('author', {}).get('name'),
                # 'tags': item.get('tags'),
                'esrb_rating': item.get('esrb_rating'),
            }
        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(self.results_base_url % next_page)
        return data
