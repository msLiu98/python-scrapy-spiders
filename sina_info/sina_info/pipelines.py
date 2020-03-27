# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaInfoPipeline(object):
    def process_item(self, item, spider):
        with open('sina_basic_info.txt', 'a+', encoding='utf-8') as f_basic_info:
            f_basic_info.write('\t'.join(item['basic_info'].values()))
            f_basic_info.write('\n')
        with open('sina_resume_info.txt', 'a+', encoding='utf-8') as f_resume_info:
            f_resume_info.write('\n'.join(['\t'.join(piece.values()) for piece in item['resume_info']]))
            f_resume_info.write('\n')
        return item
