# -*- coding: utf-8 -*-
import scrapy
from ..items import YaozhItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import re
import pandas as pd
import os


class YzspiderSpider(scrapy.Spider):
    name = 'yzspider'
    apiRoot = 'https://db.yaozh.com/hmap?'
    urlRoot = 'https://db.yaozh.com'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": 'kztoken=nJail6zJp6iXaJqWl3FnY2JtZ5mV; his=a%3A1%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnY2JtZ5mV%22%3B%7D; acw_tc=2f624a1415848005210845028e4d6a848a5a3aee4faf5ac222921256a4ca5f; _ga=GA1.3.1642981795.1584800738; UtzD_f52b_saltkey=Qi20Ksz2; UtzD_f52b_lastvisit=1584798431; yaozh_mylogin=1584838115; UtzD_f52b_ulastactivity=1584800714%7C0; _ga=GA1.2.1012859415.1584802034; think_language=zh-CN; PHPSESSID=finra3hhehveed9s967go09c95; _gid=GA1.2.1213570040.1585315665; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1584864459,1584919860,1585124682,1585315665; hmap_show=true; yaozh_logintime=1585315930; yaozh_user=896097%09msLiuThomas; yaozh_userId=896097; yaozh_jobstatus=kptta67UcJieW6zKnFSe2JyXnoaZcJtlnpuHnKZxanJT1qeSoMZYoNdzaJJyVNDYrsrZuMmm0pbYhqDUbXBvWp3CrKWS1Z%2FSyVty1HJjk5%2B283bd8981103F489Be4FdaC108ab83b0EkpmclmiXaZucnINuqm9sa4OtmqDGWKDXc2iUclSUmpqWl5WWcJhmmJWVg26046aa4fcb8370d267e6e4dde4fb4d4fee; db_w_auth=761419%09msLiuThomas; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D761419; UtzD_f52b_creditbase=0D0D4D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; UtzD_f52b_lastact=1585315932%09uc.php%09; UtzD_f52b_auth=a3d0B9nOl%2FltVgmTGeQusZRPNVkhV9InxJuGss1E4pf0ZcdbNbBrQCgXKnj1j0dDKCdH62t3%2FlE46ARkcuzcg3nszKI; _gid=GA1.3.1213570040.1585315665; kztoken=nJail6zJp6iXaJqWl3FnY2JtapiV; his=a%3A2%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnY2JtZ5mV%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnY2JtapiV%22%3B%7D; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1585315954',
        "Host": "db.yaozh.com",
        "Referer": "https://db.yaozh.com/hmap?",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    pgSize = '30'
    fileTask = r'_utils\task_grd_bed_page.csv'
    fileData = r'data\hosp_data_grd_bed.csv'
    encoding = 'utf-8-sig'
    
    def start_requests(self):
        bdstr = '1'
        grd = '全部'
        tp = '全部'
        addr = ''
        prvc = '北京市'
        pg = '1'
        
        tasks = self.load_tasks()
        self.logger.info(f'总共有 {len(tasks)} 页数据待爬取')
        for task in tasks:
            # 三级甲等_综合医院_内蒙古自治区_1
            grd, tp, prvc, pg = task.split('_')
            params = {
                'bedstr': bdstr,
                'bedend': '',
                'grade': grd,
                'type': tp,
                'address': addr,
                'province': prvc,
                'p': pg,
                'pageSize': self.pgSize
            }
            meta = {
                'tid': task,
                'pid': '_'.join(params.values())
            }
            yield scrapy.FormRequest(url=self.apiRoot, headers=self.headers, method='GET', formdata=params, meta=meta)

    def parse(self, response):
        response.body.decode(response.encoding)
        with open('tmp2.html', 'w', encoding='utf-8-sig') as f_tmp:
            f_tmp.write(response.text)
        tid = response.meta['tid']
        pid = response.meta['pid']
        loader = ItemLoader(item=YaozhItem(), response=response)
        loader.add_value("tid", tid)
        loader.add_value("pid", pid)
        loader.add_xpath("name", '//table[@class="table table-striped"]/tbody/tr/th/a/text()')
        loader.add_xpath('purl', '//table[@class="table table-striped"]/tbody/tr/th/a/@href', MapCompose(lambda i: ''.join([self.urlRoot, i])))  # 笨办法，得到医院页面网址，再爬数据
        loader.add_xpath('text', '//table[@class="table table-striped"]/tbody/tr//text()', Join('|'))
        # loader.add_xpath("grade", '//table[@class="table table-striped"]//tr/td[1]/text()')
        # loader.add_xpath("type", '//table[@class="table table-striped"]//tr/td[2]/text()')
        # loader.add_xpath("prvc", '//table[@class="table table-striped"]//tr/td[3]/text()')
        # loader.add_xpath("city", '//table[@class="table table-striped"]//tr/td[4]/text()')
        # loader.add_xpath("cnty", '//table[@class="table table-striped"]//tr/td[5]/text()')
        # loader.add_xpath("bdnm", '//table[@class="table table-striped"]//tr/td[6]/text()')
        # loader.add_xpath("adr", '//table[@class="table table-striped"]//tr/td[7]/text()')
        yield loader.load_item()
        
    def load_tasks(self):
        toCrawl = pd.read_csv(self.fileTask, encoding=self.encoding)['tid']
        crawled = list()
        if os.path.exists(self.fileData):
            crawled = pd.read_csv(self.fileData, encoding=self.encoding)['tid']
        left = set(toCrawl) - set(crawled)
        return left
