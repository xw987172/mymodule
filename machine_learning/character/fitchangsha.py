# coding: utf8
'''
双色球的预测模型
'''
import random
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
import pandas as pd
import pickle
import datetime,time
from func.myhive import myhiveclass,config
from func.mymath import mymathclass
from func.mymysql import mymysqlclass,myconfig
from sklearn.ensemble import RandomForestRegressor # 随机森林回归模型
from sklearn.linear_model import LinearRegression
from func.date.dateutils import dateutilsclass
'''
forest = RandomForestRegressor(
    n_estimators =1000,
    criterion = 'mse',
    random_state =1,
    n_jobs =-1,
)
forest.fit(X_train,Y_train)
'''

class createModel():
    '''
    创建线性回归模型，根据武汉的数据预测长沙、南宁的数据
    '''
    def __init__(self):
        self.data = self.checkRegDegree() # 训练集
        self.lineReg = self.Model() # 回归模型


    def checkRegDegree(self,data=None):
        origin = np.array([[1,1,1,1,2],[2,1,1,1,3],[3,1,4,2,5],[4,3,36,6,32],[5,4,4,2,10]])
        data = pd.DataFrame(origin,columns=['TV', 'Radio', 'Newspaper','N2','Sales'])
        return data
        # print(data)
        # import seaborn as sns
        # import matplotlib.pyplot as plt
        # sns.pairplot(data, x_vars=['TV', 'Radio', 'Newspaper'], y_vars='Sales', size=7, aspect=0.8,kind="reg")
        # plt.show()  # 注意必须加上这一句，否则无法显示。

    def Model(self):
        '''
        获取线性回归模型
        :return: 
        '''
        from sklearn.linear_model import LinearRegression
        linreg = LinearRegression()
        model = linreg.fit(self.data[['TV', 'Radio', 'Newspaper','N2']], self.data[['Sales']])
        # print(model)
        # print(linreg.intercept_)
        # print(linreg.coef_)
        pres = linreg.predict(self.data[['TV', 'Radio', 'Newspaper','N2']])
        missDg = 0
        for p,t in zip(pres,self.data[['Sales']].values):
            missDg += (round(p[0],2)-t[0])**2
        missErr = np.sqrt(missDg/len(pres))
        print("均方根误差：",missErr)
        return linreg

    def predict(self,data=None):
        '''
        预测数据
        :param data: 
        :return: 
        '''
        data = pd.DataFrame(np.array([[4,7,64,8]]),columns=['TV', 'Radio', 'Newspaper','N2'])
        print(self.lineReg.predict(data))

