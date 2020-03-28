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
    fileUrl = r'data\all_urls.csv'
    levelDict = {
        0: 'provincetr',
        7: 'citytr',
        9: 'countytr',
        11: 'towntr',
        14: 'villagetr',
    }
    
    def start_requests(self):
        leftUrls = self.load_urls()
        self.logger.info(f'---- 此次运行总任务 {len(leftUrls)} ----')
        for url in leftUrls:
            if url:
                yield scrapy.Request(url=url, headers=self.headers)
    
    def parse(self, response):
        from_url = response.url
        level = len(from_url.split('/')[-1])
        tr = self.levelDict[level]
        ld_data = ItemLoader(item=DataItem(), response=response)
        apiNext = from_url[:from_url.rfind('/') + 1]
        ld_url = ItemLoader(item=UrlItem(), response=response)
        if level == 0:
            ld_data.add_xpath('ad_name', '//tr[@class="provincetr"]/td//text()')  # 这里有些是市辖区，所以要 // 处理
            ld_data.add_xpath('ad_code', '//tr[@class="provincetr"]/td//text()')
            ld_url.add_value('from_url', from_url)
            ld_url.add_xpath('next_url', '//tr[@class="provincetr"]/td/a/@href', MapCompose(lambda i: urljoin(apiNext, i)))
        elif level == 14:
            ld_data.add_xpath('ad_name', f'//tr[@class="{tr}"]/td[3]//text()')  # 这里有些是市辖区，所以要 // 处理
            ld_data.add_xpath('ad_code', f'//tr[@class="{tr}"]/td[1]//text()')
            ld_url.add_value('from_url', from_url)
            ld_url.add_xpath('next_url', f'//tr[@class="{tr}"]/td[2]/a/@href', MapCompose(lambda i: urljoin(apiNext, i)))
        else:
            ld_data.add_xpath('ad_name', f'//tr[@class="{tr}"]/td[2]//text()')  # 这里有些是市辖区，所以要 // 处理
            ld_data.add_xpath('ad_code', f'//tr[@class="{tr}"]/td[1]//text()')
            ld_url.add_value('from_url', from_url)
            ld_url.add_xpath('next_url', f'//tr[@class="{tr}"]/td[2]/a/@href', MapCompose(lambda i: urljoin(apiNext, i)))
        yield ld_data.load_item()
        yield ld_url.load_item()

    def load_urls(self):
        to_crawl_urls = {self.api2019}
        crawled_urls = set()
        if os.path.exists(self.fileUrl):
            df_tmp = pd.read_csv(self.fileUrl, encoding=self.encoding).fillna('')
            crawled_urls = set(df_tmp['from_url'])
            to_crawl_urls.update(set(df_tmp['next_url']))
        to_crawl_urls -= crawled_urls
        return to_crawl_urls
