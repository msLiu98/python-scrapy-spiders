# -*- coding: utf-8 -*-
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from universal_example.utils import get_config
from universal_example.rules import rules
from universal_example import urls
from ..items import NewsItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(ItemLoader):
    text_out = Compose(Join(),lambda s:s.strip())
    source_out = Compose(Join(),lambda s:s.strip())

class UniversalSpider(CrawlSpider):
    name = 'universal'
    def __init__(self,name,*args,**kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        # self.start_urls = config.get('start_urls')
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args',[])))
        self.allow_domains = config.get('allowed_domains')
        super(UniversalSpider,self).__init__(*args,**kwargs)

    def parse_item(self,response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls,response=response)
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key,*extractor.get('args'),**{'re':extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('value') == 'xpath':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
            yield loader.load_item()