class fitChangsha():
    def __init__(self):
        self.weeks = [0,1,2,3,4,5,6]
        self.wstatus = ["多云","阴","小雨","晴","中雨","阵雨","霾","雷阵雨","大雨","大到暴雨","暴雨","中到大雨","小雪","雨夹雪","扬沙","小到中雨","特大暴雨","中雪","大雪","暂无","雾"]
        self.city = ["武汉","南宁","长沙"]
        self.ages = ["既存店A","既存店B","新既店","新开店"]
        self.types = ["直营","加盟"]
        self.dudaos = ["丁丹","任紫均","伍厚旺","余恒","余飞","党浩东","农才勇","刘全勇","刘潇","刘苗","刘雪松","吕婷婷",
                       "周商","周斌","周昕","宗媛","张春银","张贝","张远安","彭涛","徐钊","晏慧","曹凤","未知","朱继","李全",
                       "李博斐","李文贵","李智","杨博文","杨柳","杨飞虹","林琳","梁子菁","汤兆祥","汪霁雯","王帆","王想","王玉平",
                       "王瑶","王鑫","程振东","程晶","胡亢","胡晓玲","莫建东","葛登科","蓬琴","谢睿","赖莉清",
                       "郑思远","郭秀平","金雪娇","闫攀","陈俊","陈凯","陈萍","骆晶","黄健明","黄凡","黄家盛","黄海兰","龙阳"]

    def staticForest(self):
        forest = RandomForestRegressor(
            n_estimators=1000,
            criterion='mse',
            random_state=1,
            n_jobs=-1
        )
        data = list()
        result = list()
        for i in range(1,10):
            for j in range(1,10):
                for k in range(1,10):
                    data.append([i,j,k])
                    result.append(0.5*(i**2)+j+(k-1)**3)
        data.append([10,20,30])
        result.append(24459)
        X_train = pd.DataFrame(np.array(data))
        Y_train = pd.Series(result)
        print(X_train.head(10))
        print(Y_train.head(10))
        forest.fit(X_train,Y_train)
        print(forest.predict(pd.DataFrame(np.array([[20,20,30],[2,1,3]]))))

    def getTrain(self,shopid,date=None):
        sql = "select store_code,date,sales_amt from dw.bic_stores where store_code in ({0}) and date>='2018-04-01'".format(shopid)
        data  = myhiveclass(config).select(sql)
        return data

    def getTrue(self,shopid,date):
        sql = "select num1 from ods.population where shopid ={0} and date='{1}'".format(shopid,date)
        data = myhiveclass(config).select(sql)
        return data[0][0]

    def getData(self,shopid,date):
        """
        1、获取MySQL表的周边数据
        2、获取hive表的日商数据
        :return:
        """
        # 首先添加城市因子，这里都是武汉
        # 添加店龄，类型

        result =[]
        week = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(date)[:10], "%Y-%m-%d"))).weekday()
        for wk in self.weeks:
            if week==wk:
                result.append(1)
            else:
                result.append(0)
        sql = "select city,store_age,store_type from dw.dim_stores_info where store_code={0}".format(shopid)
        data = myhiveclass(config).select(sql)
        city,age,type = data[0]
        # 城市 one-hot
        if city=="未知":
            city="武汉"
        for ct in self.city:
            if city == ct:
                result.append(1)
            else:
                result.append(0)

        # 店龄 one-hot
        for ag in self.ages:
            if age == ag:
                result.append(1)
            else:
                result.append(0)
        # 店铺类型 one-hot
        for tp in self.types:
            if type == tp:
                result.append(1)
            else:
                result.append(0)
        # 督导 one-hot
        # for sup in self.dudaos:
        #     if super == sup:
        #         result.append(1)
        #     else:
        #         result.append(0)
        # 后面是和日期相关的指标值
        sql = "select wstatus1 from rpt.weather_day where city='{0}' and date='{1}' and ifpredict=0".format(city,date)
        data = myhiveclass(config).select(sql)
        # 天气状况 one-hot
        for ws in self.wstatus:
            if data[0][0] == ws:
                result.append(1)
            else:
                result.append(0)

        sql = "select sales_amt from bic_stores where store_code ={0} and date = '{1}'".format(shopid, date)
        data = myhiveclass(config).select(sql)
        result.append(data[0][0])
        '''
        # 周边数据
        # population 活动人口、居住人口、办公人口
        # sql = "select num1,num2,num3 from ods.population where shopid={0} and date='{1}' and radius=0.5".format(shopid,date)
        # data = myhiveclass(config).select(sql)
        # for i in range(3):
        #     result.append(data[0][i])
        #
        # # people 各种人群画像
        # standards = [
        #                 ("性别","男"),
        #                 ("性别","女"),
        #                 ("年龄段","25-34"),
        #                 ("年龄段","19-24"),
        #                 ("年龄段","35-44"),
        #                 ("年龄段","45-54"),
        #                 ("年龄段","0-18"),
        #                 ("年龄段",">=55"),
        #                 ("职业","服务人员"),
        #                 ("职业","公司职员"),
        #                 ("职业","学生"),
        #                 ("职业","医疗人员"),
        #                 ("职业","公务员"),
        #                 ("职业","教职工"),
        #                 ("职业","家庭主妇"),
        #                 ("职业","出租车司机"),
        #                 ("职业","科研人员"),
        #                 ("职业","货车司机"),
        #                 ("职业","快递员"),
        #                 ("是否有小孩","否"),
        #                 ("是否有小孩","是"),
        #                 ("资产等级","中产"),
        #                 ("资产等级","工薪一族"),
        #                 ("资产等级","富豪"),
        #                 ("资产等级","超级富豪"),
        #                 ("消费能力","中等"),
        #                 ("消费能力","较弱"),
        #                 ("消费能力","较强"),
        #                 ("消费能力","弱"),
        #                 ("消费能力","强")
        #              ]
        # for standard,type in standards:
        #     sql = "select val from ods.people where shopid={0} and date='{1}' and radius=0.5 and standard='{2}' and type='{3}'".format(shopid,date,standard,type)
        #     data = myhiveclass(config).select(sql)
        #     if len(data)==0:
        #         result.append(2000)
        #     else:
        #         result.append(data[0][0])
        '''
        return result

    def getY(self,shopid,date):
        # sql = "select sales_amt from bic_stores where store_code ={0} and date = '{1}'".format(shop,date)
        # data = myhiveclass(config).select(sql)
        # return data[0][0]
        sql = "select num1,num2,num3 from ods.population where shopid={0} and date='{1}' and radius=0.5".format(shopid,date)
        data = myhiveclass(config).select(sql)
        return data[0][0]



