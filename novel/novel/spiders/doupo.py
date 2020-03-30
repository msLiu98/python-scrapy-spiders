# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ..items import CtnItem
from scrapy.loader import ItemLoader
import os


class DoupoSpider(scrapy.Spider):
    name = 'doupo'
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # "Host": "www.biquge.info",
        # "Referer": "https://www.biquge.info/10_10229/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }
    
    chpFile = r'_utils\chp_urls.csv'
    dataDir = r'data'
    
    def start_requests(self):
        crawledChps = os.listdir(self.dataDir)
        df_urls = pd.read_csv(self.chpFile)
        for i, row in df_urls.iterrows():
            chpTitle = row['chp_title']
            chpUrl = row['chp_url']
            fileName = f'{i}_{chpTitle}.txt'
            meta = {
                'file_name': fileName,
            }
            if fileName not in crawledChps:
                yield scrapy.Request(url=chpUrl, headers=self.headers, meta=meta)
    
    def parse(self, response):
        loader = ItemLoader(item=CtnItem(), response=response)
        loader.add_value("file_name", response.meta['file_name'])
        loader.add_value("chp_url", response.url)
        loader.add_xpath("chp_title", '//div[@class="main"]/h1/text()')
        loader.add_xpath("chp_ctn", '//div[@class="txt"]//text()')
        return loader.load_item()
