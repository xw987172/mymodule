#coding:utf8
import sys
sys.path.append("/home/hdfs/mymodule")
import requests,time,json
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from func.mymysql import mymysqlclass,myconfig 
class xuanzhiClass:
	preLoginUrl = "http://xuanzhi.today36524.com/login.html#/"
	def __init__(self):
		self.__author = "xw"
		self.s = requests.session()
		self.__login()

	def __login(self,user="17621064595",passwd=b"today36524"):
		def getPublicKey():
			resp = requests.get(self.__class__.preLoginUrl)
			self.e = resp.cookies["public_key"]
			return "-----BEGIN PUBLIC KEY-----\n"+self.e+"\n-----END PUBLIC KEY-----"

		def getSPasswd():
			rsakey = RSA.importKey(getPublicKey())
			cipher = Cipher_pkcs1_v1_5.new(rsakey)
			tmp = cipher.encrypt(passwd)
			return base64.b64encode(tmp)

		postdata = '{"userName":"17621064595","password":"'+str(getSPasswd(),"utf8")+'"}'
		head = {
			"Content-Type":"application/json",
			"Cookie":"public_key={0}".format(self.e)
		}
		url = "http://xuanzhi.today36524.com/user/login"
		resp =self.s.post(url,data=postdata,headers=head)
		url = "http://xuanzhi.today36524.com/getCsrfToken?"
		self.s.get(url)
		self.csrf = self.s.cookies["csrf_token"]

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
		url = "http://xuanzhi.today36524.com/store/create"
		head = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
			"Content-Type":"application/json",
			"X-Csrf-Token":self.csrf,
		}
		postdata = {
			"cat1":'',
			"categoryId":61,
			"categoryName":"已开店",
			"country":"中国",
			"district":"",
			"latlon":"108.298565,22.881228",
			"markerCate":"已开店",
			"storeInfo":json.dumps({
				"店龄":"新开店",
				"社区类型":"学校型",
				"店铺类型":"直营"
			}),
			"storeName":"安吉客运店"
		}
		print(json.dumps(postdata))
		print(head)
		print(self.s.cookies)
		resp = self.s.post(url,data =json.dumps(postdata),headers = head)
		print(resp.text)

if __name__ == "__main__":
	with mymysqlclass(myconfig) as my:
		data =my.select("select * from spider.today")
	print(data)
