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
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "clickbids=10229; Hm_lvt_6dfe3c8f195b43b8e667a2a2e5936122=1578143929; Hm_lpvt_6dfe3c8f195b43b8e667a2a2e5936122=1578147996",
        "Host": "www.biquge.info",
        "Pragma": "no-cache",
        "Referer": "https://www.biquge.info/10_10229/",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }

    def start_requests(self):
        chps_crawled = set(os.listdir(r'D:\Projects_Github\Projects_Scrapy\novel\chp_content'))
        df_urls = pd.read_csv(r'D:\Projects_Github\Projects_Scrapy\novel\chp_urls2.csv')
        for i, url in enumerate(df_urls['chp_urls']):
            file_name = '_'.join([str(df_urls['index'][i]), df_urls['chp_titles'][i], '.txt']).replace('?_', '')
            meta = {
                'file_name': file_name,
            }
            if file_name not in chps_crawled:
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, meta=meta)
    
    def parse(self, response):
        loader = ItemLoader(item=CtnItem(), response=response)
        loader.add_value("file_name", response.meta['file_name'])
        loader.add_value("chp_url", response.url)
        loader.add_xpath("chp_title", '//div[@class="bookname"]/h1/text()')
        loader.add_xpath("chp_ctn", '//div[@id="content"]//text()')
        item = loader.load_item()
        return item
