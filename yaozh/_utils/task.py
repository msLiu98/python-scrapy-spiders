import requests
from lxml import etree
import pandas as pd
from pprint import pprint
import math


def get_initial_page(prvc, adr=''):
    apiRoot = 'https://db.yaozh.com/hmap?'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "db.yaozh.com",
        "Referer": "https://db.yaozh.com/hmap?",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    cookies = {
        'Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94': '1584800730',
        'Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94': '1584800524',
        'PHPSESSID': 'g5dbm46h2s8ko7mp1ieqdorno6',
        'UtzD_f52b_creditbase': '0D0D0D0D0D0D0D0D0',
        'UtzD_f52b_creditnotice': '0D0D2D0D0D0D0D0D0D761419',
        'UtzD_f52b_creditrule': '%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95',
        'UtzD_f52b_lastact': '1584838116%09uc.php%09',
        'UtzD_f52b_lastvisit': '1584798431',
        'UtzD_f52b_saltkey': 'Qi20Ksz2',
        'UtzD_f52b_ulastactivity': '1584800714%7C0',
        '_ga': 'GA1.3.1642981795.1584800738',
        '_gat': '1',
        '_gid': 'GA1.3.880137863.1584800738',
        'acw_tc': '707c9f9915848006694621700e316b294a1d86864ea43ada7df91db84ab4d8',
        'his': 'a%3A10%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapmT%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapmb%22%3Bi%3A2%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapqb%22%3Bi%3A3%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRwapya%22%3Bi%3A4%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYZOT%22%3Bi%3A5%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYZWY%22%3Bi%3A6%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpaW%22%3Bi%3A7%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpaZ%22%3Bi%3A8%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpiZ%22%3Bi%3A9%3Bs%3A28%3A%22nJail6zJp6iXaJqWl3FmaGRxYpqX%22%3B%7D',
        'hmap_show': 'true',
        'kztoken': 'nJail6zJp6iXaJqWl3FmaGRxYpqX',
        'think_language': 'zh-CN',
        'yaozh_mylogin': '1584838115',
        'yaozh_uidhas': '1',
        'yaozh_userId': '896097'
    }
    params = {
        'grade': '全部',
        'type': '全部',
        'address': adr,
        'province': prvc,
        'p': '1',
        'pageSize': '30'
    }
    r = requests.get(url=apiRoot, params=params, headers=headers, cookies=cookies)
    html = etree.HTML(r.content.decode(r.apparent_encoding))
    total = html.xpath('//div[@class="tr offset-top"]/@data-total')
    if total:
        total = int(total[0])
        page_num = int(total / 30) + 1
    else:
        total = 0
        page_num = 0
    return total, page_num


