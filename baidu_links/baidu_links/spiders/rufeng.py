# -*- coding: utf-8 -*-
import scrapy


class RufengSpider(scrapy.Spider):
    name = 'rufeng'
    allowed_domains = ['rufeng.net']
    start_urls = ['http://www.rufengso.net/r/2452894']

    def parse(self, response):
        pass
