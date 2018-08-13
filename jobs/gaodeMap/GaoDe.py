# coding:utf8
from urllib import parse as up
import requests
from func.mymysql import mymysqlclass,myconfig

class GaoDeClass(object):

    url = "https://www.amap.com/service/poiTipslite?&city={0}&geoobj=114.201412%7C30.516057%7C114.505596%7C30.658512&words={1}"

    def __init__(self):
        pass

    @classmethod
    def GetLocationByName(cls,city,word):
        url = cls.url.format(city, up.quote(word))
        resp = requests.get(url).json()
        result = dict()
        result["name"] = resp.get("data").get("tip_list")[0].get("tip").get("name")
        result["district"] = resp.get("data").get("tip_list")[0].get("tip").get("district")
        result["category"] = resp.get("data").get("tip_list")[0].get("tip").get("category")
        result["address"] = resp.get("data").get("tip_list")[0].get("tip").get("address")
        result["pointX"] = resp.get("data").get("tip_list")[0].get("tip").get("x")
        result["pointY"] = resp.get("data").get("tip_list")[0].get("tip").get("y")
        return result


if __name__== "__main__":
    with mymysqlclass(myconfig) as my:
        shops = my.select("select * from spider.today where city = '武汉'")
    for shopid,name,n1,city,location,n2,n3,district in shops:
        result = GaoDeClass().GetLocationByName(420100, "Today便利店({0})".format(name))
        print(result.get("pointX"),result.get("pointY"))
        print(shopid,name,n1,city,location,n2,n3,district)
