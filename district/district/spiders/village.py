# -*- coding: utf-8 -*-
import scrapy
import os
import pandas as pd
from ..items import *
import time


class VillageSpider(scrapy.Spider):
    name = 'village'
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

    def start_requests(self):
        town_dir = r'D:\Projects_Github\Repositories_Pycharm\Project_Summary\0-2 Projects_Collections\Scrapy\district\data_out'
        town_file = 'town.csv'
        town_path = os.path.join(town_dir, town_file)
        df_town = pd.read_csv(town_path)
        urls = df_town['town_url']
        crawled_path = r'D:\Projects_Github\Repositories_Pycharm\Project_Summary\0-2 Projects_Collections\Scrapy\district\district\spiders\village.csv'
        crawled = []
        if os.path.exists(crawled_path):
            crawled = pd.read_csv(crawled_path, encoding='utf_8_sig')['url']
        urls = set(urls) - set(crawled)
        print(len(urls))
        time.sleep(3)
        for url in urls:
            # headers = self.headers.copy()
            # headers['User-Agent'] = ua.random()
            yield scrapy.Request(url=url, headers=self.headers, callback=self.get_village)

    def get_village(self, response):
        url = response.url
        villages_codes = response.xpath('//tr[@class="villagetr"]/td[1]/text()').extract()
        village_categories = response.xpath('//tr[@class="villagetr"]/td[2]/text()').extract()
        villages_names = response.xpath('//tr[@class="villagetr"]/td[3]/text()').extract()
        # for village, code, village_category in zip(villages_names, villages_codes, village_categories):
        #     village_item = VillageItem()
        #     village_item['village'] = village
        #     village_item['village_code'] = code
        #     village_item['village_category'] = village_category
        #     village_item['url'] = url
        #     yield village_item
        village_dict = {
            "village": villages_names,
            "village_code": villages_codes,
            "village_category": village_categories,
            "url": url,
        }
        yield village_dict
