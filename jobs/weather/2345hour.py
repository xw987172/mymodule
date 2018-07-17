#coding:utf-8
'''
2345小时级预测数据
'''
import sys
sys.path.append("/home/hdfs/mymodule/")
import requests
from urllib.parse import quote,urlencode
from func.date.dateutils import dateutilsclass
from bs4 import BeautifulSoup as bs
from func.mymysql import mymysqlclass,myconfig
import time
from datetime import datetime
from itertools import product
class WeatherItem:
    def __init__(self):
        self.area = None
        self.time = None
        self.city = None
        self.temp = None
        self.ifpredict =2
        self.wstatus = None
        self.aqi = None

    def save(self,table = "weather_hour_f"):
        columnsList = list()
        valueList = list()
        count = 0
        for column, value in self.__dict__.items():
            columnsList.append(column)
            valueList.append(value)
            count += 1
        # sql = "select 1 from {0} where time='{1}' and area ='{2}' and ifpredict={3}".format(table, self.time, self.area,
        #                                                                                     self.ifpredict)
        sql = "replace into {0}({1}) values({2})".format(table, ",".join(columnsList), ",".join(['%s'] * count))
        with mymysqlclass(myconfig) as my:
            my.dochange(sql, valueList)


class spider2345:

    def __init__(self):
        self.url = "http://tianqi.2345.com/t/wea_hour_js/{0}{1}.js?{2}"
        self.header = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        self.types = [
            "", # 当天的小时预测
            "_1", # 明天的
            "_2"  # 后天的
        ]


        whareacodes = {"武汉":57494,"黄陂区": 70313,"蔡甸区": 60012,"新洲区": 60951,"东西湖区": 71373,"江汉区": 71828,"硚口区": 71829,"汉阳区": 71830,"武昌区": 71831,"青山区": 71832,"洪山区": 71833,"汉南区": 71834,"江夏区": 70939,"江岸区": 71827,}

        nnareacodes = {'南宁': '59431','邕宁': '60022','横县': '60661','隆安': '61001','马山': '70120','上林': '60993','武鸣': '60023','宾阳': '70105','兴宁': '72063','青秀': '72064','江南': '72065','西乡塘': '72066','良庆': '72067'}

        csareacodes = {'长沙': '57687', '宁乡': '70343', '浏阳': '60388', '湘江新区': '71101', '望城': '71405', '长沙县': '71438', '芙蓉': '71950', '天心': '71951', '岳麓': '71952', '开福': '71953', '雨花': '71954'}

        self.areas = [whareacodes,nnareacodes,csareacodes]

    def spider(self):
        args = product(self.areas,self.types)
        for area,type in args:
            for k,v in area.items():
                try:
                    self.work(k,v,type)
                except:
                    with open("2345hour_err","a") as fp:
                        fp.write(k+","+type+","+str(datetime.now())+"\n")



    def work(self,area=None,areacode = 71831,type=None):
        ts = 1000*(time.time())
        url = self.url.format(areacode,type,ts)
        resp = requests.get(url,headers = self.header)
        resp.encoding = "gbk"
        data = eval(resp.text.split(";")[0].split("=")[1])
        line = WeatherItem()
        line.area = areacode
        line.city = area
        for dt in data:
            print(dt)
            tm = str(dateutilsclass.numToTime(int(dt.get("day")))).split()[0]
            hourn = dt.get("hour")
            line.temp = dt.get("temp")
            line.time = tm+" "+hourn+":00:00"
            line.wstatus = dt.get("tq")
            try:
                line.aqi = dt.get("aqiInfo")+","+dt.get("aqiLevel")
            except:
                pass
            line.save()



    def tmp(self,url):
        '''
        获取省份城市的区县编号
        湖南长沙：http://tianqi.2345.com/hunan_dz/23.htm
        广西南宁：http://tianqi.2345.com/guangxi_dz/16.htm
        :param url: 
        :return: 
        '''
        result = dict()
        resp = requests.get(url)
        from bs4 import BeautifulSoup as bs
        soup = bs(resp.text,"html.parser")
        content = soup.find_all("div",attrs={"class":"citychk"})[0]
        dls = content.find_all("dl")[0]
        dds = dls.find_all("dd")[0].find_all("a")
        for dd in dds:
            print(dd)
            href = dd.get("href")
            mt = "".join(list(filter(str.isdigit, href)))
            area = dd.text
            result[str(area)]=mt
        print(result)

if __name__ == "__main__":
    # spider2345().tmp("http://tianqi.2345.com/hunan_dz/23.htm")
    spider2345().spider()