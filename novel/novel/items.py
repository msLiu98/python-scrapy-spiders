# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Join

class ChpItem(scrapy.Item):
    chp_title = scrapy.Field()
    chp_url = scrapy.Field()


class CtnItem(scrapy.Item):
    file_name = scrapy.Field()
    chp_ctg = scrapy.Field()
    chp_url = scrapy.Field()
    chp_title = scrapy.Field()
    chp_ctn = scrapy.Field()


class LiuliItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    entry_time = scrapy.Field()
    image_urls  = scrapy.Field()
    image_paths = scrapy.Field()
    images = scrapy.Field()
    mag = scrapy.Field()
    cat = scrapy.Field()


class LiuliImagesItem(scrapy.Item):
    image_urls  = scrapy.Field()
    image_paths = scrapy.Field()
    images = scrapy.Field()


class NineItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    watch = scrapy.Field()
    like = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    images = scrapy.Field()