def req_by_city(): # 36451 + 3041 = 39492
    tasks = {
        '130000_130100': '河北省_石家庄',
        '130000_130200': '河北省_唐山',
        '130000_130300': '河北省_秦皇岛',
        '130000_130400': '河北省_邯郸',
        '130000_130500': '河北省_邢台',
        '130000_130600': '河北省_保定',
        '130000_130700': '河北省_张家口',
        '130000_130800': '河北省_承德',
        '130000_130900': '河北省_沧州',
        '130000_131000': '河北省_廊坊',
        '130000_131100': '河北省_衡水',
        '140000_140100': '山西省_太原',
        '140000_140200': '山西省_大同',
        '140000_140300': '山西省_阳泉',
        '140000_140400': '山西省_长治',
        '140000_140500': '山西省_晋城',
        '140000_140600': '山西省_朔州',
        '140000_140700': '山西省_晋中',
        '140000_140800': '山西省_运城',
        '140000_140900': '山西省_忻州',
        '140000_141000': '山西省_临汾',
        '140000_141100': '山西省_吕梁',
        '150000_150100': '内蒙古自治区_呼和浩特',
        '150000_150200': '内蒙古自治区_包头',
        '150000_150300': '内蒙古自治区_乌海',
        '150000_150400': '内蒙古自治区_赤峰',
        '150000_150500': '内蒙古自治区_通辽',
        '150000_150600': '内蒙古自治区_鄂尔多斯',
        '150000_150700': '内蒙古自治区_呼伦贝尔',
        '150000_150800': '内蒙古自治区_巴彦淖尔',
        '150000_150900': '内蒙古自治区_乌兰察布',
        '150000_152200': '内蒙古自治区_兴安',
        '150000_152500': '内蒙古自治区_锡林郭勒',
        '150000_152900': '内蒙古自治区_阿拉善',
        '210000_210100': '辽宁省_沈阳',
        '210000_210200': '辽宁省_大连',
        '210000_210300': '辽宁省_鞍山',
        '210000_210400': '辽宁省_抚顺',
        '210000_210500': '辽宁省_本溪',
        '210000_210600': '辽宁省_丹东',
        '210000_210700': '辽宁省_锦州',
        '210000_210800': '辽宁省_营口',
        '210000_210900': '辽宁省_阜新',
        '210000_211000': '辽宁省_辽阳',
        '210000_211100': '辽宁省_盘锦',
        '210000_211200': '辽宁省_铁岭',
        '210000_211300': '辽宁省_朝阳',
        '210000_211400': '辽宁省_葫芦岛',
        '220000_220100': '吉林省_长春',
        '220000_220200': '吉林省_吉林市',
        '220000_220300': '吉林省_四平',
        '220000_220400': '吉林省_辽源',
        '220000_220500': '吉林省_通化',
        '220000_220600': '吉林省_白山',
        '220000_220700': '吉林省_松原',
        '220000_220800': '吉林省_白城',
        '220000_222400': '吉林省_延边',
        '230000_230100': '黑龙江省_哈尔滨',
        '230000_230200': '黑龙江省_齐齐哈尔',
        '230000_230300': '黑龙江省_鸡西',
        '230000_230400': '黑龙江省_鹤岗',
        '230000_230500': '黑龙江省_双鸭山',
        '230000_230600': '黑龙江省_大庆',
        '230000_230700': '黑龙江省_伊春',
        '230000_230800': '黑龙江省_佳木斯',
        '230000_230900': '黑龙江省_七台河',
        '230000_231000': '黑龙江省_牡丹江',
        '230000_231100': '黑龙江省_黑河',
        '230000_231200': '黑龙江省_绥化',
        '230000_232700': '黑龙江省_大兴安岭',
        '320000_320100': '江苏省_南京',
        '320000_320200': '江苏省_无锡',
        '320000_320300': '江苏省_徐州',
        '320000_320400': '江苏省_常州',
        '320000_320500': '江苏省_苏州',
        '320000_320600': '江苏省_南通',
        '320000_320700': '江苏省_连云港',
        '320000_320800': '江苏省_淮安',
        '320000_320900': '江苏省_盐城',
        '320000_321000': '江苏省_扬州',
        '320000_321100': '江苏省_镇江',
        '320000_321200': '江苏省_泰州',
        '320000_321300': '江苏省_宿迁',
        '330000_330100': '浙江省_杭州',
        '330000_330200': '浙江省_宁波',
        '330000_330300': '浙江省_温州',
        '330000_330400': '浙江省_嘉兴',
        '330000_330500': '浙江省_湖州',
        '330000_330600': '浙江省_绍兴',
        '330000_330700': '浙江省_金华',
        '330000_330800': '浙江省_衢州',
        '330000_330900': '浙江省_舟山',
        '330000_331000': '浙江省_台州',
        '330000_331100': '浙江省_丽水',
        '340000_340100': '安徽省_合肥',
        '340000_340200': '安徽省_芜湖',
        '340000_340300': '安徽省_蚌埠',
        '340000_340400': '安徽省_淮南',
        '340000_340500': '安徽省_马鞍山',
        '340000_340600': '安徽省_淮北',
        '340000_340700': '安徽省_铜陵',
        '340000_340800': '安徽省_安庆',
        '340000_341000': '安徽省_黄山',
        '340000_341100': '安徽省_滁州',
        '340000_341200': '安徽省_阜阳',
        '340000_341300': '安徽省_宿州',
        '340000_341500': '安徽省_六安',
        '340000_341600': '安徽省_亳州',
        '340000_341700': '安徽省_池州',
        '340000_341800': '安徽省_宣城',
        '350000_350100': '福建省_福州',
        '350000_350200': '福建省_厦门',
        '350000_350300': '福建省_莆田',
        '350000_350400': '福建省_三明',
        '350000_350500': '福建省_泉州',
        '350000_350600': '福建省_漳州',
        '350000_350700': '福建省_南平',
        '350000_350800': '福建省_龙岩',
        '350000_350900': '福建省_宁德',
        '360000_360100': '江西省_南昌',
        '360000_360200': '江西省_景德镇',
        '360000_360300': '江西省_萍乡',
        '360000_360400': '江西省_九江',
        '360000_360500': '江西省_新余',
        '360000_360600': '江西省_鹰潭',
        '360000_360700': '江西省_赣州',
        '360000_360800': '江西省_吉安',
        '360000_360900': '江西省_宜春',
        '360000_361000': '江西省_抚州',
        '360000_361100': '江西省_上饶',
        '370000_370100': '山东省_莱芜',
        '370000_370200': '山东省_青岛',
        '370000_370300': '山东省_淄博',
        '370000_370400': '山东省_枣庄',
        '370000_370500': '山东省_东营',
        '370000_370600': '山东省_烟台',
        '370000_370700': '山东省_潍坊',
        '370000_370800': '山东省_济宁',
        '370000_370900': '山东省_泰安',
        '370000_371000': '山东省_威海',
        '370000_371100': '山东省_日照',
        '370000_371300': '山东省_临沂',
        '370000_371400': '山东省_德州',
        '370000_371500': '山东省_聊城',
        '370000_371600': '山东省_滨州',
        '370000_371700': '山东省_菏泽',
        '410000_410100': '河南省_郑州',
        '410000_410200': '河南省_开封',
        '410000_410300': '河南省_洛阳',
        '410000_410400': '河南省_平顶山',
        '410000_410500': '河南省_安阳',
        '410000_410600': '河南省_鹤壁',
        '410000_410700': '河南省_新乡',
        '410000_410800': '河南省_焦作',
        '410000_410900': '河南省_濮阳',
        '410000_411000': '河南省_许昌',
        '410000_411100': '河南省_漯河',
        '410000_411200': '河南省_三门峡',
        '410000_411300': '河南省_南阳',
        '410000_411400': '河南省_商丘',
        '410000_411500': '河南省_信阳',
        '410000_411600': '河南省_周口',
        '410000_411700': '河南省_驻马店',
        '410000_419001': '河南省_济源',
        '420000_420100': '湖北省_武汉',
        '420000_420200': '湖北省_黄石',
        '420000_420300': '湖北省_十堰',
        '420000_420500': '湖北省_宜昌',
        '420000_420600': '湖北省_襄阳',
        '420000_420700': '湖北省_鄂州',
        '420000_420800': '湖北省_荆门',
        '420000_420900': '湖北省_孝感',
        '420000_421000': '湖北省_荆州',
        '420000_421100': '湖北省_黄冈',
        '420000_421200': '湖北省_咸宁',
        '420000_421300': '湖北省_随州',
        '420000_422800': '湖北省_恩施',
        '420000_429004': '湖北省_仙桃',
        '420000_429005': '湖北省_潜江',
        '420000_429006': '湖北省_天门',
        '420000_429021': '湖北省_神农架',
        '430000_430100': '湖南省_长沙',
        '430000_430200': '湖南省_株洲',
        '430000_430300': '湖南省_湘潭',
        '430000_430400': '湖南省_衡阳',
        '430000_430500': '湖南省_邵阳',
        '430000_430600': '湖南省_岳阳',
        '430000_430700': '湖南省_常德',
        '430000_430800': '湖南省_张家界',
        '430000_430900': '湖南省_益阳',
        '430000_431000': '湖南省_郴州',
        '430000_431100': '湖南省_永州',
        '430000_431200': '湖南省_怀化',
        '430000_431300': '湖南省_娄底',
        '430000_433100': '湖南省_湘西土家族苗族自治州',
        '440000_440100': '广东省_广州',
        '440000_440200': '广东省_韶关',
        '440000_440300': '广东省_深圳',
        '440000_440400': '广东省_珠海',
        '440000_440500': '广东省_汕头',
        '440000_440600': '广东省_佛山',
        '440000_440700': '广东省_江门',
        '440000_440800': '广东省_湛江',
        '440000_440900': '广东省_茂名',
        '440000_441200': '广东省_肇庆',
        '440000_441300': '广东省_惠州',
        '440000_441400': '广东省_梅州',
        '440000_441500': '广东省_汕尾',
        '440000_441600': '广东省_河源',
        '440000_441700': '广东省_阳江',
        '440000_441800': '广东省_清远',
        '440000_441900': '广东省_东莞',
        '440000_442000': '广东省_中山',
        '440000_445100': '广东省_潮州',
        '440000_445200': '广东省_揭阳',
        '440000_445300': '广东省_云浮',
        '450000_450100': '广西壮族自治区_南宁',
        '450000_450200': '广西壮族自治区_柳州',
        '450000_450300': '广西壮族自治区_桂林',
        '450000_450400': '广西壮族自治区_梧州',
        '450000_450500': '广西壮族自治区_北海',
        '450000_450600': '广西壮族自治区_防城港',
        '450000_450700': '广西壮族自治区_钦州',
        '450000_450800': '广西壮族自治区_贵港',
        '450000_450900': '广西壮族自治区_玉林',
        '450000_451000': '广西壮族自治区_百色',
        '450000_451100': '广西壮族自治区_贺州',
        '450000_451200': '广西壮族自治区_河池',
        '450000_451300': '广西壮族自治区_来宾',
        '450000_451400': '广西壮族自治区_崇左',
        '460000_460100': '海南省_海口',
        '460000_460200': '海南省_三亚',
        '460000_460300': '海南省_三亚2',
        '460000_460400': '海南省_儋州',
        '460000_469001': '海南省_五指山',
        '460000_469002': '海南省_琼海',
        '460000_469005': '海南省_文昌',
        '460000_469006': '海南省_万宁',
        '460000_469007': '海南省_东方',
        '460000_469021': '海南省_定安',
        '460000_469022': '海南省_屯昌',
        '460000_469023': '海南省_澄迈',
        '460000_469024': '海南省_临高',
        '460000_469025': '海南省_白沙黎族自治县',
        '460000_469026': '海南省_昌江黎族自治县',
        '460000_469027': '海南省_乐东黎族自治县',
        '460000_469028': '海南省_陵水黎族自治县',
        '460000_469029': '海南省_保亭黎族苗族自治县',
        '460000_469030': '海南省_琼中黎族苗族自治县',
        '510000_510100': '四川省_成都',
        '510000_510300': '四川省_自贡',
        '510000_510400': '四川省_攀枝花',
        '510000_510500': '四川省_泸州',
        '510000_510600': '四川省_德阳',
        '510000_510700': '四川省_绵阳',
        '510000_510800': '四川省_广元',
        '510000_510900': '四川省_遂宁',
        '510000_511000': '四川省_内江',
        '510000_511100': '四川省_乐山',
        '510000_511300': '四川省_南充',
        '510000_511400': '四川省_眉山',
        '510000_511500': '四川省_宜宾',
        '510000_511600': '四川省_广安',
        '510000_511700': '四川省_达州',
        '510000_511800': '四川省_雅安',
        '510000_511900': '四川省_巴中',
        '510000_512000': '四川省_资阳',
        '510000_513200': '四川省_阿坝藏族羌族自治州',
        '510000_513300': '四川省_甘孜藏族自治州',
        '510000_513400': '四川省_凉山彝族自治州',
        '520000_520100': '贵州省_贵阳',
        '520000_520200': '贵州省_六盘水',
        '520000_520300': '贵州省_遵义',
        '520000_520400': '贵州省_安顺',
        '520000_520500': '贵州省_毕节地区',
        '520000_520600': '贵州省_铜仁地区',
        '520000_522300': '贵州省_黔西南布依族苗族自治州',
        '520000_522600': '贵州省_黔东南苗族侗族自治州',
        '520000_522700': '贵州省_黔南布依族苗族自治州',
        '530000_530100': '云南省_昆明',
        '530000_530300': '云南省_曲靖',
        '530000_530400': '云南省_玉溪',
        '530000_530500': '云南省_保山',
        '530000_530600': '云南省_昭通',
        '530000_530700': '云南省_丽江',
        '530000_530800': '云南省_普洱',
        '530000_530900': '云南省_临沧',
        '530000_532300': '云南省_楚雄彝族自治州',
        '530000_532500': '云南省_红河哈尼族彝族自治州',
        '530000_532600': '云南省_文山壮族苗族自治州',
        '530000_532800': '云南省_西双版纳傣族自治州',
        '530000_532900': '云南省_大理白族自治州',
        '530000_533100': '云南省_德宏傣族景颇族自治州',
        '530000_533300': '云南省_怒江傈僳族自治州',
        '530000_533400': '云南省_迪庆藏族自治州',
        '540000_540100': '西藏自治区_拉萨',
        '540000_540200': '西藏自治区_日喀则地区',
        '540000_540300': '西藏自治区_昌都地区',
        '540000_540400': '西藏自治区_林芝地区',
        '540000_540500': '西藏自治区_山南地区',
        '540000_540600': '西藏自治区_那曲地区',
        '540000_542500': '西藏自治区_阿里地区',
        '610000_610100': '陕西省_西安',
        '610000_610200': '陕西省_铜川',
        '610000_610300': '陕西省_宝鸡',
        '610000_610400': '陕西省_咸阳',
        '610000_610500': '陕西省_渭南',
        '610000_610600': '陕西省_延安',
        '610000_610700': '陕西省_汉中',
        '610000_610800': '陕西省_榆林',
        '610000_610900': '陕西省_安康',
        '610000_611000': '陕西省_商洛',
        '620000_620100': '甘肃省_兰州',
        '620000_620200': '甘肃省_嘉峪关',
        '620000_620300': '甘肃省_金昌',
        '620000_620400': '甘肃省_白银',
        '620000_620500': '甘肃省_天水',
        '620000_620600': '甘肃省_武威',
        '620000_620700': '甘肃省_张掖',
        '620000_620800': '甘肃省_平凉',
        '620000_620900': '甘肃省_酒泉',
        '620000_621000': '甘肃省_庆阳',
        '620000_621100': '甘肃省_定西',
        '620000_621200': '甘肃省_陇南',
        '620000_622900': '甘肃省_临夏回族自治州',
        '620000_623000': '甘肃省_甘南藏族自治州',
        '630000_630100': '青海省_西宁',
        '630000_630200': '青海省_海东地区',
        '630000_632200': '青海省_海北藏族自治州',
        '630000_632300': '青海省_黄南藏族自治州',
        '630000_632500': '青海省_海南藏族自治州',
        '630000_632600': '青海省_果洛藏族自治州',
        '630000_632700': '青海省_玉树藏族自治州',
        '630000_632800': '青海省_海西蒙古族藏族自治州',
        '640000_640100': '宁夏回族自治区_银川',
        '640000_640200': '宁夏回族自治区_石嘴山',
        '640000_640300': '宁夏回族自治区_吴忠',
        '640000_640400': '宁夏回族自治区_固原',
        '640000_640500': '宁夏回族自治区_中卫',
        '650000_650100': '新疆维吾尔自治区_乌鲁木齐',
        '650000_650200': '新疆维吾尔自治区_克拉玛依',
        '650000_650400': '新疆维吾尔自治区_吐鲁番地区',
        '650000_650500': '新疆维吾尔自治区_哈密地区',
        '650000_652300': '新疆维吾尔自治区_昌吉回族自治州',
        '650000_652700': '新疆维吾尔自治区_博尔塔拉蒙古自治州',
        '650000_652800': '新疆维吾尔自治区_巴音郭楞蒙古自治州',
        '650000_652900': '新疆维吾尔自治区_阿克苏地区',
        '650000_653000': '新疆维吾尔自治区_克孜勒苏柯尔克孜自治州',
        '650000_653100': '新疆维吾尔自治区_喀什地区',
        '650000_653200': '新疆维吾尔自治区_和田地区',
        '650000_654000': '新疆维吾尔自治区_伊犁哈萨克自治州',
        '650000_654200': '新疆维吾尔自治区_塔城地区',
        '650000_654300': '新疆维吾尔自治区_阿勒泰地区',
        '650000_659001': '新疆维吾尔自治区_石河子',
        '650000_659002': '新疆维吾尔自治区_阿拉尔',
        '650000_659003': '新疆维吾尔自治区_图木舒克',
        '650000_659004': '新疆维吾尔自治区_五家渠',
        '650000_659005': '新疆维吾尔自治区_北屯',
        '650000_659006': '新疆维吾尔自治区_铁门关',
        '650000_659007': '新疆维吾尔自治区_双河',
        '650000_659008': '新疆维吾尔自治区_可克达拉',
        '650000_659009': '新疆维吾尔自治区_昆玉'
    }
    tasksStr = {
        '110000_110101': '北京市_东城区',
        '110000_110102': '北京市_西城区',
        '110000_110105': '北京市_朝阳区',
        '110000_110106': '北京市_丰台区',
        '110000_110107': '北京市_石景山区',
        '110000_110108': '北京市_海淀区',
        '110000_110109': '北京市_门头沟区',
        '110000_110111': '北京市_房山区',
        '110000_110112': '北京市_通州区',
        '110000_110113': '北京市_顺义区',
        '110000_110114': '北京市_昌平区',
        '110000_110115': '北京市_大兴区',
        '110000_110116': '北京市_怀柔区',
        '110000_110117': '北京市_平谷区',
        '110000_110118': '北京市_密云区',
        '110000_110119': '北京市_延庆区',
        '120000_120101': '天津市_和平区',
        '120000_120102': '天津市_河东区',
        '120000_120103': '天津市_河西区',
        '120000_120104': '天津市_南开区',
        '120000_120105': '天津市_河北区',
        '120000_120106': '天津市_红桥区',
        '120000_120110': '天津市_东丽区',
        '120000_120111': '天津市_西青区',
        '120000_120112': '天津市_津南区',
        '120000_120113': '天津市_北辰区',
        '120000_120114': '天津市_武清区',
        '120000_120115': '天津市_宝坻区',
        '120000_120116': '天津市_滨海新区',
        '120000_120117': '天津市_宁河区',
        '120000_120118': '天津市_静海区',
        '120000_120119': '天津市_蓟州区',
        '310000_310101': '上海市_黄浦区',
        '310000_310104': '上海市_徐汇区',
        '310000_310105': '上海市_长宁区',
        '310000_310106': '上海市_静安区',
        '310000_310107': '上海市_普陀区',
        '310000_310109': '上海市_虹口区',
        '310000_310110': '上海市_杨浦区',
        '310000_310112': '上海市_闵行区',
        '310000_310113': '上海市_宝山区',
        '310000_310114': '上海市_嘉定区',
        '310000_310115': '上海市_浦东新区',
        '310000_310116': '上海市_金山区',
        '310000_310117': '上海市_松江区',
        '310000_310118': '上海市_青浦区',
        '310000_310120': '上海市_奉贤区',
        '310000_310151': '上海市_崇明区',
        '500000_500101': '重庆市_万州区',
        '500000_500102': '重庆市_涪陵区',
        '500000_500103': '重庆市_渝中区',
        '500000_500104': '重庆市_大渡口区',
        '500000_500105': '重庆市_江北区',
        '500000_500106': '重庆市_沙坪坝区',
        '500000_500107': '重庆市_九龙坡区',
        '500000_500108': '重庆市_南岸区',
        '500000_500109': '重庆市_北碚区',
        '500000_500110': '重庆市_綦江区',
        '500000_500111': '重庆市_大足区',
        '500000_500112': '重庆市_渝北区',
        '500000_500113': '重庆市_巴南区',
        '500000_500114': '重庆市_黔江区',
        '500000_500115': '重庆市_长寿区',
        '500000_500116': '重庆市_江津区',
        '500000_500117': '重庆市_合川区',
        '500000_500118': '重庆市_永川区',
        '500000_500119': '重庆市_南川区',
        '500000_500120': '重庆市_璧山区',
        '500000_500151': '重庆市_铜梁区',
        '500000_500152': '重庆市_潼南区',
        '500000_500153': '重庆市_荣昌区',
        '500000_500154': '重庆市_开州区',
        '500000_500155': '重庆市_梁平区',
        '500000_500156': '重庆市_武隆区'
    }
    
    taskDict = {
        'task_id': '',
        'task': '',
        'total': '',
        'page': ''
    }
    task_id = list()
    tasklst = list()
    totallst = list()
    pagelst = list()
    count = 0
    for taskId, task in tasksStr.items():
        try:
            prv1, adr1 = task.split('_')
            adr1 = adr1[:2]
            tData, tPage = get_initial_page(prv1, adr1)
            task = '_'.join([prv1, adr1])
            task_id.append(taskId)
            tasklst.append(task)
            totallst.append(tData)
            pagelst.append(tPage)
            print(tData, tPage)
            count += 1
            # if count == 30:
            #     break
        except Exception as e:
            print(e)
            continue
    print(count)
    taskDict['task_id'] = task_id
    taskDict['task'] = tasklst
    taskDict['total'] = totallst
    taskDict['page'] = pagelst
    df = pd.DataFrame(taskDict)
    df.to_csv('task3.csv', encoding='utf-8-sig', index=False)
    

