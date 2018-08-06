from pyhive import hive
import configparser
import os
config = configparser.ConfigParser()
project_dir = os.path.dirname(os.path.dirname(__file__))
config.read(project_dir+"/config.ini")
myconf = config.items("hive")
host = config["hive"]["host"]
config = dict()
for key,val in myconf:
    config[key] = val if key!="port" else int(val)


class myhiveclass():
    def __init__(self,config):
        self.con = hive.Connection(**config)

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
                cur.executemany(sql,vals)
            self.con.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def select(self,sql):
        with self.con.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

if __name__ == "__main__":
    with myhiveclass(config) as hive:
        for result in hive.select("select * from dw.bic_stores where city ='南宁' limit 10"):
            print(result)