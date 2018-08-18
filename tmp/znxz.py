#coding:utf-8
'''
添加智能选址平台，添加已开店
'''
from func.mymysql import mymysqlclass,myconfig
import requests
import json
url ="http://47.97.211.164/hdl/dispatch?key=store"

postData = {
    "data":{
        "latlon":"",
        "pk":"1811324832449070",
        "status":1,
        "storeInfo":'{"社区类型":"其他型","店铺类型":"加盟","店龄":"新开店"}',
        "storeName":"",
    },
    "key":"store",
    "method":"POST",
    "path":"/user/store/create",
}
postdata = '{"path":"/user/store/list","data":{"cityCode":420100,"status":1,"pk":"1811324832449070"},"key":"store","method":"GET"}'

resp = requests.post(url,data = postdata).json()
