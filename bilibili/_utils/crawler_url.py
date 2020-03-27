import requests
import re
import json


def test():
    url = 'https://search.bilibili.com/all?keyword=%E5%BC%A0%E4%BC%9F&from_source=nav_search_new&page=2'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": 'https://www.bilibili.com/index.html',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }
    r = requests.get(url=url, headers=headers)
    print(r.status_code)
    print(r.text)


def main():
    url2 = 'https://www.bilibili.com/video/av75088331'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": url2,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }
    r = requests.get(url=url2, headers=headers)
    print(r.status_code)
    pattern_video = re.compile('.__playinfo__=(.*?)</script>')
    text = r.content.decode(r.encoding)
    text_data = re.findall(pattern_video, text)[0]
    data = json.loads(text_data)
    cid = re.findall('cid=(\d*)&', text)
    if cid:
        print(cid[0])
        url_cmt = 'http://comment.bilibili.com/{cid}.xml'.format(cid=cid[0])
        r_cmt = requests.get(url_cmt)
        with open('comment.html', 'w', encoding='utf-8') as f_tmp:
            f_tmp.write(r_cmt.content.decode())
    if data:
        with open('data.json', 'w') as f_js:
            f_js.write(text_data)
        print(data)


if __name__ == '__main__':
    test()
