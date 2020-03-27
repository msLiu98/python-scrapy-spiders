# -*- coding: utf-8 -*-
import scrapy
from ..items import GuchengInfo


class GuchengSpider(scrapy.Spider):
    name = 'gucheng'
    allowed_domains = ['gucheng.com']
    start_urls = ['http://gucheng.com/']
    url_example = 'https://hq.gucheng.com/SZ000021/gaoguanjieshao/'
    base_url = 'https://hq.gucheng.com/{stckid}/gaoguanjieshao/'  # 主网址
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "PHPSESSID=jmu7j6habda96b2f1d3i1uhgcl; Hm_lvt_9636c8f382a28ba02485f6d78a23de71=1563868825,1563868991,1563869076,1563869323; sinaH5EtagStatus=n; Hm_lvt_7b78704799dc5c8066ca16a6c54118da=1563869543; Hm_lpvt_7b78704799dc5c8066ca16a6c54118da=1563869743; Hm_lpvt_9636c8f382a28ba02485f6d78a23de71=1563869756; stockhistory=1%2C3662%2C2049",
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    file_path = r'D:\Projects_Github\Repositories_Pycharm\Summer_Xieweisi\resume_spider\gucheng_info\name_fullstckid.txt'
    checker = dict()

    def start_requests(self):
        name_stckid_company_list = self.read_stckds(self.file_path)
        print(len(name_stckid_company_list))
        for name_stckid_company in name_stckid_company_list:
            name1 = name_stckid_company[0]
            stckid1 = name_stckid_company[1]
            company1 = name_stckid_company[2]
            params = {
                'name': name1,
                'stckid': stckid1,
                'company': company1
            }
            url1 = self.base_url.format(stckid=stckid1)
            yield scrapy.Request(url=url1, headers=self.headers, callback=self.parse, meta={'params': params}, dont_filter=True)

    def parse(self, response):
        params = response.meta['params']
        name = params['name']
        url = response.url
    
        item = GuchengInfo()
        item.update(params)
        item['url'] = url
    
        names_xpath = '//div[@id="hq_wrap"]/div[1]/section/div/table//tr/td[2]/text()'
        position_xpath = '//div[@id="hq_wrap"]/div[1]/section/div/table//tr/td[3]/text()'
        brief_resume_xpath = '//div[@id="hq_wrap"]/div[1]/section/div/table//tr/td[4]/text()'
        names = response.xpath(names_xpath)
        position = response.xpath(position_xpath)
        brief_resume = response.xpath(brief_resume_xpath)
        info_zip = zip(names, position, brief_resume)
    
        item['state'] = '0'
        for piece in tuple(info_zip):
            if name in list(piece)[0].extract():
                item['position'] = piece[1].extract()
                item['brief_resume'] = piece[2].extract()
                item['state'] = '1'
        yield item

    @staticmethod
    def read_stckds(path):
        info_list = list()
        checker = set()
        with open(path, 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                info = line.strip().split()
                name = info[0]
                stckid = info[1]
                judge_id = name + stckid
                recorded = bool(judge_id in checker)
                if not recorded:
                    info_list.append(info)
                    checker.add(judge_id)
        return info_list
