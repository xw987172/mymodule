# coding =utf8
from func.myhive import myhiveclass,config
from func.mymysql import mymysqlclass,myconfig

def getData():
    sql = "select shopid,radius,date,num1,num2,num3 from ods.population where date='2018-05-17'"
    data = myhiveclass(config).select(sql)
    return data

def insertsql(data):
    for dt in data:
        sql = "insert into population(shopid,radius,date,num1,num2,num3) values(%s,%s,'%s',%s,%s,%s)" %(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5])
        if "None" in sql:
            sql = sql.replace("None","null")
        mymysqlclass(myconfig).dochange(sql)

# insertsql(getData())
import sys,time
for i in range(1000):
    sys.stdout.write(str(i)+"\r\n")
    sys.stdout.flush()
    time.sleep(0.1)