if __name__=="__main__":
    # a =createModel()
    # a.checkRegDegree()
    # a.predict()
    # fitChangsha().staticForest()
    a = fitChangsha()
    trains = list()
    Y_trains = list()
    sql = "select shopid from today where city='武汉' and shopid not in (117045,117202,117030,117035,117037,117122,117235,117206,117180,117287, 117373,117375,117368,117372,117360)"

    shops = mymysqlclass(myconfig).select(sql)
    sql = "select store_code from dw.dim_stores_info where city in ('南宁','长沙')"
    other_shops = myhiveclass(config).select(sql)
    days = list(map(dateutilsclass.getDay,reversed(list(range(3,30)))))
    # max_steps = len(shops)*len(list(days))
    whdata =  dict()
    whdates = dict()
    otdata = dict()
    otdates = dict()
    # for shop,date in product(shops,list(days)):
    #     shop = shop[0]
    #     date = str(date)[:10]
    #     if str(shop)+","+str(date)[:10] in whdata:
    #         continue
    #     try:
    #         val = a.getTrain(shop,date)
    #         whdata[str(shop)+","+str(date)[:10]] = val
    #     except Exception as e:
    #         print(shop,date,e)
    strsp = ""
    for shop in shops:
        shop = shop[0]
        strsp +=str(shop)+","
    strsp = strsp[:-1]
    data = a.getTrain(strsp)
    for shop,date,sale in data:
        if str(shop) in whdates.keys():
            whdates[str(shop)].append(str(date))
        else:
            whdates[str(shop)] = []
            whdates[str(shop)] = [str(date)]
        whdata[str(shop)+","+str(date)] = sale

    strsp = ""
    for shop in other_shops:
        shop = shop[0]
        strsp += str(shop) + ","
    strsp = strsp[:-1]
    data = a.getTrain(strsp)
    for shop,date,sale in data:
        if str(shop) in otdates.keys():
            otdates[str(shop)].append(str(date))
        else:
            otdates[str(shop)] = [str(date)]
        otdata[str(shop)+","+str(date)] = sale

    for sp in other_shops:
        sp = sp[0]
        dates = otdates.get(str(sp))
        vectorA = list()
        vectorB = list()
        common_days = list()
        try:
            for date in dates:
                i = 0
                lenghth = len(shops)
                for op in shops:
                    op = op[0]
                    whdate = whdates.get(str(op))
                    if date in whdate:
                        i+= 1
                if i == lenghth:
                    common_days.append(date)
        except:
            pass
        for op in shops:
            op = op[0]
            try:
                for dt in common_days:
                    vectorA.append(otdata.get(str(sp)+","+dt))
                    vectorB.append(whdata.get(str(op) + "," + dt))


                if len(vectorB)==0 or len(vectorA)==0:
                    continue
                try:
                    val =  mymathclass.ouDistance(vectorA,vectorB)
                    if val ==None:
                        val = 'null'
                    sql = "replace into distance30(cfrom,tend,val) values(%s,%s,%s)" %(sp,op,val)
                    try:
                        mymysqlclass(myconfig).dochange(sql)
                    except:
                        pass
                    else:
                        vectorA = list()
                        vectorB = list()
                except:
                    print(vectorA)
                    print(vectorB)
            except:
                pass
