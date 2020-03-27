# -*- coding: utf-8 -*-
import scrapy
from ..items import *
from scrapy.loader import ItemLoader
from urllib.parse import urljoin
from scrapy.loader.processors import MapCompose, TakeFirst
import os
import pandas as pd


class Adcode2Spider(scrapy.Spider):
    name = 'adcode2'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "_trs_uv=jz69duas_6_b2nk; AD_RS_COOKIE=20082856",
        "Host": "www.stats.gov.cn",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    }
    api2011 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2011/'  # 2011年数据
    api2018 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
    api2019 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'  # 2019年数据

    encoding = 'utf-8-sig'
    fileData = r'data\all_data.csv'
    
    def start_requests(self):
        leftUrls = self.load_urls()
        for url in leftUrls:
            yield scrapy.Request(url=url, headers=self.headers)
    
    def parse(self, response):
        pass

    def load_urls(self):
        to_crawl_urls = set()
        crawled_urls = set()
        if os.path.exists(self.fileData):
            df_tmp = pd.read_csv(self.fileData, encoding=self.encoding)['from_url']
            crawled_urls = set(df_tmp['from_url'])
            to_crawl_urls = set(df_tmp['next_url'])
        left_urls = to_crawl_urls - crawled_urls
        return left_urls
