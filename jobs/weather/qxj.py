#coding:utf-8
import requests
from urllib.parse import quote,urlencode
from func.date.dateutils import dateutilsclass
from bs4 import BeautifulSoup as bs
from func.mymysql import mymysqlclass,myconfig

class weather():
    def __init__(self):
        self.district = None
        self.time = None
        self.ifpredict = 0
        self.rain = None
        self.temp = None
        self.humid = None
        self.wind_speed = None

    def save(self,table = "weather_hour"):
        columnsList = list()
        valueList = list()
        count = 0
        for column, value in self.__dict__.items():
            columnsList.append(column)
            valueList.append(value)
            count += 1
        # sql = "select 1 from {0} where time='{1}' and district='{2}'".format(table, self.time, self.district)
        # with mymysqlclass(myconfig) as mp:
        #     result = mp.select(sql)
        # if len(result)== 0:
        sql = "replace into {0}({1}) values({2})".format(table, ",".join(columnsList), ",".join(['%s'] * count))

        mymysqlclass(myconfig).dochange(sql,valueList)
            # else:
            # print("需要更新")

class QXJ:
    '''
    数据源湖北气象局
    '''
    url = "http://www.hbqx.gov.cn/qx_tqsk.action"

    def __init__(self):
        pass

    @staticmethod
    def hubei(date=dateutilsclass.getDay(1)):
        '''
        获取湖北地区区县级
        :param area: 
        :param date: 
        :return: 
        '''
        areas = [
            "武汉市区,蔡甸区,江夏区,黄陂区,新洲区",
            "宜昌市区,长阳县,当阳市,五峰县,兴山县,宜都市,远安县,夷陵区,枝江市,秭归县",
            "荆州市区,公安县,洪湖市,监利县,石首市,松滋市",
            "襄阳市区,襄州区,保康县,谷城县,老河口市,南漳县,宜城市,枣阳市",
            "黄石市区,大冶市,阳新县",
            "荆门市区,京山县,沙洋县,钟祥市",
            "黄冈市区,红安县,黄梅县,罗田县,麻城市,团风县,武穴市,英山县,蕲春县,浠水县",
            "十堰市区,丹江口市,房县,郧西县,郧县,竹山县,竹溪县",
            "恩施市区,巴东县,鹤峰县,建始县,来凤县,利川市,咸丰县,宣恩县",
            "潜江市区",
            "天门市",
            "仙桃市区",
            "随州市区,广水市",
            "咸宁市区,赤壁市,崇阳县,嘉鱼县,通城县,通山县",
            "孝感市区,安陆市,大悟县,汉川市,孝昌县,应城市,云梦县",
            "鄂州市区",
            "神农架林区"
        ]
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        def do(distinct,date):
            data = {
                "StationName": quote(distinct, encoding="gbk"),
                "datatime": date,
            }
            resp = requests.post(QXJ.url,data=data,headers = headers).text
            soup = bs(resp,"html.parser")
            soup = soup.find_all("table",attrs={"class":"show_tab"})[0]
            datas = soup.find_all("tr")[1:]
            if len(datas) ==0:
                raise Exception("no data")
            line = weather()
            line.district = distinct
            for data in datas:
                tds = data.find_all("td")
                line.time =  tds[0].text
                line.temp = tds[1].text
                line.humid = tds[2].text
                line.rain = tds[3].text
                line.wind_speed = tds[4].text
                line.save()

        for area in areas:
            for distinct in area.split(","):
                do(distinct,date)

    @staticmethod
    def guangxi():
        url = "http://flash.weather.com.cn/wmaps/xml/nanning.xml?81203"
        resp = requests.get(url)
        resp.encoding = "utf8"
        print(resp.text)

    @staticmethod
    def hunan():
        url = "http://www.hnqx.gov.cn/hunan/cityhunan/query?token=inner&type=1&sbtType=10"
        resp = requests.get(url)
        resp.encoding = "utf8"
        print(resp.json())

if __name__ == "__main__":
    # QXJ.area("黄陂区","2018-01-01")
    for n in reversed(range(1,100)):
        date = str(dateutilsclass.getDay(n))[:10]
        print(date)
        try:
            QXJ.hubei(date)
        except Exception as e:
            print(e)
    # #%BB % C6 % DA % E9 % C7 % F8

