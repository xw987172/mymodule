# coding: utf8
'''
__author__ :xw
__info__ : 天眼查验证码识别
'''
import time,math,requests,base64,sys
from PIL import Image
import pytesseract
import numpy as np
import pygame
from func.mymath import mymathclass

class tyc:

    def __init__(self):
        self._getPicTarget()
        self.createImages()

    def _getPicTarget(self):
        '''
        获取图片数据
        :return: 
        '''
        timestamp = math.floor(1000*time.time())
        url = "https://antirobot.tianyancha.com/captcha/getCaptcha.json?t={0}&_={1}".format(timestamp,timestamp-5)
        try:
            info = requests.get(url).json()
        except:
            print("error")
            while(1):
                self._getPicTarget()
        else:
            self.targetImage = info.get("data").get("targetImage")
            self.bgImage = info.get("data").get("bgImage")

    def createImages(self):
        '''
        把base64字符串 转成图片保存下来
        :return: 
        '''
        def image(name,data):
            imgdata = base64.b64decode(data)
            with open(name+".png","wb") as op:
                op.write(imgdata)
        for name,data in [("target",self.targetImage),("background",self.bgImage)]:
            image(name,data)

    def recoword(self,file):
        im = Image.open(file)
        print(im.size)
        data = list()
        for h in range(0,im.size[1]):
            data.append(list())
            for w in range(0,im.size[0]):
                data[h].append(im.getpixel((w, h)))
        # 切分像素点
        result = list()
        num =0
        for i in range(0,im.size[0]):
            newList = [x[i] for x in data]
            newList = set(newList)
            if len(newList)==1:
                continue
            else:
                result.append(i)
        spit = list()
        num =0
        for idx,val in enumerate(result):
            if len(spit) == num:
                spit.append(list())

            spit[num].append(val)
            if idx<=len(result)-2 and val+1!= result[idx+1]:
                num +=1
        spit = list(filter(lambda x:len(x)>6 , spit))
        shape1 = [0,0,1,im.size[1]]  # x0,y0,x1,y1
        shape1[0] = spit[0][0]
        shape1[2] = spit[0][-1]
        region = im.crop(shape1)
        region.save("spit.png")
        # words = dict()
        # for i,val in enumerate(spit):
        #     words[i] = [[data[j][k] for k in val] for j in range(0,im.size[1])]


    def match(self):
        im = Image.open("spit.png")
        normal = im.getpixel((0, 0))
        data = list()
        a,b = im.size
        for h in range(0, b):
            for w in range(0, a):
                try:
                    a1, b1, c1 = im.getpixel((h, w))
                    if abs(a1 - normal[0]) + abs(b1 - normal[1]) + abs(c1 - normal[2]) < 10:
                        data.append(0)
                    else:
                        data.append(1)
                except:
                    pass
        im2 = Image.open("background.png")
        max = 100
        x,y =0,0
        for h in range(0, im2.size[1]-b+1):
            for w in range(0, im2.size[0]-a+1):
                bdata = list()
                for h1 in range(0,b):
                    for w1 in range(0,a):
                        try:
                            a1,b1,c1 = im2.getpixel((h+h1,w+w1))
                            if abs(a1-normal[0])+abs(b1-normal[1])+abs(c1-normal[2])<10:
                                bdata.append(0)
                            else:
                                bdata.append(1)
                        except:
                            pass
                try:
                    cor = mymathclass.ouDistance(data, bdata)
                except Exception as e:
                    cor = 0
                if cor<max:
                    max = cor
                    x = h
                    y = w
        print(max)
        shape = [y,x,y+a,x+b]
        print(shape)
        region = im2.crop(shape)
        region.save("result.png")

    @staticmethod
    def createcharpics():
        dir = "/Users/xuwei/chinese/"
        import os
        try:
            os.makedirs(dir)
        except:
            print("已经存在...")
        pygame.init()
        start, end = (0x4E00, 0x9FA5)
        for codepoint in range(int(start),int(end)):
            word = chr(codepoint)
            print(word)
            font = pygame.font.Font("msyh.ttf", 64)
            rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))
            pygame.image.save(rtext, os.path.join(dir, word + ".png"))



    def __str__(self):
        return self.targetImage+"\n"+self.bgImage

if __name__=="__main__":

    a=tyc()
    a.recoword("target.png")
    a.match()