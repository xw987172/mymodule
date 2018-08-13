# coding:utf8
import requests
import re
from selenium import webdriver
import urllib.parse
from bs4 import BeautifulSoup as bs
import hashlib,re
import execjs,os
import base64
s = requests.Session()
url0 = "https://m.jd.com/"
resp = s.get(url0,verify=False)
print(resp.status_code)
print(resp.url)
print(resp.cookies)
sid = resp.cookies.get("sid")

url1 = "https://plogin.m.jd.com/user/login.action?appid=461&returnurl=http%3A%2F%2Fhome.m.jd.com%2FmyJd%2Fhome.action&ipChanged="

resp = s.get(url1,verify=False)
print(resp.status_code)
print(resp.url)
print(resp.cookies)

str_rsaString = re.findall("str_rsaString = '(.*?)'",resp.text)[0]

s_token = re.findall("str_kenString = '(.*?)'",resp.text)[0]

def getMd5(obj = resp.text):
    mds = re.findall("return md5\((.*?)\);",obj)[0]
    parts = mds.split(')+')
    result = ""
    for part in parts:
        part = part+")"
        if "md5" in part:
            h1 = hashlib.md5()
            st = re.findall("md5\('(.*?)'\)",part)[0]
            h1.update(st.encode(encoding='utf-8'))
            result += h1.hexdigest()
        elif "toUpper" in part:
            st = re.findall("'(.*?)'",part)[0]
            result += st.upper()
        elif "charAt" in part:
            st = re.findall("'(.*?)'",part)[0]
            index = int(re.findall("charAt\((.*?)\)",part)[0])
            result += st[index]
        elif "toLow" in part:
            st = re.findall("'(.*?)'",part)[0]
            result += st.lower()
        elif "substr" in part:
            st = re.findall("'(.*?)'",part)[0]
            index = int(re.findall("substr\((.*?)\)",part)[0])
            result += st[index:]
    h1 = hashlib.md5()
    h1.update(result.encode(encoding='utf-8'))
    return h1.hexdigest()

def getRsa(pub,target):
    url = "http://58.87.111.185:5000/getRsa?pub={0}&target={1}".format(pub,target)
    driver = webdriver.PhantomJS()
    driver.get(url)
    data = driver.page_source.encode("utf-8","ignore").decode()
    rsaStr = re.findall("<p id=\"info\">(.*?)</p>",data)[0]
    return urllib.parse.quote(rsaStr)

def get_risk_id():
    risk_id = dict()
    url = "https://payrisk.jd.com/m.html"
    resp = requests.get(url)
    risk_id["token"] = re.findall("'(..*?)'",resp.text)[0]



username = getRsa(str_rsaString,"17621064595")
pwd = getRsa(str_rsaString,"zhouhen987")
dat = getMd5()
risk_id = {
    "eid":None,
    "fp":None,
    "token":None,
}
authcode = None
url = "https://plogin.m.jd.com/cgi-bin/m/domlogin"
postdata = "username=%s&pwd=%s&remember=true&s_token=%s&dat=%s&wlfstk_datk=%s&authcode=%s&risk_jd%5Beid%5D=%s&risk_jd%5Bfp%5D=%s&risk_jd%5Btoken%5D=%s" %(
    username,
    pwd,
    s_token,
    dat,
    dat,
    authcode,
    risk_id.get("eid"),
    risk_id.get("fp"),
    risk_id.get("token"),
)
resp = s.get(url)
print(resp.cookies)
pt_key = resp.cookies.get("pt_key")
pt_token = resp.cookies.get("pt_token")

def last():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Cookie":"pt_key=AAFba5gQADDskHO2evRYNF1VZn8IFuR_L1PS7H71f8n_EZCDyeBXnjgcVi4sXggxkKaT3weibOk; pt_token=9luh4qgv;",
    }

    url = "https://home.m.jd.com/myJd/newhome.action?sid=ed513d92f632fffd8102451154d60fe8"

    resp = requests.get(url,headers = headers)
    print(resp.status_code,resp.url)
    print(resp.text)
    print(resp.cookies)

last()