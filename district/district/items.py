# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProvItem(scrapy.Item):
    prov_name = scrapy.Field()
    prov_url = scrapy.Field()
    # prov_code = scrapy.Field()


class CityItem(scrapy.Item):
    city_name = scrapy.Field()
    city_code = scrapy.Field()
    city_url = scrapy.Field()


class CntyItem(scrapy.Item):
    cnty_name = scrapy.Field()
    cnty_code = scrapy.Field()
    cnty_url = scrapy.Field()


class TownItem(scrapy.Item):
    town_name = scrapy.Field()
    town_code = scrapy.Field()
    town_url = scrapy.Field()


class VlgeItem(scrapy.Item):
    vlge_name = scrapy.Field()
    vlge_code = scrapy.Field()
    vlge_ctgr = scrapy.Field()
