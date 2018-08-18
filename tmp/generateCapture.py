# coding:utf8

import requests
import os,sys
dirname = r"C:\Users\xwtoday\Desktop\captures"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Cookie":"__jdu=1906441014; TrackID=1mbmNEeOuGM2roVPhL7MRQxrT1nZ9TXCHhtrC3yg5GpmposI8OBwRJhJN-ItfTzi_PCO2pvM_wDbLUqRHq0JuxHTUjMIKkVkdVi8ugu1AQ_E; pinId=jDozGbtvXq_QjwD949cXx7V9-x-f3wj7; shshshfpa=27500b89-83b5-ea5a-c558-24cee07d7dd5-1531711876; shshshfpb=080d411448475985141423b51c98a480d957d7e3c420864c15b4c11372; 3AB9D23F7A4B3C9B=GKNIPXVBOM72DYEOJ46UKOJIKY6BHHDVOELKVLWQ6LVBWMBWPXURNP5C3WS22RXC6UZM6IO53UDR2U2Y32IM57NELE; abtest=20180817145005213_01; subAbTest=20180817145005213_33; mobilev=html5; USER_FLAG_CHECK=1554f04f7bb07ea759f3945846bff6ce; sid=0e6650058cae8af3bdb6291f16a18a26; __jda=122270672.15344886040301646387553.1534488604.1534488604.1534488604.1; __jdv=122270672|direct|-|none|-|1534488604035; __jdc=122270672; mba_muid=15344886040301646387553; intlIpLbsCountryIp=58.49.27.26; intlIpLbsCountrySite=jd; mhome=1; autoOpenApp_downCloseDate_auto=1534488604500_21600000; visitkey=7454467032510494; wq_ufc=1554f04f7bb07ea759f3945846bff6ce; guid=b77373e60b69fd01d32fb34715ae4a6efcb92625a8a8ef03adbf66825dd47fe3; lang=chs; lsid=14rdfxljqvxc4g3qhnt6p6ymlovjdn8f; shshshfp=a01bb958511344338a768fb96edf2336; shshshsID=c02e0ad0868fa8167926ba5d594f2a4f_1_1534488609186; __jdb=122270672.2.15344886040301646387553|1.1534488604; mba_sid=15344886040374595092835391050.2",
}
url = "https://plogin.m.jd.com/cgi-bin/m/authcode?mod=login&v=0.3122098597483174.png"
for i in range(5000):
    resp = requests.get(url,headers=headers,verify=False)
    print(resp.url,resp.status_code)
    with open(os.path.join(dirname,str(i)+".png"),"wb") as fp:
        fp.write(resp.content)