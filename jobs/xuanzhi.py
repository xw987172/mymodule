#coding:utf8

import requests,time

pre_login_url="http://xuanzhi.today36524.com/login.html#/"


class xuanzhiClass:
	def __init__(self):
		pass

	def spider(self):
		print("I'm in spider function.")
		n = 100
		while(n>0):
			print("spider "+str(n))
			n-=1
			time.sleep(0.1)
		return "spider over"

	def addShop(self):
		'''向选址平台添加today门店（按坐标方式）'''

		url = "http://xuanzhi.today36524.com"

		print(url)
		n =100
		while(n>0):
			print("addShop "+str(n))
			n-=1
			time.sleep(0.1)

		return "addShop over"
