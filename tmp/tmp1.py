# coding:utf8

from func.mymysql import mymysqlclass,myconfig
from func.myhive import myhiveclass,config



with myhiveclass(config) as hive:
    data = hive.select("""
      select store_code,date,sales_amt from dw.bic_stores where store_code in
      (117031,117129,117130)
      and date>"2018-07-03"
    """)

for store_code,date,sales in data:
    sql = "update spider.single_sales_predict_tomo set real_sale={0} where store_code={1} and predict_date='{2}' and date ='{3}'".format(sales,store_code,date,'2018-08-02')

    with mymysqlclass(myconfig) as my:
        my.dochange(sql)