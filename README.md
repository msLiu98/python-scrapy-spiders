# python-scrapy-spiders

## 项目简介
本项目包含一些我自己建立的、使用和完善后的scrapy爬虫项目

## 目录

- [中国行政区划代码爬虫](district/district)

## 爬虫详细介绍

### 中国行政区划代码爬虫

* [示例网址](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/)

* 难度级别： &spades; &spades;

* 功能介绍

    - 较强的鲁棒性，支持断点重续爬取
    
    - 不同模式，FIFO（深度爬取）和LIFO（广度爬取）
    
* 爬虫代码介绍

    1. [adcode.py](district/district/spiders/adcode.py)
    
        * 深度爬取，从省级向村级一级一级递进爬取
        
        * 缺点：没有断点重续
        
    2. [adcode2.py](district/district/spiders/adcode2.py)
        
        * `adcode.py`改进，记录网址作为爬取依据
        
        * 支持断点重续
        
    3. [village.py](district/district/spiders/village.py)
    
        * 历史版本

