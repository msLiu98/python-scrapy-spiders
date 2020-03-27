# -*- coding: utf-8 -*-
import scrapy
from ..items import BasicInfoItem, ResumeInfoItem
from urllib.parse import urlencode
import re


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com']

    base_url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCI_CorpManagerInfo.php?'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'SINAGLOBAL=59.78.22.228_1552659033.846165; SCF=AuNn7m28GPlzfW3Mni9pUBKWeYUk4JRB1gCnAXRJRv43era0PPJ35iw7dDE-J8l1Wh2TnAqkh6IfwatEWS__6_g.; sso_info=v02m6alo5qztYybl42Umoa9rZiXjKadlqWkj5OMuIyznLWNs4ywjpOAwA==; U_TRS1=00000084.d34eba5.5cc10611.b25fa3ff; UOR=www.google.com.hk,finance.sina.com.cn,; visited_funds=511880; SGUID=1560259566030_92580935; UM_distinctid=16b4a338091111-0ee9c8f8986afa-9333061-144000-16b4a338093426; lxlrttp=1560672234; SUB=_2AkMqbjjcf8NxqwJRmP4TzGLkaop1zwrEieKcMskHJRMyHRl-yD9jqmEctRB6Ae4WMzaBG3ThQYTF08xgCMHc1-qhbsTA; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhQbHvumo2BL0fFpngCpAcn; FIN_ALL_VISITED=sh143143; VISITED_BOND=sh143143; ULV=1563712853695:14:8:4:211.80.44.72_1563712847.178210:1563712847975; U_TRS2=000000b7.ae6b5970.5d37a323.cb81d589; FINA_V_S_2=sz002128,sz002055,sz002104,sz002134,sz002047',
        'Host': 'vip.stock.finance.sina.com.cn',
        'Pragma': 'no-cache',
        # 'Referer': 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/002128.phtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    file_name = 'name_stock.txt'

    def start_requests(self):
        to_crawl_list = self.read_stckds(self.file_name)
        print(len(to_crawl_list))
        for info in to_crawl_list:
            name = info[0]
            stckid = info[1]
            meta_params = {
                'name': name,
                'stckid': stckid,
            }
            url_params = {
                'stockid': stckid,
                'Name': name
            }
            try:
                url = self.base_url + urlencode(url_params, encoding='gb2312')
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, meta={'params': meta_params}, dont_filter=True)
            except Exception as e:
                print(e)
                continue

    def parse(self, response):
        params = response.meta['params']
        name = params['name']
        url = response.url

        basic_info_dict = BasicInfoItem()
        info_dict = ResumeInfoItem()

        name_check = response.xpath('//*[@id="Table1"]//tr[1]/td[1]/div/text()')

        if name_check:
            basic_info_dict['url'] = url
            basic_info_dict['name'] = name
            if response.xpath('//table[@id="Table1"]//tr[1]/td[2]/div/text()'):
                basic_info_dict['sex'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table1"]//tr[1]/td[2]/div/text()').extract_first('None').replace('\xa0 ', 'None').replace('\u3000', 'None'))
            else:
                basic_info_dict['sex'] = 'None'
            if response.xpath('//table[@id="Table1"]//tr[1]/td[3]/div/text()'):
                basic_info_dict['birth'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table1"]//tr[1]/td[3]/div/text()').extract_first('None').replace('\xa0', 'None').replace('\u3000', 'None'))
            else:
                basic_info_dict['birth'] = 'None'
            if response.xpath('//table[@id="Table1"]//tr[1]/td[4]/div/text()'):
                basic_info_dict['academy_degree'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table1"]//tr[1]/td[4]/div/text()').extract_first('None').replace('\xa0', 'None').replace('\u3000', 'None'))
            else:
                basic_info_dict['academy_degree'] = 'None'
            if response.xpath('//table[@id="Table1"]//tr[1]/td[5]/div/text()'):
                basic_info_dict['nationality'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table1"]//tr[1]/td[5]/div/text()').extract_first('None').replace('\xa0', 'None').replace('\u3000', 'None'))
            else:
                basic_info_dict['nationality'] = 'None'
            if response.xpath('//table[@id="Table1"]//tr[2]/td[2]/text()'):
                basic_info_dict['brief_resume'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table1"]//tr[2]/td[2]/text()').extract_first('None').replace('\xa0', 'None').replace('\u3000', ''))
            else:
                basic_info_dict['brief_resume'] = 'None'

            resume_info_list = list()
            if response.xpath('//table[@id="Table3"]'):
                for i, company in enumerate(response.xpath('//table[@id="Table3"]//tr/td/div/a/text()'), start=1):
                    info_dict['url'] = url
                    info_dict['name'] = name
                    # info_dict['company'] = company.text.replace('\xa0', 'None').replace('\u3000', 'None')
                    if response.xpath('//table[@id="Table3"]//tr[{i}]/td[2]/div/text()'.format(i=i)):
                        info_dict['position'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table3"]//tr[{i}]/td[2]/div/text()'.format(i=i)).extract_first('None').replace('\xa0', 'None').replace('\u3000', 'None'))
                    else:
                        info_dict['position'] = 'None'
                    if response.xpath('//table[@id="Table3"]//tr[{i}]/td[3]/div/text()'.format(i=i)):
                        info_dict['start_date'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table3"]//tr[{i}]/td[3]/div/text()'.format(i=i)).extract_first('None').replace('\xa0', 'None').replace('\u3000', 'None'))
                    else:
                        info_dict['start_date'] = 'None'
                    if response.xpath('//table[@id="Table3"]//tr[{i}]/td[4]/div/text()'.format(i=i)):
                        info_dict['end_date'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table3"]//tr[{i}]/td[4]/div/text()'.format(i=i)).extract_first('None').replace('\xa0', '').replace('\u3000', 'None'))
                    else:
                        info_dict['end_date'] = 'None'
                    if response.xpath('//table[@id="Table3"]//tr[{i}]/td[5]/div/text()'.format(i=i)):
                        info_dict['salary'] = re.sub('[\r\n\s]', '', response.xpath('//table[@id="Table3"]//tr[{i}]/td[5]/div/text()'.format(i=i)).extract_first('None').replace('\xa0', 'None').replace('\u3000', 'None'))
                    else:
                        info_dict['salary'] = 'None'
                    resume_info_list.append(info_dict)

            total_info_dict = dict()
            total_info_dict['basic_info'] = basic_info_dict
            total_info_dict['resume_info'] = resume_info_list
            yield total_info_dict

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
                judge_id = name+stckid
                recorded = bool(judge_id in checker)
                if not recorded:
                    info_list.append(info)
                    checker.add(judge_id)
        return info_list
