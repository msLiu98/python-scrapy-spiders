# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import base64
from fake_useragent import UserAgent

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H170982QQ66N284D"
proxyPass = "863971B94B36191E"

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class DistrictDownloaderMiddleware(object):
    def __init__(self, crawler):
        super(DistrictDownloaderMiddleware, self).__init__()
        self.ua = UserAgent()
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)

