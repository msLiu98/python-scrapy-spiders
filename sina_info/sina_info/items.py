# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BasicInfoItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    birth = scrapy.Field()
    academy_degree = scrapy.Field()
    nationality = scrapy.Field()
    brief_resume = scrapy.Field()


class ResumeInfoItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    position = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    salary = scrapy.Field()