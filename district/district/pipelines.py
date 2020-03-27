# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import *
import csv
import os
from pandas import DataFrame


class DistrictPipeline(object):
    province_path = 'province.csv'
    city_path = 'city.csv'
    county_path = 'county.csv'
    town_path = 'town.csv'
    village_path = 'village.csv'

    def process_item(self, item, spider):
        if isinstance(item, ProvinceItem):
            if not os.path.exists(self.province_path):
                with open(self.province_path, 'a+', encoding='utf-8', newline='') as f_csv:
                    writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                    writer.writeheader()
            with open(self.province_path, 'a+', encoding='utf-8', newline='') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                writer.writerow(item)
                
        elif isinstance(item, CityItem):
            if not os.path.exists(self.city_path):
                with open(self.city_path, 'a+', encoding='utf-8', newline='') as f_csv:
                    writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                    writer.writeheader()
            with open(self.city_path, 'a+', encoding='utf-8', newline='') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                writer.writerow(item)

        elif isinstance(item, CountyItem):
            if not os.path.exists(self.county_path):
                with open(self.county_path, 'a+', encoding='utf-8', newline='') as f_csv:
                    writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                    writer.writeheader()
            with open(self.county_path, 'a+', encoding='utf-8', newline='') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                writer.writerow(item)
                
        elif isinstance(item, TownItem):
            if not os.path.exists(self.town_path):
                with open(self.town_path, 'a+', encoding='utf-8', newline='') as f_csv:
                    writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                    writer.writeheader()
            with open(self.town_path, 'a+', encoding='utf-8', newline='') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                writer.writerow(item)

        elif isinstance(item, VillageItem):
            if not os.path.exists(self.village_path):
                with open(self.village_path, 'a+', encoding='utf_8_sig', newline='') as f_csv:
                    writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                    writer.writeheader()
            with open(self.village_path, 'a+', encoding='utf_8_sig', newline='') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=item.keys())
                writer.writerow(item)
        elif isinstance(item, dict):
            df = DataFrame(item)
            if not os.path.exists(self.village_path):
                df.to_csv(self.village_path, mode='a+', encoding='utf_8_sig', index=False, header=True)
            else:
                df.to_csv(self.village_path, mode='a+', encoding='utf_8_sig', index=False, header=False)
