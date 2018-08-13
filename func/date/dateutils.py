# coding: utf8
from datetime import datetime
from datetime import timedelta
import time

class dateutilsclass():

    @staticmethod
    def getDay(n):
        '''
        获取从今天起 n天前的日期
        :param n: 
        :return: 
        '''
        return datetime.now() - timedelta(days=n)

    @staticmethod
    def getWeek(date):
        '''
        获取星期几
        :param date: 
        :return: enum(0-6)
        '''
        return datetime.fromtimestamp(time.mktime(time.strptime(date, "%Y-%m-%d"))).weekday()

    @staticmethod
    def numToTime(nInt):
        '''
        时间戳转时间
        :param nInt: 时间戳 
        :return: 
        '''
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(nInt))

if __name__=="__main__":
    print(dateutilsclass.numToTime(1526230800))
    print(dateutilsclass.numToTime(1526223600))
