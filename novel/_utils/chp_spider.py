import requests
from lxml import etree
import pandas as pd
import re
import time


def main():
    chp_url = "https://www.biquge.info/10_10229/"
    chp_url2 = "http://www.shuquge.com/txt/83108/index.html"
    chp_url3 = 'http://www.shuquge.com/txt/70/'  # 大主宰
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "bcolor=; font=; size=; fontcolor=; width=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }
    r = requests.get(url=chp_url3, headers=headers)
    print(r.status_code)
    r.encoding = r.apparent_encoding
    text = r.content.decode('utf-8-sig', errors='ignore')
    # print(text)
    with open('zhuzai.html', 'w', encoding='utf-8-sig') as f_tmp:
        f_tmp.write(text)
    html = etree.HTML(text)
    xp_chp_url = '//div[@id="list"]//a/@href'
    xp_chp_title = '//div[@id="list"]//a/@title'
    xp_chp_url2 = '//div[@class="listmain"]//a/@href'
    xp_chp_title2 = '//div[@class="listmain"]//a/text()'
    xp_chp_url3 = '//div[@class="listmain"]/dl/dd/a/@href'
    xp_chp_title3 = '//div[@class="listmain"]/dl/dd/a/text()'
    chp_urls = [chp_url3+href for href in html.xpath(xp_chp_url3)]
    chp_titles = html.xpath(xp_chp_title3)
    info = {
        'chp_urls': chp_urls,
        'chp_titles': chp_titles
    }
    df_tmp = pd.DataFrame(info)
    df_tmp.to_csv('chp_urls_zhuzai.csv', encoding='utf-8-sig', index=False)
    

def gen_index():
    df_tmp = pd.read_csv('chp_urls_zhuzai.csv', encoding='utf-8-sig')
    df_tmp['index'] = df_tmp['chp_urls'].map(lambda i: re.findall('70/(.*)\.html', i)[0])
    df_tmp.to_csv('chp_urls_zhuzai.csv', encoding='utf-8-sig', index=False)


def func_timer(function):
    """
    计时装饰器
    :param function: 待计时函数
    :return: 函数结果
    """
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name=function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name=function.__name__, time=t1 - t0))
        return result
    return function_timer


@func_timer
def req_ctn():
    url = 'http://www.shuquge.com/txt/70/13862196.html'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Cookie": "bcolor=; font=; size=; fontcolor=; width=",
        "Host": "www.shuquge.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.shuquge.com/txt/70/index.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }
    r = requests.get(url=url, headers=headers)
    text = r.content.decode(r.apparent_encoding)
    # print(text)
    title = re.findall('<h1>(.*)</h1>', text)[0]
    return title


if __name__ == '__main__':
    title1 = req_ctn()
    print(title1)