def req_by_prv():  # 98313
    taskPrv = {
        "110000": "北京市",
        "120000": "天津市",
        "130000": "河北省",
        "140000": "山西省",
        "150000": "内蒙古自治区",
        "210000": "辽宁省",
        "220000": "吉林省",
        "230000": "黑龙江省",
        "310000": "上海市",
        "320000": "江苏省",
        "330000": "浙江省",
        "340000": "安徽省",
        "350000": "福建省",
        "360000": "江西省",
        "370000": "山东省",
        "410000": "河南省",
        "420000": "湖北省",
        "430000": "湖南省",
        "440000": "广东省",
        "450000": "广西壮族自治区",
        "460000": "海南省",
        "500000": "重庆市",
        "510000": "四川省",
        "520000": "贵州省",
        "530000": "云南省",
        "540000": "西藏自治区",
        "610000": "陕西省",
        "620000": "甘肃省",
        "630000": "青海省",
        "640000": "宁夏回族自治区",
        "650000": "新疆维吾尔自治区",
    }
    
    taskDict = {
        'task_id': '',
        'task': '',
        'total': '',
        'page': ''
    }
    task_id = list()
    tasklst = list()
    totallst = list()
    pagelst = list()
    count = 0
    for prvId, prvName in taskPrv.items():
        try:
            tData, tPage = get_initial_page(prvName)
            task_id.append(prvId)
            tasklst.append(prvName)
            totallst.append(tData)
            pagelst.append(tPage)
            print(tData, tPage)
            count += 1
            # if count == 30:
            #     break
        except Exception as e:
            print(e)
            continue
    print(count)
    taskDict['task_id'] = task_id
    taskDict['task'] = tasklst
    taskDict['total'] = totallst
    taskDict['page'] = pagelst
    df = pd.DataFrame(taskDict)
    df.to_csv('taskPrv.csv', encoding='utf-8-sig', index=False)


