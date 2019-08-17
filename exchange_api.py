#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import urlencode
from constant import note2change

from constant import exchange_appkey

# ----------------------------------
# 货币汇率调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/23
# ----------------------------------

# 人民币牌价
def request1(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/exchange/rmbquot"
    params = {
        "key": exchange_appkey,  # APP Key
        "type": "0",  # 两种格式(0或者1,默认为0)

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"


# 外汇汇率
def request2(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/exchange/frate"
    params = {
        "key": appkey,  # APP Key
        "type": "",  # 两种格式(0或者1,默认为0)

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"


#1.人民币牌价
#request1(appkey, "GET")

#2.外汇汇率
#request2(appkey, "GET")


def format_exchange():
    data = request1(exchange_appkey, "GET")
    if not data:
        return
    xx = list()
    for i in data:
        for _, v in i.items():
            for item_k, item_v in note2change.items():
                if item_k == v['name']:
                    if v['fBuyPri'] == None:
                        v['fBuyPri'] = '0'
                    if  v['mBuyPri'] == None:
                        v['mBuyPri'] = '0'
                    xx.append({
                        'name': item_v,
                        u'fBuyPri': v['fBuyPri'],
                        u'mBuyPri': v['mBuyPri'],
                    })
    return xx

def juhe_exchange():
    # a =  [{
    #     u'fBuyPri': u'42.5600',
    #     u'mBuyPri': u'46.1000',
    #     'name': u'USD'
    # },
    #     {
    #         u'fBuyPri': u'42.5600',
    #         u'mBuyPri': u'46.1000',
    #         'name': u'RMB'
    #     }]

    a= format_exchange()
    if not a:
        return u'汇率接口访问超出免费配额每日100次，稍后再试'
    ss = ''
    for i in a:
        if i.get('fBuyPri') != None:
            fBuyPri = i.get('fBuyPri')
        else:
            fBuyPri = ' '
        if  i.get('mBuyPri') != None:
            mBuyPri = i.get('mBuyPri', ' ')
        else:
            mBuyPri = ' '
        ss += i['name'] + u'  现汇买入价   ' + fBuyPri  + '\n' +i['name']+u'  现钞买入价  '+ mBuyPri + '\n'
    return ss


#print test()