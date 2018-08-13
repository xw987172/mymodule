import configparser,pymysql
import os
config = configparser.ConfigParser()
project_dir = os.path.dirname(os.path.dirname(__file__))
config.read(project_dir+"/config.ini")
myconf = config.items("mysql")
myconfig = dict()
for key,val in myconf:
    myconfig[key] = val if key!="port" else int(val)


class mymysqlclass():
    def __init__(self,config):
        self.con = pymysql.connect(**config)

    def __enter__(self):
        return self

    def insertmany(self,sql,vals):
        cur = self.con.cursor()
        try:
            cur.executemany(sql,vals)
            self.con.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def dochange(self,sql,vals=None):
        cur = self.con.cursor()
        try:
            if vals==None:
                cur.execute(sql)
            else:
                cur.executemany(sql, vals)
            self.con.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def select(self,sql):
        cur = self.con.cursor()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

if __name__=="__main__":
    data = [['2018-08-03', 117362, 4527.56787109375, 'sales_predict', 'xgboost'], ['2018-08-03', 117363, 6986.17431640625, 'sales_predict', 'xgboost']]
    # import pandas as pd
    sql = "insert into machine_learning(date,store_code,predict_sales,model_group,model) values(%s,%s,%s,%s,%s)"
    with mymysqlclass(myconfig) as mysql:
        mysql.dochange(sql,data)
        # result = mysql.select("select shopid,name from today limit 10")
    # data = pd.DataFrame(list(result),columns=["id","name"])
    # print(data["id"])