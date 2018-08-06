# coding:utf-8
import requests
from func.mymysql import mymysqlclass,myconfig
def wuhan():
    with mymysqlclass(myconfig) as my:
        shops = my.select("select shopid,location from today WHERE city='武汉'")


    for shopid,location in shops:
        lng,lat = location.split(",")
        url = "https://restapi.amap.com/v3/geocode/regeo?key=8325164e247e15eea68b59e89200988b&s=rsv3&location={0},{1}&radius=2800&callback=&platform=JS&logversion=2.0&sdkversion=1.3&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=350D4CAC-4C25-4904-A424-8257380EAB28".format(lng,lat)

        resp = requests.get(url).json()

        district = resp.get("regeocode").get("formatted_address").split("武汉市")[1].split("区")[0]

        sql = "update today set district='{0}' where shopid={1}".format(district,shopid)

        print(sql)

def changsha():
    with mymysqlclass(myconfig) as my:
        shops = my.select('select b.store_code,b.store_address from dw.dim_stores_info_new b where  b.city="长沙"')

    for shop,store_address in shops:

        if "区" in store_address:
            a1 = store_address.split("区")[0]
            if "市" in a1:
                a1 = a1.split("市")[1]
            a1 = a1.replace("长沙","")
        sql = "update today set district='{0}' where shopid={1}".format(a1,shop)
        print(sql)

changsha()

