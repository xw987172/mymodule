import pyhs2
import configparser
config = configparser.ConfigParser()
config.read("../config.ini")
myconf = config.items("hive")
config = dict()
for key,val in myconf:
    config[key] = val if key!="port" else int(val)


class myhiveclass():
    def __init__(self,config):
        self.con = pyhs2.connect(**config)

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
                cur.execute(sql, vals)
            else:
                cur.execute(sql)
            self.con.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def select(self,sql):
        with self.con.cursor() as cur:
            cur.execute(sql)
            return cur.fetch()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

if __name__ == "__main__":
    with myhiveclass(config) as hive:
        for result in hive.select("select * from bic_stores where city ='南宁' limit 10"):
            print(result)