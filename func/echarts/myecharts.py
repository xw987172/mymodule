#coding:utf-8

from pyecharts import Bar
import sys,os,time
import importlib
def createPic(picType,title,subtitle,content,file):
        m = __import__("pyecharts")
        c = getattr(m,picType)
        b = c("我的第一个图标","这是副标题")
        for subject,name,vals in content:
                b.add(subject,name, vals,is_more_utils=True)
        b.render(path=file,pixel_ratio=len(content))