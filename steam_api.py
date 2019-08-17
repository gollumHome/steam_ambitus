#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division



#import Decimal
import operator
import json, urllib
from urllib import urlencode

from exchange_api import format_exchange
from collections import OrderedDict
from constant import steam_appid,steam_appkey



# Asset price
def request_stream_asset(m="GET"):
    url = "https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?"
    params = {
        "key": steam_appkey,  # APP Key
        "appid": steam_appid,

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["result"]['success']
        if error_code:
            # 成功请求
            return res["result"]['assets']
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"






