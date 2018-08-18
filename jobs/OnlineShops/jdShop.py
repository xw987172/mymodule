#coding : utf8
import requests
from urllib.parse import quote

url = "https://so.m.jd.com/ware/search.action?keyword=%E5%A8%83%E5%93%88%E5%93%88ad%E9%92%99%E5%A5%B6&searchFrom=home"

resp = requests.get(url)

print(resp.text)