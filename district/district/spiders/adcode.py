# -*- coding: utf-8 -*-
import scrapy
from ..items import *
from scrapy.loader import ItemLoader
from urllib.parse import urljoin
from scrapy.loader.processors import MapCompose
import os
import time


class DistrictSpider(scrapy.Spider):
    name = 'adcode'
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
    api2018 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
    api2019 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'  # 2019年数据
    # TODO http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2011/ 2011年的数据

    fileProv = r'data\province.csv'
    fileCity = r'data\city.csv'
    fileCnty = r'data\county.csv'
    fileTown = r'data\town.csv'
    fileVlge = r'data\village.csv'

    def start_requests(self):
        # print(os.getcwd())  # 'D:\Projects_Github\Public_Projects\python-scrapy-spiders\district'
        # time.sleep(5)
        yield scrapy.Request(url=self.api2019, headers=self.headers, callback=self.get_prov)

    def get_prov(self, response):
        ld_prov = ItemLoader(item=ProvItem(), response=response)
        ld_prov.add_xpath('prov_name', '//tr[@class="provincetr"]/td/a/text()')
        ld_prov.add_xpath('prov_url', '//tr[@class="provincetr"]/td/a/@href', MapCompose(lambda i: urljoin(self.api2019, i)))
        item_prov = ld_prov.load_item()
        yield item_prov
        for url in item_prov['prov_url']:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.get_city)

    def get_city(self, response):
        ld_city = ItemLoader(item=CityItem(), response=response)
        ld_city.add_xpath('city_name', '//tr[@class="citytr"]/td[2]/a/text()')
        ld_city.add_xpath('city_code', '//tr[@class="citytr"]/td[1]/a/text()')
        ld_city.add_xpath('city_url', '//tr[@class="citytr"]/td[2]/a/@href', MapCompose(lambda i: urljoin(self.api2019, i)))
        item_city = ld_city.load_item()
        yield item_city
        for url in item_city['city_url']:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.get_cnty)

    def get_cnty(self, response):  # 6位地区代码
        apiCnty = response.url[:response.url.rfind('/') + 1]
        ld_cnty = ItemLoader(item=CntyItem(), response=response)
        ld_cnty.add_xpath('cnty_name', '//tr[@class="countytr"]/td[2]/a/text()')
        ld_cnty.add_xpath('cnty_code', '//tr[@class="countytr"]/td[1]/a/text()')
        ld_cnty.add_xpath('cnty_url', '//tr[@class="countytr"]/td[2]/a/@href', MapCompose(lambda i: urljoin(apiCnty, i)))
        item_cnty = ld_cnty.load_item()
        yield item_cnty
        for url in item_cnty['cnty_url']:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.get_town)

    def get_town(self, response):  # 9位地区代码
        apiTown = response.url[:response.url.rfind('/') + 1]
        ld_town = ItemLoader(item=TownItem(), response=response)
        ld_town.add_xpath('town_name', '//tr[@class="towntr"]/td[2]/a/text()')
        ld_town.add_xpath('town_code', '//tr[@class="towntr"]/td[1]/a/text()')
        ld_town.add_xpath('town_url', '//tr[@class="towntr"]/td[2]/a/@href', MapCompose(lambda i: urljoin(apiTown, i)))
        item_town = ld_town.load_item()
        yield item_town
        # for url in item_town['cnty_url']:
        #     yield scrapy.Request(url=url, headers=self.headers, callback=self.get_town)