def req_by_cnty():
    tasksCnty = get_task_cnty()
    taskDict = {
        'task_id': '',
        'task': '',
        'total': '',
        'page': ''
    }
    task_id = list()
    tasklst = list()
    totallst = list()
    pagelst = list()
    count = 0
    for taskId, task in tasksCnty.items():
        try:
            prv1, adr1 = task.split('_')
            adr1 = adr1[:2]
            tData, tPage = get_initial_page(prv1, adr1)
            task = '_'.join([prv1, adr1])
            task_id.append(taskId)
            tasklst.append(task)
            totallst.append(tData)
            pagelst.append(tPage)
            print(tData, tPage)
            count += 1
            # if count == 10:
            #     break
        except Exception as e:
            print(e)
            continue
    print(count)
    taskDict['task_id'] = task_id
    taskDict['task'] = tasklst
    taskDict['total'] = totallst
    taskDict['page'] = pagelst
    df = pd.DataFrame(taskDict)
    df.to_csv('taskCnty.csv', encoding='utf-8-sig', index=False)
    

def get_task_cnty():
    taskPrv = {
        "110000": "北京市",
        "120000": "天津市",
        "130000": "河北省",
        "140000": "山西省",
        "150000": "内蒙古自治区",
        "210000": "辽宁省",
        "220000": "吉林省",
        "230000": "黑龙江省",
        "310000": "上海市",
        "320000": "江苏省",
        "330000": "浙江省",
        "340000": "安徽省",
        "350000": "福建省",
        "360000": "江西省",
        "370000": "山东省",
        "410000": "河南省",
        "420000": "湖北省",
        "430000": "湖南省",
        "440000": "广东省",
        "450000": "广西壮族自治区",
        "460000": "海南省",
        "500000": "重庆市",
        "510000": "四川省",
        "520000": "贵州省",
        "530000": "云南省",
        "540000": "西藏自治区",
        "610000": "陕西省",
        "620000": "甘肃省",
        "630000": "青海省",
        "640000": "宁夏回族自治区",
        "650000": "新疆维吾尔自治区",
    }
    df_tmp = pd.read_csv('county.csv', encoding='utf-8-sig', dtype=str)[['county', 'county_code']]
    df_tmp['prv_code'] = df_tmp['county_code'].map(lambda i: '{}0000'.format(i[:2]))
    df_tmp['province'] = df_tmp['prv_code'].map(taskPrv)
    df_tmp['task'] = df_tmp['province'] + '_' + df_tmp['county'].map(lambda i: i[:2])
    df_tmp['task_id'] = df_tmp['prv_code'] + '_' + df_tmp['county_code'].map(lambda i: i[:6])
    return dict(zip(df_tmp['task_id'], df_tmp['task']))


if __name__ == '__main__':
    df = pd.read_csv(r'D:\Projects_Github\Projects_Scrapy\yaozh\_utils\task_grd_bed.csv', encoding='utf-8-sig', dtype={'dtnum': int})
    df1 = df[(df['dtnum'] > 200)]  # cnty 21075, type 78226
    df2 = df[(df['dtnum'] <= 200) & (df['dtnum'] > 0)]  # cnty 62302, type 20082, grd_bed 12897
    print(df['dtnum'].sum())
    print(df2['dtnum'].sum())
    df2['pgnum'] = (df2['dtnum'] / 30).map(math.ceil)
    # print(df2.head())
    toCrawlPage = list()
    for i, row in df2.iterrows():
        pgnum = row['pgnum']
        for n in range(1, pgnum + 1):
            toCrawlPage.append('_'.join([row['task'], str(n)]))
    df3 = pd.DataFrame({'tid': toCrawlPage})
    df3.to_csv('task_grd_bed_page.csv', encoding='utf-8-sig', index=False)
