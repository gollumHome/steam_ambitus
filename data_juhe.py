#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

#import Decimal
import operator
import json, urllib
from urllib import urlencode

from exchange_api import format_exchange
from collections import OrderedDict
from steam_api import request_stream_asset
from constant import steam_appid,steam_appkey


def format_aseet():
    # assets =  [{
	# 		"prices": {
	# 			"USD": 249,
	# 			"GBP": 205,
	# 			"BYN": 0
	# 		},
	# 		"name": "1383",
	# 		"date": "2019-03-05",
	# 		"class": [{
	# 			"name": "def_index",
	# 			"value": "1383"
	# 		}],
	# 		"classid": "3213434708"
	# 	}]
    assets = request_stream_asset()
    current_exchange = format_exchange()
    # current_exchange = [{
    #     u'fBuyPri': '42.5600',
    #     u'mBuyPri': '46.1000',
    #     'name': u'USD'
    # },
    #     {
    #         u'fBuyPri': u'42.5600',
    #         u'mBuyPri': u'46.1000',
    #         'name': u'GBP'
    #     }
    # ]
    asset_result_list = []
    for i in assets:
        asset_prices = list()
        for currency_type, currency_num in i['prices'].items():
            for item_exchange in current_exchange:
                if item_exchange['name'] == currency_type:
                    num1 = currency_num / 100/100
                    num2 =float(item_exchange['fBuyPri'])
                    num = num1 * num2
                    temp = OrderedDict()
                    temp['RNY'] = round(num, 3)
                    temp[currency_type] = currency_num
                    asset_prices.append(temp)
        asset_result_list.append({'name': i['name'],
                                  'prices': asset_prices})
    return asset_result_list


def view_text_price(asset_id):
    asset_result_list = format_aseet()
    print asset_result_list
    for item in asset_result_list:
        if str(asset_id) == item['name']:
            return item['prices']


def result_to_str_juhe(asset_id):
    result = view_text_price(str(asset_id))
    sorted_list = sorted(result, key=operator.itemgetter('RNY'), reverse=False)
    ss = ''
    if result:
        for item in sorted_list:
            for k, v in item.items():
                ss += k + ' ' + str(v)+'Y' + '  '
            ss += '\n'
        return ss

#print format_aseet()
#print result_to_str(1383)