# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re
import os
import pandas as pd
from .items import *


class CtnPipeline(object):
    def process_item(self, item, spider):
        assert isinstance(item, CtnItem)
        spider.logger.info('成功获得数据! {}'.format(item['chp_title'][0]))
        fileName = item['file_name'][0]
        fp_to = f'{spider.dataDir}\\{fileName}'
        if not os.path.exists(spider.dataDir):
            os.mkdir(spider.dataDir)
        with open(fp_to, 'w', encoding='utf-8-sig') as f_tmp:
            f_tmp.write(item['chp_title'][0])
            f_tmp.write('\n')
            f_tmp.write('\n'.join(item['chp_ctn']).replace('&nbsp;', ''))


class ChpPipeline(object):
    def process_item(self, item, spider):
        assert isinstance(item, ChpItem)
        file_name = 'chp_urls'
        chp_file = r'D:\Projects_Github\Projects_Scrapy\novel\_csvFiles\{file_name}.csv'
        f_p = chp_file.format(file_name=file_name)
        df_tmp = pd.DataFrame(item)
        df_tmp.to_csv(f_p, mode='a+', encoding='utf-8', header=False)


class NovelCsvPipeline(object):
    def process_item(self, item, spider):
        new_data = dict(item)
        file_name = spider.name
        chp_file = r'D:\Projects_Github\Projects_Scrapy\novel\_csvFiles\{file_name}.csv'
        f_p = chp_file.format(file_name=file_name)
        df_tmp = pd.DataFrame(new_data)
        if os.path.exists(f_p):
            df_tmp.to_csv(f_p, mode='a+', encoding='utf-8', index=False, header=False)
        else:
            df_tmp.to_csv(f_p, mode='a+', encoding='utf-8', index=False)
        return item
