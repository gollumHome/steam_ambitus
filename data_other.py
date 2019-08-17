# coding: utf-8

import json, urllib
from urllib import urlencode
from constant import steam_appid,steam_appkey
from steam_api import request_stream_asset
from collections import OrderedDict
import operator
import requests

# USD ->
api1 = 'https://www.freeforexapi.com/api/live?pairs=USDJPY,USDRUB,USDNOK,' \
       'USDMYR,USDPHP,USDSGD,USDTHB,USDKRW,USDCAD,USDCHF,USDHKD,USDZAR,USDBRL,' \
       'USDIDR,USDVND,USDTRY,USDUAH,USDMXN,USDPLN,USDAED,USDCLP,USDCOP,' \
       'USDPEN,USDSAR,USDTWD,USDINR,USDARS,USDCRC,USDILS,USDKWD,USDQAR,USDUYU,USDKZT,USDBYN'

api2 = 'https://www.freeforexapi.com/api/live?pairs=GBPUSD,EURUSD,AUDUSD,NZDUSD'

test = 'https://www.freeforexapi.com/api/live?pairs=USDJPY'

def request_exchange_other_api1(m="GET"):
    url = api1
    if m == "GET":
        headers = {"authority": "www.freeforexapi.com"
                 }
        result = requests.get(url, headers=headers)
        res = json.loads(result.text)
        if res['code'] == 200:
            return res['rates']
        return None


def request_exchange_other_api2(m="GET"):
    url = api2
    if m == "GET":
        headers = {"authority": "www.freeforexapi.com"
                 }
        result = requests.get(url, headers=headers)
        res = json.loads(result.text)
        if res['code'] == 200:
            return res['rates']
        return None


# USD ->
data1 = {
		"USDJPY": {
			"rate": 106.258499,
			"timestamp": 1565922366
		},
		"USDRUB": {
			"rate": 66.062901,
			"timestamp": 1565922366
		}
	}

#->USD
data2 = other2usd ={
            "AUDUSD": {
                "timestamp": 1565928846,
                "rate": 0.678935
            },
            "EURUSD": {
                "timestamp": 1565928846,
                "rate": 1.110007
            }}

def get_asset_with_current_exchange():
    # assets =  [{
	# 		"prices": {
	# 			"USD": 249,
	# 			"GBP": 205,
	# 			"ADSD": 1
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
    usd2other = request_exchange_other_api1()
    # usd2other = {
	# 	"USDJPY": {
	# 		"rate": 106.258499,
	# 		"timestamp": 1565922366
	# 	},
	# 	"USDxxx": {
	# 		"rate": 66.062901,
	# 		"timestamp": 1565922366
	# 	}
	# }

    temp_usd2thoer = {}
    for k, v in usd2other.items():
        if 'USD' in k:
            temp_usd2thoer[k.split('USD')[1]] = v
    # other2usd ={
    #         "GBPUSD": {
    #             "timestamp": 1565928846,
    #             "rate": 0.678935
    #         },
    #         "NZDUSD": {
    #             "timestamp": 1565928846,
    #             "rate": 0.644481
    #         },
    #         "EURUSD": {
    #             "timestamp": 1565928846,
    #             "rate": 1.110007
    #         }}
    other2usd = request_exchange_other_api2()
    temp_other2usd = {}
    for k, v in other2usd.items():
        if 'USD' in k:
            temp_other2usd[k.split('USD')[0]] = v


    asset_result_list = []
    for asset_item in assets:
        asset_prices = list()
        for currency_type in asset_item['prices'].keys():
            if currency_type in temp_usd2thoer.keys():
                temp = OrderedDict()
                num_usd = asset_item['prices'][currency_type] / temp_usd2thoer[currency_type]['rate']
                temp['USD'] = round(num_usd, 3)
                temp[currency_type] = asset_item['prices'][currency_type]
                asset_prices.append(temp)
            if currency_type in temp_other2usd.keys():
                temp = OrderedDict()
                num_usd = asset_item['prices'][currency_type] * temp_other2usd[currency_type]['rate']
                temp['USD'] = round(num_usd, 3)
                temp[currency_type] = asset_item['prices'][currency_type]
                asset_prices.append(temp)
        asset_result_list.append({'name': asset_item['name'],
                                  'prices': asset_prices})
    return asset_result_list


def view_text_price(asset_id):
    asset_result_list = get_asset_with_current_exchange()
    for item in asset_result_list:
        if str(asset_id) == item['name']:
            return item['prices']


def result_to_str_other(asset_id):
    result = view_text_price(str(asset_id))
    sorted_list = sorted(result, key=operator.itemgetter('USD'), reverse=False)
    print sorted_list
    ss = ''
    if result:
        for item in sorted_list:
            for k, v in item.items():
                ss += k + ' ' + str(v)+'' + '  '
            ss += '\n'
        return ss



def other_exchange():

    usd2other = request_exchange_other_api1()
    other2usd = request_exchange_other_api2()
    ss = ''
    if usd2other:
        for item in usd2other.keys():
            ss += 'USD' + '  -> '+item.split('USD')[1] +'   '+ str(round(usd2other[item]['rate'],3)) + '\n'
    if other2usd:
        for item in other2usd.keys():
            ss += 'USD' + '  -> '+item.split('USD')[0] +'    '+ str(round(1 / other2usd[item]['rate'], 3)) + '\n'
    return ss
print request_exchange_other_api2()
#print get_asset_with_current_exchange()
#print view_text_price(1383)
#print result_to_str_other(1383)

#print other_exchange()