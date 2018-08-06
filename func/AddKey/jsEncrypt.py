# coding:utf8

class ASN1:
    def __init__(self):
        pass
    @staticmethod
    def decode(b6):
        newB6 = dict()
        newB6["enc"] = b6
        newB6["pos"] = 0
        b5 = b6
        b8 = newB6.get("enc")[newB6.get("pos")]
        newB6["pos"] += 1
        b3 = newB6.get("enc")[newB6.get("pos")]
        newB6["pos"] += 1
        bZ = b3 & 127
        if bZ ==b3:
            return bZ
        if bZ>3:
            raise ValueError("又error了。。。")
        if bZ ==0:
            return -1
        b3 = 0
        for b1 in range(bZ):
            b3 = (b3 << 8) | newB6.get("enc")[newB6.get("pos")]
            newB6["pos"] += 1
        b2 = b6.get("pos") - b5.get("pos")
        bZ = None


class bx():
    def __init__(self,publicKey):
        if publicKey:
            if isinstance(publicKey,str):
                self.parseKey(publicKey)
            else:
                print("???")

    def parseKey(self,publicKey):
        try:
            b6 = 0
            bW = 0
            b5 = self.decode(publicKey)
            b6 = ASN1.decode(b5)
        except Exception as err:
            print("error?",err)

    def decode(self,key):
        bY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        b3 ="= \f\n\r\t\u00A0\u2028\u2029"
        L = dict()
        for bZ in range(64):
            L[bY[bZ]] = bZ
        for bZ in range(len(b3)):
            L[b3[bZ]] = -1
        bX = list()
        b0 =0
        b2 =0
        newKey = list()
        for bZ in range(len(key)):
            if key[bZ] == "=":
                break
            newKey.append(L.get(key[bZ]))
            if newKey[bZ] == -1:
                continue
            b0 |= newKey[bZ]
            b2 +=1
            if b2>=4:
                bX.append((b0>>16))
                bX.append((b0>>8) & 255)
                bX.append(b0 & 255)
                b0 = 0
                b2 = 0
            else:
                b0 <<= 6

        if b2==1:
            raise ValueError("永远不可能来到的错误")
        elif b2 ==2:
            bX.append(b0 >> 10)
        elif b2 == 3:
            bX.append(b0 >> 16)
            bX.append((b0 >> 8) & 255)
        return bX

class JsEncrypt(object):

    default_key_size = 1024
    default_public_exponent = '010001'
    log = False
    key = None
    t = {}

    def __init__(self):
        pass

    def SetPublicKey(self,publicKey):
        if self.__class__.log and self.__class__.key:
            raise ValueError("已经存在key")
        self.__class__.key = bx(publicKey)

    def encrypt(self,pwd):
        return "加密后的结果"

if __name__=="__main__":
    publicKey ="MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5laljaN9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7PAzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQq+CA6agNkqly2H4j6wIDAQAB"
    bx(publicKey)