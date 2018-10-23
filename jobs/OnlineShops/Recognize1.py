#coding=utf-8
import sys
import pymysql
import requests
import json,time,datetime
import hashlib

conn=pymysql.connect(
    host='192.168.71.111',
    port=3375,
    user='dw',
    passwd='cyOp5O^7XYN&iu2L',
    db='dw',
    charset='utf8'
    )

def postData(store_code,skuList):
    t = int(1000 * time.time())
    #url = "http://openapi.sandbox7.today.cn/test.htm"
    url="http://gateway.sandbox7.today.cn/api/com.today.api.purchase.service.OpenPurchaseService/1.0.0/addOrderAgent4Fresh/921cb9a4d06d114e5921bdb2a1e1547d"
    APIKey="921cb9a4d06d114e5921bdb2a1e1547d"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data1 = {
        "body": {
            "request": {
                "storeId": store_code,
                "skuList":skuList
            }
        }
    }
    str1 = json.dumps(data1)
    md = hashlib.md5()
    toSecret = APIKey + str(t) + "8S9csk2PUAgU" + str1
    md.update(toSecret.encode())
    res=md.hexdigest()
    postdata = "timestamp={0}&secret2={1}&parameter=".format(t,res) + str1
    print(postdata)
    print(url)
    resp = requests.post(url,headers=headers ,data=postdata)
    print(resp.text)
    resp = resp.json()
    if resp.get("status") == 0:
        if resp.get("responseCode")=="Err-Purchase-101":
            postData(store_code, skuList)
        else:
            with open("./order.log","a") as fp:
                print(resp.get("responseMsg"))
                fp.write(str(datetime.datetime.now())+"\t"+str(store_code)+resp.get("responseMsg").encode("utf-8"))
            return False
    elif resp.get("status") == 1 and "callOrderId" in resp.get("success").keys():
        print(str(datetime.datetime.now())+"\t"+str(store_code)+"\t"+"叫货成功")
        return True
    elif resp.get("status") == 1 and "callOrderId" not in resp.get("success").keys():
        print(str(datetime.datetime.now()) + "\t" + str(store_code) + "\t" +str(resp))
        return True
    else:
        print(resp)
        return False


#代订日期
today=datetime.date.today()
orderDate=today+datetime.timedelta(days=-1)

query_sql_1="""
SELECT  store_code,date
from report.fresh_batchorder_goods
where date = '{0}'
group by store_code,date
""".format(orderDate)

cur = conn.cursor()
cur.execute(query_sql_1)
data=cur.fetchall()
storeData = data

for store_code,date in storeData:
    skuList = list()
    cur = conn.cursor()
    sql = """
    select goods_id,suggestordernum from report.fresh_batchorder_goods where store_code = {0} and date = '{1}'
    """.format(store_code,date)
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    orderData = data
    for goods_id,num in orderData:
        skuList.append({
            "skuNo":goods_id,
            "agentMultiple":num,
            ##"checkResult":"sampleDataString"
        })
    try:
        res = postData(store_code,skuList)
    except:
        pass
    else:
        if res:
            cur = conn.cursor()
            sql = """
                update report.fresh_batchorder_goods set uploadsucceed=1 where store_code = {0} and date = '{1}'
                """.format(store_code,date)
            cur.execute(sql)
            conn.commit()

conn.close()
