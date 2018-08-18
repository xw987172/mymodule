# coding :utf8
'''
操作windows桌面，获取桌面信息
'''
import win32api
import win32api
import win32gui
title = set()

hwnd = win32gui.FindWindow("Chrome_WidgetWin_1","用C/C++实现较完整贪吃蛇游戏 - CSDN博客 - Google Chrome")
print(hwnd)