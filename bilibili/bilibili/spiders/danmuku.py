# -*- coding: utf-8 -*-
import scrapy


class DanmukuSpider(scrapy.Spider):
    name = 'danmuku'
    allowed_domains = ['bilibili.com']
    url1 = 'http://comment.bilibili.com/151140295.xml'
    url2 = 'https://api.bilibili.com/x/v1/dm/list.so?oid=151140295'  # oid 即 cid

    # <d p="349.79800,1,25,16777215,1579355158,0,1a84edf3,27374640770318340">？？？？？？</d>
    # TODO: 其中 1579355158 是时间戳， 1a84edf3 疑似用户id
    def parse(self, response):
        pass
