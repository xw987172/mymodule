# coding:utf-8
import requests
import sys
sys.path.append("../../")
from func.mymysql import mymysqlclass,myconfig
from datetime import datetime
'''
中国天气网
'''

def GetGeo():
    '''
    获取shopid,location映射关系
    :return: 
    '''
    sql = "select shopid,location from today where location is not null"
    with mymysqlclass(myconfig) as my:
        result = my.select(sql)
    return result

class WeatherItems:

    def __init__(self):
        self.shopid = None
        self.location = None
        self.time = None
        self.wstatus = None
        self.wcode = None
        self.temp = None
        self.humid = None
        self.wd = None
        self.wr = None
        self.ifpredict = 0
    def save(self):
        pass

# 114.343466,30.554921
targets = GetGeo()
tm = str(datetime.now())[:16]+":00"
print(tm)
url = "http://forecast.weather.com.cn/town/api/v1/sk?lat={0}&lng={1}"
results = []
for shop,location in targets:
    lng,lat = location.split(",")
    url0 = url.format(lat,lng)
    resp = requests.get(url0).json()

    data = [shop,location,tm,resp.get("weather"),resp.get("weathercode"),resp.get("temp"),resp.get("humidity"),resp.get("WD"),resp.get("WS")]
    results.append(tuple(data))

insertsql = "insert into weather_hour_c(shopid,location,`time`,wstatus,wcode,temp,humid,wd,wr) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
with mymysqlclass(myconfig) as my:
    my.insertmany(insertsql,results)


