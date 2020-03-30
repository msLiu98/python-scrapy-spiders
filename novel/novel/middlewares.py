# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import requests
import time


class ProxySelfDownloaderMiddleware(object):
    
    def process_request(self, request, spider):
        count = int(requests.get('http://127.0.0.1:5000/count').text)
        if count > 0:
            proxy = requests.get('http://127.0.0.1:5000/get').text
            request.meta['proxy'] = 'http://{proxy}'.format(proxy=proxy)
            spider.logger.info(proxy)
        else:
            spider.logger.error('No proxy for this request!')
            time.sleep(5)
            return request


class UserAgentDownloaderMiddleware(object):
    def __init__(self, crawler):
        super(UserAgentDownloaderMiddleware, self).__init__()
        self.ua = UserAgent()
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)
