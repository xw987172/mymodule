import sys
from func.mymath import mymathclass
from func.myhive import myhiveclass,config
from func.mymysql import mymysqlclass, myconfig
from func.date.dateutils import dateutilsclass
import xlwt
class ab:
    shopday = {}
    whshopday = {}
    def ac(self):

        # 由2组字典组成
        # #南宁、长沙的所有门店的日商向量数据
        dict1 = {
            '长沙1':[1,2,3,4,5,6,7],
            '长沙2':[7,6,4,5,3,2,1],
            '南宁1':[2,3,5,1,3,5,2],
        }
        dict2 = {
        # 武汉的所有门店的
            '武汉1':[4,5,6,7,8,9,10],
            '武汉2':[2,1,2,4,5,8,10],
        }
        result = [key+"-"+key2+":"+str(mymathclass.cosLike(val,val2)) for key,val in dict1.items() for key2,val2 in dict2.items()]
        return result

    @staticmethod
    def _getData(store_code,whstore_code):
        '''
        得到南宁和长沙的店铺与武汉的店铺的日商的余弦值
        :param store_code: 
        :param whstore_code: 
        :return: (store_code, whstore_code, 余弦值,)
        '''
        if str(store_code) in ab.shopday:
            dates = ab.shopday.get(str(store_code))
        else:
            with myhiveclass(config) as myhive:
                date = myhive.select("select substring(sale_date,1,10) from bic_stores where store_code=%s and date>='2018-04-01'" %(store_code))
            tmp = ['"'+x[0]+'"' for x in date]
            ab.shopday[str(store_code)] = set(tmp)
            dates = set(tmp)

        if str(store_code) in ab.whshopday:
            whdates = ab.whshopday.get(str(store_code))
        else:
            with myhiveclass(config) as myhive:
                date = myhive.select("select substring(date,1,10) from bic_stores where store_code=%s and date>='2018-04-01'" %(whstore_code))
            tmp = ['"'+x[0]+'"' for x in date]
            ab.whshopday[str(whstore_code)] = set(tmp)
            whdates = set(tmp)

        common_day = dates & whdates
        if len(common_day)>10:
            common_day = ",".join(common_day)
            with myhiveclass(config) as myhive:
                vals1 = myhive.select("select concat_ws(',',cast(sales_amt as string)) from bic_stores where store_code =%s and date in (%s)" %(whstore_code,common_day))
                vals1 = [x[0] for x in vals1]
                vals2 = myhive.select(
                    "select concat_ws(',',cast(sales_amt as string)) from bic_stores where store_code =%s and date in (%s)" % (
                    store_code, common_day))
                vals2 = [x[0] for x in vals2]
                mr = mymathclass.cosLike(vals1,vals2)
                print(store_code,whstore_code,mr)
            return (store_code,whstore_code,mr,)
        else:
            return (store_code,whstore_code,"null")

    def work(self):
        '''
        执行函数
        :return: 
        '''
        dict11,dict12 = [self.getdata1(city) for city in ['"武汉"',("南宁","长沙")]]
        print("开始进度条...")
        total = len(dict12)*len(dict11)
        print("总计：",total)
        result = [self._getData(store_code,whstore_code) for store_code in dict12 for whstore_code in dict11]
        wb = xlwt.Workbook()
        st = wb.add_sheet("sheet")
        for i,s in enumerate(result):
            st.write(i,0,str(s[0]))
            st.write(i,1,str(s[1]))
            st.write(i,2,str(s[2]))
        wb.save("coslike2.xls")

    @staticmethod
    def getdata1(city):
        '''
        获取不同城市下的所有店铺
        :param city: 
        :return: 
        '''
        sql = "select distinct store_code from dw.bic_stores where city in (%s)" %(str(city)) if isinstance(city,str) else "select distinct store_code from dw.bic_stores where city in %s and store_code>116012" %(str(city))
        with myhiveclass(config) as myhive:
            result = myhive.select(sql)
        return [store_code[0] for store_code in result]

    def tmp(self):
        sql = "select id from population_hour"
        data = mymysqlclass(myconfig).select(sql)
        for id in data:
            ids = mymysqlclass(myconfig).select("select id, shopid, date, radius, posi, num1, num2, num3, createtime from population_hour where id = %s" %(id))
            id, shopid, date, radius, posi, num1, num2, num3, createtime = ids[0]
            try:
                sql = "insert into population_hour_bak(id,shopid,date,radius,posi,num1,num2,num3,createtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                mymysqlclass(myconfig).dochange(sql,(id, shopid, date, radius, posi, num1, num2, num3, createtime))
            except:
                print(ids)

    def dosql(self):
        sql = "select distinct cfrom from corlike"
        shops = mymysqlclass(myconfig).select(sql)
        for shop in shops:
            sql = "select tend,cor/b.corsum from corlike,(select sum(cor) as corsum from corlike where cfrom=%s) as b where cfrom=%s" %(shop[0],shop[0])
            data = mymysqlclass(myconfig).select(sql)
            for dt in [dateutilsclass.getDay(n) for n in range(3,4)]:
                dt = str(dt)
                num1,num2,num3 = [0]*3
                for radius in [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
                    for sid,rate in data:
                        sql = "select {0}*num1,{0}*num2,{0}*num3 from population where shopid ={1} and date='{2}' and radius={3}".format(rate,sid,dt[:10],radius)
                        tmp = mymysqlclass(myconfig).select(sql)
                        if len(tmp)==1:
                            num1+=tmp[0][0]
                            num2+=tmp[0][1]
                            num3+=tmp[0][2]
                    sql = "insert into population_pre(shopid,date,num1,num2,num3,radius) values(%s,%s,%s,%s,%s,%s)"
                    print(sql)
                    print(shop,dt[:10],num1,num2,num3,radius)
                    mymysqlclass(myconfig).dochange(sql,(shop[0],dt[:10],num1,num2,num3,radius))

    def dosql_people(self):
        sql = "select distinct cfrom from corlike"
        shops = mymysqlclass(myconfig).select(sql)
        for shop in shops:
            sql = "select tend,cor/b.corsum from corlike,(select sum(cor) as corsum from corlike where cfrom=%s) as b where cfrom=%s" %(shop[0],shop[0])
            data = mymysqlclass(myconfig).select(sql)
            for dt in [dateutilsclass.getDay(n) for n in range(3,4)]:
                dt = str(dt)
                val = 0
                for radius in [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
                    for standard,type in [("性别","男"),
                                            ("性别","女"),
                                            ("年龄段","25-34"),
                                            ("年龄段","19-24"),
                                            ("年龄段","35-44"),
                                            ("年龄段","45-54"),
                                            ("年龄段",">=55"),
                                            ("年龄段","0-18"),
                                            ("职业","服务人员"),
                                            ("职业","公司职员"),
                                            ("职业","学生"),
                                            ("职业","医疗人员"),
                                            ("职业","公务员"),
                                            ("职业","教职工"),
                                            ("职业","家庭主妇"),
                                            ("职业","出租车司机"),
                                            ("职业","科研人员"),
                                            ("职业","货车司机"),
                                            ("职业","快递员"),
                                            ("是否有小孩","是"),
                                            ("是否有小孩","否"),
                                            ("资产等级","中产"),
                                            ("资产等级","工薪一族"),
                                            ("资产等级","富豪"),
                                            ("资产等级","超级富豪"),
                                            ("消费能力","中等"),
                                            ("消费能力","较弱"),
                                            ("消费能力","较强"),
                                            ("消费能力","弱"),
                                            ("消费能力","强")]:
                        for sid,rate in data:
                            sql = "select {0}*val from people where shopid ={1} and date='{2}' and radius={3} and standard='{4}' and type='{5}'".format(rate,sid,dt[:10],radius,standard,type)
                            tmp = mymysqlclass(myconfig).select(sql)
                            if len(tmp)==1:
                                val+=tmp[0][0]
                        sql = "insert into pre_people(shopid,date,standard,type,val,radius) values(%s,%s,%s,%s,%s,%s)"
                        print(sql)
                        print(shop,dt[:10],standard,type,val,radius)
                        mymysqlclass(myconfig).dochange(sql,(shop[0],dt[:10],standard,type,val,radius))

    def dosql_surround(self):
        sql = "select distinct cfrom from corlike"
        shops = mymysqlclass(myconfig).select(sql)
        types = mymysqlclass(myconfig).select("select distinct type1,type2 from surround where date='2018-06-20'")
        for shop in shops:
            sql = "select tend,cor/b.corsum from corlike,(select sum(cor) as corsum from corlike where cfrom=%s) as b where cfrom=%s" % (
            shop[0], shop[0])
            data = mymysqlclass(myconfig).select(sql)
            for dt in [dateutilsclass.getDay(n) for n in range(3, 4)]:
                dt = str(dt)
                val = 0
                for standard, type in types:
                    for sid, rate in data:
                        sql = "select {0}*count(1) from surround where shopid ={1} and date='{2}' and type1='{3}' and type2='{4}'  and distance<=500".format(
                            rate, sid, dt[:10], standard, type)
                        tmp = mymysqlclass(myconfig).select(sql)
                        if len(tmp) == 1:
                            val += tmp[0][0]
                    sql = "insert into pre_surround(shopid,date,type1,type2,num) values(%s,%s,%s,%s,%s)"
                    print(sql)
                    print(shop, dt[:10], standard, type, val)
                    mymysqlclass(myconfig).dochange(sql, (shop[0], dt[:10], standard, type, val))

if __name__ == "__main__":
    # print(ab().work())
    ab().dosql()
    # ab().dosql_people()
    ab().dosql_surround()