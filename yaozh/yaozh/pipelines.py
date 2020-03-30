# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import os
from .items import *


class YaozhPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, YaozhItem):
            info_dict = dict()
            pid = item['pid'][0]
            info_dict['pid'] = pid
            info_dict['tid'] = item['tid'][0]
            info_dict['name'] = item['name']
            info_dict['purl'] = item['purl']
            infoTxt = item['text'][0]
            info_dict['text'] = infoTxt.split('||	|')
            df_tmp = pd.DataFrame(info_dict)
            fp_to = spider.fileData
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                df_tmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
            else:
                df_tmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False, header=False)
            spider.logger.info(f'***** 任务完成 {pid} *****')
            return item
        
        elif isinstance(item, YaozhTaskItem):
            df_tmp = pd.DataFrame(dict(item))
            fp_to = spider.fileTask
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                df_tmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
            else:
                df_tmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False, header=False)
            spider.logger.info(f'***** 获得任务 {item["tid"][0]} *****')
            return item
