import requests


def main():
    video_url = 'http://upos-sz-mirrorkodo.bilivideo.com/upgcxcode/85/12/146961285/146961285-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1581523309&gen=playurl&os=kodobv&oi=1974527994&trid=970349eec6c0437fa1c57f6ef9400587u&platform=pc&upsig=c70fe4f2631533323668dbeea35e28a4&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=10250622'
    sound_url = 'http://upos-sz-mirrorkodo.bilivideo.com/upgcxcode/85/12/146961285/146961285-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1581523309&gen=playurl&os=kodobv&oi=1974527994&trid=970349eec6c0437fa1c57f6ef9400587u&platform=pc&upsig=231b9e742a74122b5d27afdcd0ff88a6&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=10250622'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.bilibili.com/video/av85978152/?spm_id_from=trigger_reload'
    }
    r = requests.get(url=video_url, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        with open('video.mp4', 'wb') as f_tmp:
            f_tmp.write(r.content)
            print('video done!')
    r = requests.get(url=sound_url, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        with open('video.mp3', 'wb') as f_tmp:
            f_tmp.write(r.content)
            print('sound done!')


if __name__ == '__main__':
    main()
