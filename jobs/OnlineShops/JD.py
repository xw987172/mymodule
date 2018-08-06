# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import sys
import json
import time,math
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA


def getEncrypt(password,publickey):
    str1 ="""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5lalja
N9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7P
AzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQ
q+CA6agNkqly2H4j6wIDAQAB
-----END PUBLIC KEY-----
    """
    rsaKey = RSA.importKey(str1)
    cipher = Cipher_pkcs1_v1_5.new(rsaKey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text

def getEncrypt2(password,publicKey):
    pass

class JD:
    login_url = "https://passport.jd.com/new/login.aspx"
    s = requests.Session()
    def login(self):
        requests.utils.add_dict_to_cookiejar(self.__class__.s.cookies,{"__jdv":"122270672|direct|-|none|-|1532678595779"})
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
            "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
        }
        resp = self.__class__.s.get(self.__class__.login_url,headers = headers,verify=False).content
        soup = bs(resp,"lxml")
        form = soup.select("#formlogin")[0]
        postdata = dict()
        postdata["sa_token"] = form.select("#sa_token")[0].get("value")
        postdata["uuid"] = form.select("#uuid")[0].get("value")
        mid_url1 = "https://gia.jd.com/fcf.html?a=7TJI7TceW0Pu7Tce7TZ37Tce7Tce7T7L7TcezlP47Tce7TZ37Tce7Tce7T7L7TceWIAewGAB6SAewdwPwHcPw4wPwH7QWIAewGAB6SAewH34OTwkiTNQZBbQOg%3ClZlw*iTAeZLw*wHaDwl%3ClFTJP7Tce7T7L7TceJGAewGAB6SAewHcuZIDevH%3CPwHcPw4wPwH7X7Tce7TZ37TceW0NBWt3XWd6uyQ6uil9C7T70zQft7T70z09dygDuihZ*qIAewGAe6eAewQFH7Tce7TZ37TceZjNRZjk0ffP0gPRST%3CDefjEhf4R1ZjfSRjbfSACRRBFgZfNOTANTfjx0S%3CFZZ%3CieZAbIRLZ1TNJhS%3CCwZLWt6BJ6Z%3CEN6k7cTBwjTfF5gfJTRN3gS%3CpS6kP77Tce7T7L7TceJIAewGAB6SAew47f64CIR4ZIRkPZTLf%3CTPF7Z%3CCKwP7Nf4CRZPNgZ%3CRLTNN3f4Zcfk7fZNFgAkRcfTcBSPJ7fk7ITNJ3RBf1gTfigHfc6476fkF6ZfF57Tce7TJ%3C/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Referer": "https://passport.jd.com/new/login.aspx",
        }
        pdata = {
            "g":"7TJI7TceJhZPW4NdFgEj7Tce7TZ37TcewTJbZH4lFLJHiBW*wTAkOLb4iBZPZQw*iB<BwLiEwl<PwHcPw4wPwH7XWQPdygDPwHcPwj<PwH7*ieAewGAe6eAewQxbzQJkigJP7Tce7TZ37TceqQaC6jDPwHcPw4wPwH7XWeAewGAB6SAew4E37Tce7T7L7TceztZgFh7Byg9u7Tce7TZ37TceT4<PwHcPw4wPwH7GWQ9tWlfe7Tce7TZ37Tceih3*z0ftFg7ryhRVilbezlkP7Tce7T7L7Tceid7XJtZPWPFPWdZpzlDPwHcPwj<PwHckwBWuwBiPwHcPw4wPwH7HzlxXW4RPW1Ro7Tce7TZ3wH6Pw4wPwH7Bit7PFgESFhZXz1fjyg9u7Tce7TZ37TceOL2*qL<eOL2PwHcPw4wPwH7jygkPqQ9uFA9QFdZPJIAewGAB6SjD7T7L7TceWlfBWlPXzPZjzt7bFlAPwHcPwjNjWdfP7T7L7Tcez09HigxTJ09eigJP7Tce7TZ3J17kFSAe6eAewQPuF0fDFgR<iGAewGAB6hReJgAPw4wPwH7bF0RIFgbbJQPXWGAewGAB6gFbz1ZP7T7L7Tcezt3Pz4RbJ0NGihZP7Tce7TZ3J17kFSAe6eAewQZ*JSAewGAB6SAew4E37Tce7T7L7TceW0xbJ0FXWQjPwHcPwj<PwH7ZigZ7zdRPzIAewGAe6eAewQZHzGAewGAB6T6Pw4wPwH7bWtcPwHcPwj<PwHcjZL<*wIAewGAe6eAewdReigZr7Tce7TZ37TceT4<PwHcPw4wPwH7*z1fdygEB7Tce7TZ37TceOLajwQAeZHPQFgNGOL7bwTFbOLNGFTFQiH<BwLNPwBaPwHcPw4wPwH7HigElihwPwHcPwj<PwH7bOTAlZTitZLNPFQ<kFTZGiB4jigFGZT4DFT74ZTfQOSAewGAe6eAewdJPiQJs7Tce7TZ37TcewLfHFQfbigfGigABOLAjw0cxZLA*OgZbFTbHFTPPiTiPwHcPZj6/",
            "d":"7TJI7Tceil<PwHcPwj<PZjcPwH7jF<bbWlaPwHcPwj<PwH7bOTAlZTitZLNPFQ<kFTZGiB4jigFGZT4DFT74ZTfQOSAewGAe6eAewdJPiQJsS0NByIAewGAB6SAewH2kilFPigNPiQNPwBakZL3GwT6kwLPHigADilAEFg<l7Tce7T7L7Tceil9uJ0fDJ<EbzgAPwHcPwj<PwH7tFg7dzIAe6lfDW0feygkPzdRbzIktFg7dzIAewGAe6eAewdJPiQJsJQfeWlPXzGAewGAB6SAewPJPi4Jw7Tc*wSD*7Tc*K<9*FgE1TIAew<fT7Tc*wGD*7Tc*6lbezlkpJgjp7Tce7T7L7TceWlbbF0PuFjxg7Tce7TZ37TceflfGRj*PwH31TNZw7Tc*RfwPwH2xvH2PwH2oTt3Pz4Jw7Tc*RfwPwH31TNZw7Tc*RfwPwH2xvH2PwH3Ly17XzgPkzS4PwHcPw4wPwH7lFgE4ztcPwHcPwj<PwH7hFg7vyh6PwHcPw4wPwH7eFgE4Fh7PWGAewGAB6SAewPJPi4CpJIAewNJPi4Jw7Tce7T7L7TceFhbjFgEByg9uWeAewGAB6SAk6GAew4NORjxNhlPuWtRbzQZPFN9bWd7bqhwPwHcPw4wPwH7NgNRViQxPzQRVzgPuzgND7Tce7T7L7TceRfbAhlZXz09ehl7kFQFPWP9oigxQhlFszlNj7Tce7T7L7TceRfbAhlFeigJVF0f*J0aPwHcPw4wPwH7NgNRVWlbbF0fehtRPq1RkWQfVz0947Tce7T7L7TceRfbAhtRPq1RkWQfVFQPsJ0fehlNuyhZXJ17XW0PH7Tce7T7L7TcefjfISjPAhjfifN9jFhbjJh7PhlFpz1RPWP9bzQPBztRezt3pieAewGAe6eAew4fifN9BA4JI7Tce7T7L7TceTjfThlfsFgkPzdRVygE4FhbVJgPuJIAewGAe6eAew49NAk9BJ0NuF0NeFN94Fh7pJQNjyhFPWeAewGAe6eAew49NAk9jFhbjJh7PhlFszlNj7Tce7T7L7TceTjfThtRPq1RkWQfVFQxXihRVz0PuFgNe7Tce7T7L7TceTjfThtRPq1RkWQfVy0NsFP9Qz09bJIAewGAe6eAew49NAk9jFhbjJh7Phlbbz0FVFQxXihRVz0PuFgNe7Tce7T7L7TceTjfThtFPWdRPqN9bWd7bqf9XiQpPit6PwHcPw4wPwH7hRA71TN9HzlxXWP9GJgFQFh7VFQxXih6PwHcPw4wPwH7hRA71TN9Hzlk*WQfBWlf4htRPq1RkWQfVWBZjieAewGAe6eAewPJN64C7fN9hRA71TN9Hzlk*WQfBWlf4htRPq1RkWQfVWBZjieAewGAe6eAewPJN64JwhlZXzh3eFhZBFgRVJ0fDJ1feFf9BwtRHhtZeFlcPwHcPw4wPwH7hRA71TN94Fg7kFk9eFgE4Fh7PWP9pzQFX7Tce7T7L7TcefjfIRjxVF0fGJgJVWlbbF0feWeAewGAe6eAewPJN64JwhlRPW1RohtRPq1RkWQAPwHcPw4wPwH7hRA7vSfRVfjfIRjxVF0f*J0bVJ0fDJ1feFSAewGAe6eAewPJN64JwhlReihJVidfQFQfeWeAewGAe6eAewPJN64JwhlxXWlfVil9uJ0fDJIAewGAe6eAewPJN64C7fN9hRA71TN9sztZPhlZXzdRPq16PwHcPZA6Pw4wPwH7tJhiPwHcPwj<PwH77zdRPzIAew<PuieDPwHcPw4wPwH7tJhcPwHcPwj<PwH77zdRPzIbSKSAew<Peyhwof<jp7Tc*Rt7bW0bpitwPwH2lwT2*7Tce7TJ<7T7L7TceJ1wPwHcPwj<PZjcPwH74FhFpilfAygkP7Tce7TZ3wTABwH4*OTakZLaBOSAe6eAewQRPJQPHFAfuFNRpzgAPwHcPwj<xZTweOT2EOLAkwH2l7TJ<7T7L7TcezSAewGAB6SAt6GAewQZXzh3bJ<kXF0APwHcPwj<PwH7LAkwx6l9CW0Nj7Tce7TJ<7T7L7TceFQ8PwHcPwj<PZAcPwH73WQPbzIAew<7sigZr7Tce7T7L7Tce6QNky0NkWeAewL4B7Tce7T7L7Tce6lbbz0C4JhZjFhcPwHcPw4wPwH71JgEdAlfX7Tce7T7L7TceS0PeigJpzQ8PwH3TigEB7Tc*RjcPwHcPw4wPwH77zh3bit6PwHcPw4wPwH7ZFgEszeAewGAe6eAewP3bW1PeJhwPwHcPw4wPwH7SzlZrJlfszIAewGAkRIAe6eAewQDPwHcPwj<PZjcPwH7lFgE4zt7TJgcPwHcPwj<PwHcPwHcPw4wPwH7*WQ94JgZjAtfG7Tce7TZ37TcewH2*wB2xwLWPwHcPw4wPwH7lFgE4ztcPwHcPwj<PwH71zl9dz0APwH37zQwu7Tce7T7L7TcezgNDf09kilb6zlPuJ1wPwHcPwj<*7T7L7Tcey0NeF1JbWQfLzlEHJh7eFgEHqSAewGAB6T6Pw4wPwH7Hzl9rygfNzQNGz0f47Tce7TZ3J17kFSAe6eAewQN*W<ZXF0fOigkP7Tce7TZ37TceTg9mygxsiSAewGAe6eAewQN*W<EbzgAPwHcPwj<PwH7OFhRBilN*FSAewGAe6eAewQN*WNFPWdZpzlDPwHcPwj<PwHckvH2PwH2oTgNHygEjztZo7TZI7Tc*SgEjFg*PwH3ZigwPwH35AeAewNaPwH2xwN8xwk8jKSAew<N*W0xPflfGSlPj7T70ZTwtvHwl7Tc*K<Ccf<kw7T7L7Tc*z0PrFSAew<JPilCXKSAew<ZoWQ9CFSAeRHitvH2uwBwEZGDEOSAewNZbFQNeySAeRHABZeDBZGAewGAe6eAewd3sihRQzt7C7Tce7TZ37TceTgNHSgEjFg*PwHcPw4wPwH7*WQ94JgZj7Tce7TZ37TceRlfHyl8PwHcPw4wPwH7kWlfe6gJPzd6PwHcPwj<PwH7Zztppz0xb7T70ZSD*7Tc*K<kbilPuJ09ByIAB6GAew<PuJ0fs7Tc*TgNH7Tc*TkwPwH3i7Tc*wT3VwTZVZI4PwH33W13sFfJPi4CpJIAeRHABZeDBZGAewIbvSNRZTIAe6eAew0xpylAPwH31FgZrze4PwH3Ly17XzgAPw4ilZeD*vHwBOTiuOT4PwH3TigFbWQ4Pw4ikwBWuwBiPwHcPw4wPwH7sigEdJgNdFSAewGAB6SAewdpovAZO7Tce7T7L7TcezlEwygEP7Tce7TZ3J17kFSAe6eAewQpbJQNNzQNGz0f47Tce7TZ3FQNsWlAPw4wPwH74FhFpilfZFgkXWd4PwHcPwj<D7T7L7TceFgEkzgfeihRpzlE5WQRPWGAewGAB6SAk6GAewdFPzQRXWPZkiGAewGAe6eAewd3ezlRkitRTJgcPwHcPw4wPwH7lFgE4ztcPwHcPw4wPwH7CihbAztfHyN3XygEjWeAewGAe6eAewQbbWQRtih7P6l9uitfeWQfuit4PwHcPw4wPwH7Hzl9rygfNzQNGz0f47Tce7T7L7Tceih3*6l94FAEbzgAPwHcPw4wPwH7bW13OigkP7Tce7T7L7Tceih3*fQfeWlPXzGAewGAe6eAewd3sihRQzt7C7Tce7T7L7TceW17XF1fHJIAewGAe6eAewdfBFh73FlfuJIAewGAe6eAewQxbzQJkigJP7Tce7T7L7Tcez0NuFtfbFlfB7Tce7T7L7TcezlEwygEP7Tce7T7L7TceF09OztRAWQNHyeAewGAe6eAewQJPzlxXilNjyg9u7Tce7T7L7Tcezgf4ygN<FhFpilfB7Tce7T7L7Tceil9uzQfHJ0PXzGAewGAe6eAewd3sJgJpzdwPwHcPw4wPwH7CygkPf1P*FhwPwHcPw4wPwH7tFg7ryhRAFgk*zt7bWdPTJ09eigJP7Tce7T7L7TceJlfGylPjA0feWlPBJ0fuJNZjzt7bFlAPwHcPw4wPwH7BFh7lygZPfl9eylfe7Tce7T7L7TceFlfj6QNjJ0feqSAewGAe6eAewdZPzQRIFgNHzlDPwHcPw4wPwH7dFhR1igkPW0N4WeAewGAe6eAewQJPJNfBFh7ZFgRpiSAewGAe6eAewdJPiQCpJ<JPJNfBFh7ZFgRpiSAewGAe6eAewQpbJQNNzQNGz0f47Tce7T7L7TceJQPGWQNjFSAewGAe6eAewd7PWhfPWtRZSAR76gZHFhZB7Tce7T7L7Tceidf4Flfj7Tce7T7L7TceW0fezgPBWlPXzdwPwHcPw4wPwH7*WQfBFgEjihRpzlDPwHcPw4wPwH7Gz1fPJ09XJ0aPwHcPw4wPwH7eFgJpWtRPWP3eztRXil9sS0NuF0xPWGAewGAe6eAewdfuWQfdyhZjFh76WQ9jzlZXz<bbzQRsFhcPwHcPw4wPwH74FhFpilfZFgkXWd4PwHcPw4wPwH7Hz0P*iQ9bWQ6PwHcPw4wPwH7HWQf4FgEjygNsWeAewGAe6eAewdZjzt7bFlAPwHcPw4wPwH7kWlcPwHcPw4wPwH7eFhNkFhZjTgf4ygNvFhPTqhZjFgk3ilZPWtwPwHcPw4wPwH7CFgRpiAZbW0NGygxpJ0PPWeAewGAkRIAtRIAe6eAewd2PwHcPwj<PZAcPZjcPwH7uigkP7Tce7TZ37Tce6lbezlkP7Tc*A<R07Tc*A0xkFlPu7Tce7T7L7TceFQPsFgEbzgAPwHcPwj<PwH7pzdRPWQEbzIk*F0iCJQPPJlfe7Tce7T7L7TceF0fBit7pW1RpzlDPwHcPwj<PwH76zt7jig7sFSAew<RXitfCFgEj7Tc*RQ9ezgNj7Tce7T7L7TcezgPCFfREW0fB7Tce7TZ37TfI7TJI7TceF0fBit7pW1RpzlDPwHcPwj<PwH76zt7jig7sFSAew<RXitfCFgEj7Tc*RQ9ezgNj7Tce7T7L7TceWtfQFQPDFhwPwHcPwj<PwH7*F0iPwHcPw4wPwH7jqh3P7Tce7TZ37Tceih3*z0PHihRpzlDPw4FDvgJXzlJsFSkHy17XzgACW0RQ7Tce7TJ<7Tf<7TJ<7T7L7TJI7TcezQNCFSAewGAB6SAew4ZoWQ9CFSAewN3<RGAewNFpFhJPWGAewGAe6eAewQFpz0fuigkP7Tce7TZ37TcezgbUFQ7CF0JHFQpGid3bFg9UzlFXy09PFQJpFgbUig4PwHcPw4wPwH74FhZHWQP*J0PXzGAewGAB6SAewGAewGAe6eAewQkpzgfAqh3PWeAewGAB6SAk6GAt6GAewQRPWlZeyh3jyg9u7Tce7TZ37Tce7Tce7T7L7TceWtfQFQPDFhwPwHcPwj<PwH7*F0iPwHcPw4wPwH7jqh3P7Tce7TZ37Tceih3*z0PHihRpzlDPw4F*F0iPwHcPZj6PZA6PZj6Pw4wPZjcPwH7uigkP7Tce7TZ37TceTQNjyhFP7Tc*6lxpFgEj7Tce7T7L7TceFQPsFgEbzgAPwHcPwj<PwH7pzdRPWQEbzIkuigZsvh3sJgJpzGAewGAe6eAewQRPWlZeyh3jyg9u7Tce7TZ37Tce7Tce7T7L7TcezgPCFfREW0fB7Tce7TZ37TfI7TJI7TceF0fBit7pW1RpzlDPwHcPwj<PwH7OihRpJQAPwH3Lz0PPzd6PwH3Nq0fHJhRbiQxP7Tce7T7L7TceWtfQFQPDFhwPwHcPwj<PwHcPwHcPw4wPwH7jqh3P7Tce7TZ37Tceih3*z0PHihRpzlDPw4FDvgEbil*PwHcPZj6Pw4wPZjcPwH74FhZHWQP*J0PXzGAewGAB6SAewP3XWdRbiQxP7Tc*TQNjyhFP7Tc*6lxpFgEj7Tc*RhbPitfjig7sFSAewGAe6eAewdZkFQFpq0fB7Tce7TZ37Tce7Tce7T7L7TceJ1P*FSAewGAB6SAewQN*W0xpilNjyg9u7T70qIk*zQNHzIAewGAtRIAkRIAtRIAkRIAe6eAewdWPwHcPwj<PZjcPwH74FhFpilf6yhbPzN7bJ0PX7Tce7TZ3wGAe6eAewdZHWQfPzPRXWIAewGAB6TcB7T7L7TceWlZeFgfuT0fQJIAewGAB6Sjx7TJ<7T7L7TceWeAewGAB6SAt6GAewQNligPsS0fpFlbj7Tce7TZ3ZB<e7T7L7TceihFbygxhygRjyIAewGAB6T<eOL2Pw4wPwH7HzlxXW4RPW1Ro7Tce7TZ3wH6Pw4wPwH7oFgPdy16PwHcPwj<DwL2Pw4wPwH7tygRjyIAewGAB6T<eOL2Pw4wPwH7*yhbPz<RPW1Ro7Tce7TZ3wH6PZj6Pw4wPwH7BieAewGAB6SAt6GAew4NHJ0PlFA7XWQRPWGAewGAB6SAewd7diGakOSAe6eAewL<kweAe6eAewLckwG4PwHcPw4wPwH73itRpJQfLih3jyg9u7Tce7TZ37TceWQJGKL2Pw4wPwH2*7T7L7Tc*wI4PwHcPw4wPwH73W13hzt7rWt3bilAPwHcPwj<PwH7eFlcowTW*7T7L7Tc*wTW*7T7L7Tc*wTW*KSAewGAe6eAew47bilCdWQ9kzQ6PwHcPwj<PwH7eFlcoOT4Pw4wPwH2EOSAe6eAewLc*ZG4PwHcPw4wPwH7IJhRjzlE0igZP7Tce7TZ37TceWQJGKLckZSAe6eAewLckZSAe6eAewLckZS4PwHcPw4wPwH7IJhRjzlEcygJoz0Pdy16PwHcPwj<PwH7eFlcowHwB7T7L7Tc*wHwB7T7L7Tc*wHwBKSAewGAe6eAew47kJ1RXzPZoigRXJeAewGAB6SAewd7diGaxZT4Pw4wPwH2xZH2Pw4wPwH2xZT4p7Tce7T7L7Tce6dfjJ09uf0fDJIAewGAB6SAewd7diGa*7T7L7Tc*wIAe6eAewL2p7Tce7T7L7Tce6lN*J0PXzPRPq16PwHcPwj<PwH7eFlcowIAe6eAewL2Pw4wPwH2*KSAewGAe6eAew4JeihPAFhbj7Tce7TZ37TceWQJGKL<eZeAe6eAewL<eZeAe6eAewL<eZe4PwHcPw4wPwH7cygJoz0Pdy16PwHcPwj<PwH7eFlcowTWD7T7L7Tc*wH<k7T7L7Tc*wHAkKSAewGAe6eAew4bpFlbsygJoJNRPq16PwHcPwj<PwH7eFlcowIAe6eAewL2Pw4wPwH2*KSAewGAe6eAew4PuigZjyhFP6Q9eF0fe7Tce7TZ37TceWQJGKLckZSAe6eAewLckZSAe6eAewLckZS4PwHcPw4wPwH77zQNHJ0PlFAZbW1RpzlDPwHcPwj<PwH7eFlcowHAk7T7L7Tc*wHAk7T7L7Tc*wHAkKSAewGAe6eAew4PuigZjyhFP6lN*J0PXzPRPq16PwHcPwj<PwH7eFlcowIAe6eAewL2Pw4wPwH2*KSAewGAe6eAew4PuFQ9IigZrFt7XJgE47Tce7TZ37TceWQJGKLckwSAe6eAewLckwGAe6eAewL<EZe4PwHcPw4wPwH77zQFXf0fDJIAewGAB6SAewd7diGa*7T7L7Tc*wIAe6eAewL2p7Tce7T7L7TceTgfuJSAewGAB6SAewd7diGaeZLiPw4wPwH2eZLiPw4wPwH2eZLip7Tce7T7L7TceTgfuJfRPq16PwHcPwj<PwH7eFlcowHAk7T7L7Tc*wHAk7T7L7Tc*wHAkKSAewGAe6eAewPZHWQ9sz07bWGAewGAB6SAewd7diGaxZB2Pw4wPwH2xZB2Pw4wPwH2xZB2p7Tce7T7L7Tcef0beFgf<R0NeykZoigRXJeAewGAB6SAewd7diGa*7T7L7Tc*wIAe6eAewL2p7Tce7T7L7Tcef0beFgf<RQNHFSAewGAB6SAewd7diGaxOTcPw4wPwH2xOTcPw4wPwH2xOTcp7Tce7T7L7Tcef0beFgf<S0Pdy0xpFlbj7Tce7TZ37TceWQJGKLckZSAe6eAewLckZSAe6eAewLckZS4PwHcPw4wPwH7Ay17PFARwygJoJNZoigRXJeAewGAB6SAewd7diGaeZTAPw4wPwH2eZTAPw4wPwH2eZTAp7Tce7T7L7Tcef0beFgf<AlbbF09t7Tce7TZ37TceWQJGKL2Pw4wPwH2*7T7L7Tc*wI4PwHcPw4wPwH7hygE4ztWPwHcPwj<PwH7eFlcowHwl7T7L7Tc*wHwl7T7L7Tc*wHwlKSAewGAe6eAewPJpzQRXJjFeigkP7Tce7TZ37TceWQJGKL<twIAe6eAewL<twIAe6eAewL<twI4PwHcPw4wPwH7hygE4ztJAFhbj7Tce7TZ37TceWQJGKL2Pw4wPwH2*7T7L7Tc*wI4PwHcPZj6Pw4wPwH7jqGAewGAB6SjjOL2Pw4wPwH7syg*PwHcPwj<PwHcxOTcuwTiDvH<uwT2j7Tce7T7L7TceJlPs7Tce7TZ37Tceihf4yg9pzd3kJIAB6GAB6Q6BO07bF0cEZHwBOgwEwlcxZHA*ZT7HOLFGiHixFQ<jwHPGOTNQiT6EOTNGwBABFQAxwHNbZHABOgNPiQ6DwBwPZjZbJgRpzlPuW1fj7TZI7TZIF0fQihfsJIAt6lNkF0PXztfjW1fj7TZI7TZIFLalZg<EwB2xwLatOLwtwQZQwg<*F0FPiQF4wQAEOTZPwHfPFL<EZT4EZBcEwHcEF0ZPFQf4ZL6BZLcEiHZbZeAt6lNkF0PXztfjW1fj7TZI7TZIF0fQihfsJIAt6tFpF0fXygE*Jh6PwjcPwjc*ZlFHZli*iTJHiTb4wTJQOgiBFL4BwLRGwH2EwLZ4FTA*w0ZPZT<EZBf4iT<EwgZQFgNbO0cjZLN4iTi*OLfH7Tce7T7L7TceWtwPwHcPwj<PZjcPwH7Hzl9rygAPwHcPwjNjWdfP7T7L7Tcez09HigxTJ09eigJP7Tce7TZ3J17kFSAe6eAewdZPWtZpzlETJ09eigJP7Tce7TZ3J17kFSAe6eAewQJszl7bzNZjzt7bFlAPwHcPwjNQigxBFSAe6eAewQPuF0fDFgR<6GAewGAB6hReJgAPZj6PZj6/",
        }
        resp = self.__class__.s.post(mid_url1,headers=headers,data=pdata,verify =False).text
        postdata["eid"] = resp
        # postdata["fp"] = form.select("#sessionId")[0].get("value") or 'unknow'
        postdata["fp"] = "0d935a1f78f9a67c0a524302883a6e7e"
        postdata["_t"] = form.select("#token")[0].get("value")
        postdata["loginType"] = form.select("#loginType")[0].get("value")
        postdata["pubKey"] = form.select("#pubKey")[0].get("value")
        postdata["useSlideAuthCode"] = '1'
        postdata["loginname"]="17621064595"
        postdata["nloginpwd"] = str(getEncrypt("zhouhen987",postdata["pubKey"])).replace("b'","").replace("'","")
        # postdata["nloginpwd"] = "TUQgKuXn5sZYmFCD3%2BLwnWgAxA0JhlFKiUcRdty%2FPtZgY95kNTMf1zL%2Fr4uHfqKqdkudzDc85Orlpt7tRLEcfvfQsAiVdDYUJs%2Bn%2FJ8WpdYTeT4j%2BtaoxO8tXMROYZyhxLE63dzpWRRa97Q2voSq7E3VzOf%2Fod1KgkGCZYa90Fg%3D"
        seqSid_url = "https://seq.jd.com/jseqf.html?bizId=passport_jd_com_login_pc&platform=js&version=1"
        resp = requests.get(seqSid_url,verify=False).text
        postdata["seqSid"] = resp.split(";")[0].split("=")[1].replace('"','')

        cookie1url ="https://qr.m.jd.com/show?appid=133&size=147&t="
        self.__class__.s.get(cookie1url,verify=False)

        requests.utils.add_dict_to_cookiejar(self.__class__.s.cookies,{"3AB9D23F7A4B3C9B":postdata["eid"]})
        requests.utils.add_dict_to_cookiejar(self.__class__.s.cookies,{'__jda':'122270672.15330054186311418709161.1533005419.1533005419.1533005419.1'})
        requests.utils.add_dict_to_cookiejar(self.__class__.s.cookies,{'__jdb':'122270672.1.15330054186311418709161|1.1533005419'})
        requests.utils.add_dict_to_cookiejar(self.__class__.s.cookies,{'__jdc':'122270672'})
        requests.utils.add_dict_to_cookiejar(self.__class__.s.cookies,{'__jdu':'15330054186311418709161'})

        # 以上正常
        # 接下来输入账号密码，进入authcode
        r = np.random.rand()
        try:
            authcode_url = form.select("#JD_Verification1")[0].get("src2")
            if authcode_url==None:
                raise ValueError("需要验证码")
            else:
                pass
                # postdata["authcode"] = "3e96be222f1d4099b4ee9bc4737e0902"
        except:

            authcode_url = "https://iv.jd.com/slide/g.html?appId=1604ebb2287&scene=login&product=embed&e=7AQ7MFUYFZTRLN2WNWVDG7ERGHUIKQG6V5QNMASWLFHFM4F25HBD3GLWWHKL477C7P4NECRHO34MVOYWSDPVHJRCYI"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                "Referer":"https://passport.jd.com/new/login.aspx",

            }
            resp = self.__class__.s.get(authcode_url,headers=headers,verify=False).json()
            print(resp)
            with open("authcode.jpg","wb") as fp:
                fp.write(base64.urlsafe_b64decode(resp.get("bg")))
            with open("patch.jpg","wb") as fp:
                fp.write(base64.urlsafe_b64decode(resp.get("patch")))

            authCheck_url = "https://iv.jd.com/slide/s.html?d=0aC005wmjFMq8909g10t00011010000000000000004V000000000c101000000g000000000h000101000l101000000h000000000g000000000h101000000h000000000g101000000h102000000g104000000h105000000h103000000h106000000g107101000g105000000i104000000h103000000g103000000h102101000g102000000h102000000h102000000h102000000g102000000h103101000i102000000f102000000i101000000f000000000h101000000g101000000h000000000m000000000i000000000a101000000g000000000i101000000g101000000i102000000g102000000i102000000f102000000g102000000i102000000g102000000h101000000g000000000h101000000h000000000h000000000g000000000i101000000h000000000f101101000h101000000g102000000i102000000g102000000h102000000g102000000g103000000i101000000h101000000g101000000h000000000h101000000h000101000k000000000g000000000V101000000w000000000F000000000w000000000w101000000w000000000p000000000g000000000d101000000h000000000g000000000h101000000g102000000h101000000h103000000h101000000g101000000h101000000g101000000i101000000f101101000i000000000h101000000g000000000h000000000j000000000F101000000v000000000p000000000n000000000p000000000o101000000g000000000p000000000n000000000x101000000o000000000E000000000i000000000h101000000g000000000h000000000l000000000o101000000h000000000o000000000o000000000p101000000v000000000p000000000o000000000o000000000h000000000g101000000b000000000h000000000g000000000i101000000g101000000h000000000h101101000g000000000g101000000h000000000h101000000g000000000h101000000h000000000h000000000u000000000E101000000g000000000g000000000w0000000011101000000x000000000P000000000-00000000E2001000000b001002000g0000000003&c=989d2faca8e04dc6bf06b629a0ed8c44&w=272&appId=1604ebb2287&scene=login&product=embed&e=7AQ7MFUYFZTRLN2WNWVDG7ERGHUIKQG6V5QNMASWLFHFM4F25HBD3GLWWHKL477C7P4NECRHO34MVOYWSDPVHJRCYI&s=682335257219926914"
            b  =list()
            def st(d):
                reg = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~"
                e = d # 源码上是+d 不知道有什么区别
                l = len(reg)
                result = list()
                while(e):
                    mod = e % l
                    e = int((e-mod) / l)
                    result.append(reg[e])
                return "".join(result)


            def pm(d,c,b):
                e = st(abs(d))
                a = ""
                if not b:
                    a += "1" if d > 0 else "0"
                tmp = "".join(['0']*(c-1))+e
                a += tmp[-c:]

            c =  [["678", "352", 1532940427165],["84", "378", 1532940427165],["237", "20", 1532940427471],["237", "20", 1532940427490],["249", "56", 1532940427507],["257", "85", 1532940427541],["264", "142", 1532940427590],["264", "142", 1532940427801],["262", "142", 1532940427808],["261", "142", 1532940427824],["254", "148", 1532940427840],["244", "159", 1532940427857],["230", "174", 1532940427873],["213", "193", 1532940427891],["197", "214", 1532940427908],["190", "222", 1532940427925],["181", "234", 1532940427941],["172", "242", 1532940427958],["173", "242", 1532940428245],["174", "242", 1532940428257],["182", "243", 1532940428273],["191", "246", 1532940428290],["200", "249", 1532940428308],["206", "251", 1532940428326],["212", "253", 1532940428340],["217", "255", 1532940428356],["220", "256", 1532940428373],["223", "257", 1532940428389],["224", "257", 1532940428408],["224", "257", 1532940428423],["224", "258", 1532940428441],["224", "258", 1532940428458],["224", "258", 1532940428473],["224", "258", 1532940428495],["224", "259", 1532940428511],["224", "259", 1532940428528],["224", "259", 1532940428541],["223", "259", 1532940428557],["222", "259", 1532940428574],["221", "259", 1532940428591],["220", "259", 1532940428608],["219", "259", 1532940428623],["218", "259", 1532940428640],["217", "259", 1532940428658],["217", "259", 1532940428674],["217", "259", 1532940428691],["216", "259", 1532940428707],["216", "259", 1532940428725],["216", "259", 1532940428740],["216", "259", 1532940428758],["215", "260", 1532940428774],["215", "260", 1532940428819],["215", "260", 1532940428851],["215", "260", 1532940428858],["215", "260", 1532940428875],["215", "260", 1532940428890],["215", "260", 1532940428907],["214", "261", 1532940428924],["214", "261", 1532940428941],["214", "261", 1532940428958],["213", "261", 1532940428974],["213", "261", 1532940428991],["213", "261", 1532940429008],["212", "261", 1532940429025],["212", "262", 1532940429042],["210", "262", 1532940429058],["209", "263", 1532940429074],["208", "263", 1532940429091],["207", "263", 1532940429108],["206", "263", 1532940429123],["206", "263", 1532940429141],["206", "263", 1532940429157],["205", "263", 1532940429481],["205", "264", 1532940429491],["205", "264", 1532940429545],["205", "264", 1532940429570],["205", "264", 1532940429602],["205", "264", 1532940429642],["205", "264", 1532940429724],["204", "264", 1532940429771],["204", "264", 1532940429860],["204", "264", 1532940429875],["204", "264", 1532940429900],["204", "264", 1532940429933],["204", "264", 1532940429941],["203", "264", 1532940429965],["203", "265", 1532940429981],["203", "265", 1532940429991],["203", "265", 1532940431274]]
            for e in range(len(c)):
                if e == 0:
                    b.append(pm(c[e][0] if c[e][0] < 262143 else 262143, 3, True))
                    b.append(pm(c[e][1] if c[e][1] < 16777215 else 16777215, 4, True))
                    b.append(pm(c[e][2] if c[e][2] < 4398046511103 else 4398046511103, 7, True))
                else:
                    a = c[e][0] - c[e - 1][0]
                    f = c[e][1] - c[e - 1][1]
                    d = c[e][2] - c[e - 1][2]
                    b.append(pm(a if a < 4095 else 4095, 2, False))
                    b.append(pm(f if f < 4095 else 4095, 2, False))
                    b.append(pm(d if d < 16777215 else 16777215, 4, True))
            d = "".join(b)
            c = resp.get("challenge")
            w = 272
            appId = "1604ebb2287"
            scene = "login"
            product = "embed"
            e = postdata["eid"]
            s = postdata["seqSid"]
            resp = self.__class__.s.get("http://iv.jd.com/slide/s.html?d={0}&c={1}&w={2}&appId={3}&scene={4}&produce={5}&e={6}&s={7}".format(d,c,w,appId,scene,product,e,s),verify=False).json()
            print(resp)
            postdata["authcode"] = resp.get("validate")
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Referer": "https://passport.jd.com/new/login.aspx",
            "Content-Type":"application/x-www-form-urlencoded",
            "charset" : "UTF-8",
            "X-Requested-With":"XMLHttpRequest",
        }
        dologin_url = "https://passport.jd.com/uc/loginService?uuid={0}&&r={1}&version=2015".format(postdata["uuid"],np.random.rand())
        # cookies = "login_c=1; mp=17621064595; DeviceSeq=9b3922f1083b483c85f8da4c6aa553f8; user-key=6109b444-5159-491b-8bd7-b35188774ceb; cn=0; ipLoc-djd=1-72-2799-0; PCSYCityID=1381; __jdc=122270672; unpl=V2_bzNtbRVeEBdwC0NQeRtYV2JWFQ0SUUYcJg5CUHodXVAyUEAKclRCFXwUR1JnG10UZgUZWUtcQhVFCEdkfiksBWYCEV9HUUocRThFVEsRbAVjARFaR19GHHQJQ1V7GV4HYgMWWkRQcyVyOHYJI0YGQDNRSzNCZ0QQcg1DVXoQbARXAiIWLFYOFXEKRVN%2bEVkMZgIXXEJXQRdwCEJTfR5sBFcA; __jdv=122270672|nclick.linktech.cn|t_4_A100234788|tuiguang|f8b34245335c4d6aa748b755050ddbcf|1532908683834; __jdu=15329224981661119367710; pinId=jDozGbtvXq_QjwD949cXx7V9-x-f3wj7; pin=jd_650b4e54ab8df; unick=jd_176210gbt; _tp=XwY46hmX6kfF2RksEoLG8bRVbUPpa4V43JtszlWglgY%3D; _pst=jd_650b4e54ab8df; __jda=122270672.15329224981661119367710.1532922498.1532922498.1532930441.2; TrackID=1QVKMBRF-TaImFvqpKUi-g_FxHwQyvHMks3KT86_pLm0UIBGQMF8K9Cb6c25OmNn4Bze7nlDgJGJzwDgKhi3FipQwZvRwUXZd6Sj7Ptwm4JIXX75p-deNzAKzMMlnEHj-; shshshsID=8d2eba7d1dde9896d7f2d5a467004972_1_1532931388081; 3AB9D23F7A4B3C9B=7AQ7MFUYFZTRLN2WNWVDG7ERGHUIKQG6V5QNMASWLFHFM4F25HBD3GLWWHKL477C7P4NECRHO34MVOYWSDPVHJRCYI; alc=UASTNOBzjdAbpanfZeeS4g==; _t=jzBHBpMxQ4KQ/0nrWoI2Plu2QGJljT9AM3GdMQqekOM=; __jdb=122270672.11.15329224981661119367710|2.1532930441; wlfstk_smdl=jhqze3ph5ie12e6ymdbxbjmp3my19pzs"
        postdata1 = "uuid={0}&eid={1}&fp={2}&_t={3}&loginType={4}&loginname={5}&nloginpwd={6}&pubKey={7}&sa_token={8}&seqSid={9}&useSlideAuthCode={10}".format(
            postdata["uuid"],
            postdata["eid"],
            postdata["fp"],
            postdata["_t"],
            postdata["loginType"],
            postdata["loginname"],
            postdata["nloginpwd"],
            # "1321312312",
            postdata["pubKey"],
            postdata["sa_token"],
            postdata["seqSid"],
            postdata["useSlideAuthCode"]
        )
        print(self.__class__.s.cookies)
        resp = self.__class__.s.post(dologin_url,headers=headers,data=postdata1,verify=False)
        print(resp.text[:100])
        target = "https://order.jd.com/center/list.action"
        resp = requests.get(target,verify=False,cookies = resp.cookies)
        print(resp.url)

    def test(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Referer": "https://passport.jd.com/new/login.aspx",
        }
        postdata = ""
        dologin_url = "https://passport.jd.com/uc/loginService?uuid={0}&&r={1}&version=2015".format(postdata["uuid"],
                                                                                            np.random.rand())
        resp = self.__class__.s.post(dologin_url, headers=headers, data=postdata, verify=False)
        print(self.__class__.s.cookies)
        target = "https://order.jd.com/center/list.action"
        resp = requests.get(target, verify=False, cookies=resp.cookies)
        print(resp.text)

if __name__=="__main__":
    JD().login()