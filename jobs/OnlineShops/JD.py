#coding:utf-8
'''
京东
'''
import requests
from urllib.parse import quote,urlencode
from func.date.dateutils import dateutilsclass
from bs4 import BeautifulSoup as bs
from func.mymysql import mymysqlclass,myconfig
import time
from datetime import datetime
from itertools import product

class JDClass(object):

    def __init__(self):
        pass

    def login(self):
        def checkLogin():
            url = "https://home.jd.com"
            headers = {
                ""
            }

    def spider(self):
        pass

if __name__ == "__main__":

    a = JDClass()