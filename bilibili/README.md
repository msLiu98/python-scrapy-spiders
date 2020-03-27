# Bilibili project


## 视频爬虫要点

1. referer 的限制导致网页直接对 m4s 网址访问错误，在请求头中加入 referer 即可
2. m4s 是一种 音频/视频 文件，所以需要判断到底是音频还是视频，不过目前已解决
3. bilibili 的视频网页源代码有 视频 和 音频 的链接


## 一些 api

1. 用户的关注列表与动态列表
    ```shell script
    url_follow = 'https://api.vc.bilibili.com/feed/v1/feed/get_attention_list?uid={uid}'
    ```

2. 搜索链接
    ```shell script
    url_search = 'https://search.bilibili.com/all?keyword={word}&from_source=nav_search_new&page={page}'
    api_search = 'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&search_type=video&keyword={}&page={}'.format(word=word, page=page)
    ```
   
3. 视频网址
    ```shell script
    url_video = 'https://www.bilibili.com/video/{av_id}'
    ```

4. 弹幕链接
    ```shell script
    url_danmu = 'http://comment.bilibili.com/{cid}.xml'
    ```