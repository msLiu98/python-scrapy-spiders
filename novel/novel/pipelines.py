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
        dir_path = r'D:\Projects_Github\Projects_Scrapy\novel\_csvFiles\chp_content'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        f_p = os.path.join(dir_path, item['file_name'][0])
        with open(f_p, 'w', encoding='utf-8-sig') as f_tmp:
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
