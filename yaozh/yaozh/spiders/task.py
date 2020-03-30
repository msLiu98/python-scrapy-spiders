# -*- coding: utf-8 -*-
import scrapy
from ..items import YaozhTaskItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import pandas as pd
import os
from ..params import prvcsStatDict, grdDict, typeDict


class TaskSpider(scrapy.Spider):
    name = 'task'

    apiRoot = 'https://db.yaozh.com/hmap?'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": 'acw_tc=2f624a1415848005210845028e4d6a848a5a3aee4faf5ac222921256a4ca5f; _ga=GA1.3.1642981795.1584800738; UtzD_f52b_saltkey=Qi20Ksz2; UtzD_f52b_lastvisit=1584798431; yaozh_mylogin=1584838115; UtzD_f52b_ulastactivity=1584800714%7C0; think_language=zh-CN; PHPSESSID=kthcp86k5inrgkcikt7ajbl4d4; hmap_show=true; _gid=GA1.2.557271595.1585124682; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1584855834,1584864459,1584919860,1585124682; _ga=GA1.2.1012859415.1584802034; yaozh_logintime=1585124687; yaozh_user=896097%09msLiuThomas; yaozh_userId=896097; yaozh_jobstatus=kptta67UcJieW6zKnFSe2JyXnoaZcJtlnpuHnKZxanJT1qeSoMZYoNdzaJJyVNDYrsrZuMmm0pbYhqDUbXBvWp3CrKWS1Z%2FSyVty1HJjk5%2B24556CF29CB1c00dD285C1cc3c67C66fEkpmclW%2BdaJydmINuqm9sa4OtmqDGWKDXc2iUclSUmpqWlZaVbZ1slpSWg26038916cbb67ac153bbf72e23d51f981cc; db_w_auth=761419%09msLiuThomas; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D761419; UtzD_f52b_creditbase=0D0D2D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; UtzD_f52b_lastact=1585124688%09uc.php%09; UtzD_f52b_auth=e9ebqsjjZAnyR7KABpSPEhd3kXweS6%2BUjddx4MRr1ZIdXMS70w06j3eZqBsLAbM6yI2gCUGykuKN3%2FgWB9avHM%2FxzSw; _gid=GA1.3.557271595.1585124682; kztoken=nJail6zJp6iXaJqWl3FnYWNsaZmb; his=a%3A7%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsZ5uS%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsZ5yS%22%3Bi%3A2%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsaJOU%22%3Bi%3A3%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsaJWT%22%3Bi%3A4%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsaJaS%22%3Bi%3A5%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsaJaZ%22%3Bi%3A6%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FnYWNsaZmb%22%3B%7D; _gat=1; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1585124871',
        "Host": "db.yaozh.com",
        "Referer": "https://db.yaozh.com/hmap?",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    
    cntyFile = r'_utils\county.csv'
    fileTaskGrdBed = r'_utils\task_grd_bed.csv'
    fileTask = r'_utils\task_grd_bed.csv'
    pageSize = '30'
    
    def start_requests(self):
        bdstr = '1'
        grd = '全部'
        tp = '全部'
        addr = ''
        prvc = '北京市'
        pg = '1'
        
        toCrawlTasks = self.get_task_grd()
        self.logger.info(f'剩余任务数量 {len(toCrawlTasks)}')
        for tid, task in toCrawlTasks.items():
            grd, tp, prvc = task.split('_')
            params = {
                'bedstr': bdstr,
                'bedend': '',
                'grade': grd,
                'type': tp,
                'address': addr,
                'province': prvc,
                'p': pg,
                'pageSize': self.pageSize
            }
            meta = {
                'tid': tid,
                'task': task
            }
            yield scrapy.FormRequest(url=self.apiRoot, headers=self.headers, formdata=params, method='GET', meta=meta)

    def parse(self, response):
        loader = ItemLoader(item=YaozhTaskItem(), response=response)
        # with open('tmp2.html', 'w', encoding='utf-8-sig') as f_tmp:
        #     f_tmp.write(response.text)
        tid = response.meta['tid']
        task = response.meta['task']
        dtnum = response.xpath('//div[@class="tr offset-top"]/@data-total').extract()
        loader.add_value('tid', tid)
        loader.add_value('task', task)
        if dtnum:
            loader.add_value('dtnum', dtnum[0])
        else:
            loader.add_value('dtnum', '0')
        yield loader.load_item()
        
    def get_task_cnty(self):
        df_tmp = pd.read_csv(self.cntyFile, encoding='utf-8-sig', dtype=str)[['county', 'county_code']]
        df_tmp['prv_code'] = df_tmp['county_code'].map(lambda i: '{}0000'.format(i[:2]))
        df_tmp['province'] = df_tmp['prv_code'].map(prvcsStatDict)
        df_tmp['task'] = df_tmp['province'] + '_' + df_tmp['county'].map(lambda i: i[:2])
        df_tmp['task_id'] = df_tmp['prv_code'] + '_' + df_tmp['county_code'].map(lambda i: i[:6])
        return dict(zip(df_tmp['task_id'], df_tmp['task']))

    def get_task_grd(self):
        task = ['_'.join([grade, tp, prv]) for grade in grdDict.values() for tp in typeDict.values() for prv in prvcsStatDict.values()]
        taskId = ['_'.join([grade, tp, prv]) for grade in grdDict.keys() for tp in typeDict.keys() for prv in prvcsStatDict.keys()]
        toCrawl = dict(zip(taskId, task))
        fp_to = self.fileTask
        if os.path.exists(fp_to):
            taskIdCrawled = pd.read_csv(fp_to, encoding='utf-8-sig')['tid']
            for x in taskIdCrawled:
                toCrawl.pop(x)
        return toCrawl
