# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import *
import csv
import os
import pandas as pd


class DistrictPipeline(object):
    def process_item(self, item, spider):
        dfTmp = pd.DataFrame(dict(item))
        if isinstance(item, ProvItem):
            fp_to = spider.fileProv
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
                spider.logger.warning('***** 省级 区域已录入，无需重复录入 *****')
            else:
                spider.logger.info('***** 完成 省级 区域录入 *****')
                
        elif isinstance(item, CityItem):
            fp_to = spider.fileCity
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
            else:
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False, header=False)
            spider.logger.info('***** 完成 市级 区域录入 *****')

        elif isinstance(item, CntyItem):
            fp_to = spider.fileCnty
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
            else:
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False, header=False)
            spider.logger.info('***** 完成 区/县级 区域录入 *****')
                
        elif isinstance(item, TownItem):
            fp_to = spider.fileTown
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
            else:
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False, header=False)
            spider.logger.info('***** 完成 街道/镇级 区域录入 *****')

        elif isinstance(item, VlgeItem):
            fp_to = spider.fileVlge
            if not os.path.exists(fp_to):
                spider.logger.info('没有文件，新创建！')
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False)
            else:
                dfTmp.to_csv(fp_to, mode='a+', encoding='utf-8-sig', index=False, header=False)
            spider.logger.info('***** 完成 居委会/村级 区域录入 *****')
