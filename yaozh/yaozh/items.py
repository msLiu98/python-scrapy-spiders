# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class YaozhItem(scrapy.Item):
    name = scrapy.Field()
    purl = scrapy.Field()
    text = scrapy.Field(
        input_processor=MapCompose(lambda i: i.replace('\t', '').replace(' ', '').replace('\n', '\t')),
        output_processor=MapCompose(str.strip)
    )
    grade = scrapy.Field()
    type = scrapy.Field()
    prvc = scrapy.Field()
    city = scrapy.Field()
    cnty = scrapy.Field()
    bdnm = scrapy.Field()
    adr = scrapy.Field()
    pid = scrapy.Field()
    tid = scrapy.Field()
    
    
class YaozhTaskItem(scrapy.Item):
    task = scrapy.Field()
    tid = scrapy.Field()
    dtnum = scrapy.Field()
