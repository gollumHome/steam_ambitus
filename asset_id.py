#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division


import json, urllib
from urllib import urlencode



steam_appkey = '824367C3B8AA3C7EADD70FF8A0DB3516'
steam_appid = '730'

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


if __name__ == '__main__':
    import os
    assets = list()
    asset_list = request_stream_asset()
    if asset_list:
        for i in asset_list:
            assets.append(i['name'])
    print assets
    dirs = 'd:/id_list.text'
    if not os.path.exists(dirs):
        open(dirs, 'w')
    os.open(dirs, os.O_RDWR)
    with open(dirs, 'w') as f:
        f.write('  '.join(assets))
