# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(ItemLoader):
    text_out = Compose(Join(),lambda s:s.strip())
    source_out = Compose(Join(),lambda s:s.strip())

class ChinaSpider(CrawlSpider):
    name = 'china'
    # allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(.,"下一页")]'))
    )

    # def parse_item(self, response):
    #     item = NewsItem()
    #     item['title'] = response.xpath('//h1[@id="chan_newsTitle"]/text()').extract_first()
    #     item['url'] = response.url
    #     item['text'] = ''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip()
    #     item['datetime'] = response.xpath('//div[@id="chan_newsInfo"]/text()').re_first('(\d+-\d+-\d+-\d+\s\d+:\d+:\d+)')
    #     item['source'] = response.xpath('//div[@id="chan_newsInfo"]/text()').re_fist('来源:(.*)').strip()
    #     item['website'] = '中华网'
    #     yield item
    def parse_item(self, response):
        loader = ChinaLoader(item=NewsItem(),response=response)
        loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url',response.url)
        loader.add_xpath('text','//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()',re='(\d+-\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_xpath('source', '//div[@id="chan_newsInfo"]/text()',re='来源:(.*)')
        loader.add_value('website','中华网')
        yield loader.load_item()



