# coding: utf8
'''
双色球的预测模型
'''
import random
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from func.myhive import myhiveclass

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
        pass

    def getData(self):
        sql = "select distinct store_code from dw.bic_stores where city ='武汉'"
        with myhiveclass(config) as myhive:
            result = myhive.select(sql)
        return [store_code[0] for store_code in result]

if __name__=="__main__":
    a =createModel()
    a.checkRegDegree()
    a.predict()
