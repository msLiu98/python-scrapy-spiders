# -*- coding: utf-8 -*-
import scrapy
from ..items import YaozhTaskItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import pandas as pd
import os


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
    cookies = {
        'Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94': '1584800730',
        'Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94': '1584800524',
        'PHPSESSID': 'g5dbm46h2s8ko7mp1ieqdorno6',
        'UtzD_f52b_creditbase': '0D0D0D0D0D0D0D0D0',
        'UtzD_f52b_creditnotice': '0D0D2D0D0D0D0D0D0D761419',
        'UtzD_f52b_creditrule': '%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95',
        'UtzD_f52b_lastact': '1584838116%09uc.php%09',
        'UtzD_f52b_lastvisit': '1584798431',
        'UtzD_f52b_saltkey': 'Qi20Ksz2',
        'UtzD_f52b_ulastactivity': '1584800714%7C0',
        '_ga': 'GA1.3.1642981795.1584800738',
        '_gat': '1',
        '_gid': 'GA1.3.880137863.1584800738',
        'acw_tc': '707c9f9915848006694621700e316b294a1d86864ea43ada7df91db84ab4d8',
        'his': 'a%3A10%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapmT%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapmb%22%3Bi%3A2%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapqb%22%3Bi%3A3%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapya%22%3Bi%3A4%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYZOT%22%3Bi%3A5%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYZWY%22%3Bi%3A6%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpaW%22%3Bi%3A7%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpaZ%22%3Bi%3A8%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpiZ%22%3Bi%3A9%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpqX%22%3B%7D',
        'hmap_show': 'true',
        'kztoken': 'nJail6zJp6iXaJqWl3FmaGRxYpqX',
        'think_language': 'zh-CN',
        'yaozh_mylogin': '1584838115',
        'yaozh_uidhas': '1',
        'yaozh_userId': '896097'
    }
    lgcookies = {
        'Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94': '1584800730',
        'Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94': '1584800524',
        'PHPSESSID': 'cb73sj0tfumgpi91o43kq2k1s7',
        'UtzD_f52b_auth': 'c272ILiDkKFX6ACK1V475f8J1IwZxlOYewBrehxCqCYZgklWoApcLZyWdfpx4QdbIQZ4KoRyTF3FxQoeGCSDs024%2BsY',
        'UtzD_f52b_lastact': '1584883795%09uc.php%09',
        'UtzD_f52b_lastvisit': '1584798431',
        'UtzD_f52b_saltkey': 'Qi20Ksz2',
        'UtzD_f52b_ulastactivity': '1584800714%7C0',
        '_ga': 'GA1.3.1642981795.1584800738',
        '_gat': '1',
        '_gid': 'GA1.3.880137863.1584800738',
        'acw_tc': '707c9f9915848006694621700e316b294a1d86864ea43ada7df91db84ab4d8',
        'db_w_auth': '761419%09msLiuThomas',
        'his': 'a%3A10%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGVpaZuX%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGVpaZub%22%3Bi%3A2%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGVpapeZ%22%3Bi%3A3%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGVqZJmU%22%3Bi%3A4%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGVrZ5uX%22%3Bi%3A5%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGVrZ5yW%22%3Bi%3A6%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGZtaZaT%22%3Bi%3A7%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGZtaZaU%22%3Bi%3A8%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGdsZZiZ%22%3Bi%3A9%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGlrapOZ%22%3B%7D',
        'hmap_show': 'true',
        'kztoken': 'nJail6zJp6iXaJqWl3FmaGlrapOZ',
        'think_language': 'zh-CN',
        'yaozh_jobstatus': 'kptta67UcJieW6zKnFSe2JyXnoaZcJtlnpuHnKZxanJT1qeSoMZYoNdzaJJyVNDYrsrZuMmm0pbYhqDUbXBvWp3CrKWS1Z%2FSyVty1HJjk5%2BE02d75B3d6713Ac61b3e63F944E6d169EkpmclW%2BVZ5WbmYNuqm9sa4OtmqDGWKDXc2iUclSUmpqVnJyUbp5pnJqVg26036dda4b1e059c58625cceb7e611634fb',
        'yaozh_logintime': '1584883793',
        'yaozh_mylogin': '1584838115',
        'yaozh_uidhas': '1',
        'yaozh_user': '896097%09msLiuThomas',
        'yaozh_userId': '896097'
    }
    
    fileTaskGrdBed = r'D:\Projects_Github\Projects_Scrapy\yaozh\_utils\task_grd_bed.csv'
    fileTask = r'D:\Projects_Github\Projects_Scrapy\yaozh\_utils\task_grd_bed.csv'
    
    def start_requests(self):
        # toCrawlTasks = self.get_task_cnty()
        # for tid, task in toCrawlTasks.items():
        #     prvc, adr = task.split('_')
        #     adr = adr[:2]
        #     params = {
        #         'grade': '全部',
        #         'type': '全部',
        #         'address': adr,
        #         'province': prvc,
        #         'p': '1',
        #         'pageSize': '30'
        #     }
        #     meta = {
        #         'tid': tid,
        #         'task': '_'.join([prvc, adr])
        #     }
        #     yield scrapy.FormRequest(url=self.apiRoot, headers=self.headers, cookies=self.cookies, formdata=params, method='GET', meta=meta)
        toCrawlTasks = self.get_task_grade()
        self.logger.info(f'剩余任务数量 {len(toCrawlTasks)}')  # 6205 续接
        for tid, task in toCrawlTasks.items():
            # grd, prv = task.split('_')
            grd, tp, prv = task.split('_')
            params = {
                'bedstr': '1',
                'bedend': '',
                'grade': grd,
                'type': tp,  # 默认 '全部'
                'address': '',
                'province': prv,
                'p': '1',
                'pageSize': '30'
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
        
    @staticmethod
    def get_task_cnty():
        taskPrv = {
            "110000": "北京市",
            "120000": "天津市",
            "130000": "河北省",
            "140000": "山西省",
            "150000": "内蒙古自治区",
            "210000": "辽宁省",
            "220000": "吉林省",
            "230000": "黑龙江省",
            "310000": "上海市",
            "320000": "江苏省",
            "330000": "浙江省",
            "340000": "安徽省",
            "350000": "福建省",
            "360000": "江西省",
            "370000": "山东省",
            "410000": "河南省",
            "420000": "湖北省",
            "430000": "湖南省",
            "440000": "广东省",
            "450000": "广西壮族自治区",
            "460000": "海南省",
            "500000": "重庆市",
            "510000": "四川省",
            "520000": "贵州省",
            "530000": "云南省",
            "540000": "西藏自治区",
            "610000": "陕西省",
            "620000": "甘肃省",
            "630000": "青海省",
            "640000": "宁夏回族自治区",
            "650000": "新疆维吾尔自治区",
        }
        df_tmp = pd.read_csv(r'D:\Projects_Github\Projects_Scrapy\yaozh\_utils\county.csv', encoding='utf-8-sig', dtype=str)[['county', 'county_code']]
        df_tmp['prv_code'] = df_tmp['county_code'].map(lambda i: '{}0000'.format(i[:2]))
        df_tmp['province'] = df_tmp['prv_code'].map(taskPrv)
        df_tmp['task'] = df_tmp['province'] + '_' + df_tmp['county'].map(lambda i: i[:2])
        df_tmp['task_id'] = df_tmp['prv_code'] + '_' + df_tmp['county_code'].map(lambda i: i[:6])
        return dict(zip(df_tmp['task_id'], df_tmp['task']))

    def get_task_grade(self):
        grdDict = {
            '301': '三级甲等',
            '302': '三级乙等',
            '303': '三级丙等',
            '300': '三级未定',
            '201': '二级甲等',
            '202': '二级乙等',
            '203': '二级丙等',
            '200': '二级未定',
            '101': '一级甲等',
            '102': '一级乙等',
            '103': '一级丙等',
            '100': '一级未定',
            '000': '未定级'
        }
        tpDict = {
            '001': '综合医院',
            '002': '中医医院',
            '003': '中西医结合医院',
            '004': '专科医院',
            '005': '民族医院',
            '006': '妇幼保健院',
            '007': '专科疾病防治院（所、站）',
            '008': '护理院',
            '009': '疗养院',
            '010': '社区卫生服务中心',
            '011': '乡镇卫生院',
            '012': '疾病预防控制中心',
            '013': '计划生育服务中心',
            '014': '门诊部',
            '015': '诊所',
            '016': '村卫生室',
            '017': '卫生监督所(中心)',
        }
        taskPrv = {
            "110000": "北京市",
            "120000": "天津市",
            "130000": "河北省",
            "140000": "山西省",
            "150000": "内蒙古自治区",
            "210000": "辽宁省",
            "220000": "吉林省",
            "230000": "黑龙江省",
            "310000": "上海市",
            "320000": "江苏省",
            "330000": "浙江省",
            "340000": "安徽省",
            "350000": "福建省",
            "360000": "江西省",
            "370000": "山东省",
            "410000": "河南省",
            "420000": "湖北省",
            "430000": "湖南省",
            "440000": "广东省",
            "450000": "广西壮族自治区",
            "460000": "海南省",
            "500000": "重庆市",
            "510000": "四川省",
            "520000": "贵州省",
            "530000": "云南省",
            "540000": "西藏自治区",
            "610000": "陕西省",
            "620000": "甘肃省",
            "630000": "青海省",
            "640000": "宁夏回族自治区",
            "650000": "新疆维吾尔自治区",
        }
        # task = ['_'.join([grade, prv]) for grade in grdDict.values() for prv in taskPrv.values()]
        # taskId = ['_'.join([grade, prv]) for grade in grdDict.keys() for prv in taskPrv.keys()]
        task = ['_'.join([grade, tp, prv]) for grade in grdDict.values() for tp in tpDict.values() for prv in taskPrv.values()]
        taskId = ['_'.join([grade, tp, prv]) for grade in grdDict.keys() for tp in tpDict.keys() for prv in taskPrv.keys()]
        toCrawl = dict(zip(taskId, task))
        fp_to = self.fileTask
        if os.path.exists(fp_to):
            taskIdCrawled = pd.read_csv(fp_to, encoding='utf-8-sig')['tid']
            for x in taskIdCrawled:
                toCrawl.pop(x)
        return toCrawl
