# coding:utf8
import requests
import re
from bs4 import BeautifulSoup as bs
import hashlib
s = requests.Session()
url0 = "https://m.jd.com/"
resp = s.get(url0,verify=False)
print(resp.status_code)
print(resp.url)
print(resp.cookies)

url1 = "https://plogin.m.jd.com/user/login.action?appid=461&returnurl=http%3A%2F%2Fhome.m.jd.com%2FmyJd%2Fhome.action&ipChanged="

resp = s.get(url1,verify=False)
print(resp.status_code)
print(resp.url)
print(resp.cookies)
print(resp.text)


url2 = "https://plogin.m.jd.com/cgi-bin/m/domlogin"

class RSAKeyPair():

    def __init__(self,a,b,c,d=1024):
        self.e = [int(a)]+[0]*130
        self.d = [1,1]+[0]*129


def setMaxDigits(num):
    maxDigits = num
    zero_array = [0]*maxDigits
    bigZeros = zero_array
    bigOne = zero_array
    bigOne[0] = 1

def getusername(username):
    str_rsastring = "C20FCAE7ED5E9122439DE58B7E0258CB2AFF5561EADBCDE476B0DC72B4850FF8AF1E2546BEB23EE5721397F0A1106B864F87B8D4EE053FE3397DFB33F12AF91424286D39829E6A76953B65B88C0B10B6B6D8EB788A346746FB7D51A1C4A349F671536F19811D84A011F388F4939C8AB0B59AE513851EF4FD49376B2D3F75BD71"
    setMaxDigits(131)
    b = RSAKeyPair("3","10001",str_rsastring,1024)

def getpasswd(pwd):pass

def getdat(content):
    pattern = "md5\((.*?)\);"
    target = re.findall(pattern, content)[0]
    td = target.split(")+")
    result = list()
    for i,t in enumerate(td):
        t = str(t)+")" if i !=len(td)-1 else str(t)
        if "'+'" in t:
            result.append(t.split("'+'")[0]+"'")
            st = t.split("'+'")[1]+"'"
        try:
            st,deal = t.split(".")
        except:
            if "md5" in t:
                tr = re.findall("md5\((.*?)\)",t)[0]
                t = hashlib.md5(tr.encode('utf-8')).hexdigest()
            result.append(t)
        else:
            if "toUpper" in deal:
                st = st.upper()
            elif "toLow" in deal:
                st = st.lower()
            elif "substr" in deal:
                st = st[int(deal[-2]):]
            elif "charAt" in deal:
                st = st[int(deal[-2])]
            result.append(st)
    return hashlib.md5("".join(result).encode("utf-8")).hexdigest()

postdata = {
    "username":getusername("17621064595"),# 需要加密
    "pwd":getpasswd("zhouhen987"),# 需要加密
    "remember":"true",
    "s_token":"?",
    "dat":getdat(resp.text),
    "wlfstk_datk":"06435bdeae2f30d3f76ff3145ee98071",
    "risk_jd":{
        "eid":"7AQ7MFUYFZTRLN2WNWVDG7ERGHUIKQG6V5QNMASWLFHFM4F25HBD3GLWWHKL477C7P4NECRHO34MVOYWSDPVHJRCYI",
        "fp":"f223f5a3ea9470ad17bb9a6c3d99cae7",
        "token":"NIIE2AI76LTKYQLE25HG4JJFR4EVKTF57A226JQMFSJJHOEZTOXFA3WVDGQ2YF7AB3HKAGQVQDGNW",
    }
}
print(postdata.get("dat"))