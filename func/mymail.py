#coding=utf-8
import smtplib,time,os,sys
from email.mime.text import MIMEText
from email.header import Header
from func.echarts.myecharts import createPic
class MyMail:
    def __init__(self,server,user,passwd,tfrom,tto):
        self.user = user
        self.passwd = passwd
        self.smtpserver = server
        self.lfrom = tfrom
        self.lto = tto
        self.msg = None
        print(format("发送方：{0}".format(tfrom),"-<50"))
        print(format("接收方：{0}".format(tto),"-<50"))

    def createHeader(self,subject):
        self.createContent()
        print(format("开始构造邮件Header", "=^50"))
        self.msg["subject"] = Header(subject,"utf-8")
        self.msg["From"] = self.lfrom
        self.msg["To"] = self.lto

    def createContent(self):
        print(format("开始构造邮件内容","=^50"))
        mail_body = """
       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
            <title>获取地理位置</title>
            <style type="text/css">#iCenter{width:300px; height: 280px; border:1px #000 solid;margin:20px auto;}</style>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/echarts/4.1.0/echarts.js"></script>
        </head>
        <body>
        
        <p id="location"></p>
        <table border="1">
            <tbody>
                <tr>
                    <td rowspan="2">店号</td>
                    <td rowspan="2">店名</td>
                    <td colspan="4" align="center">鲜食</td>
                </tr>
                <tr>
                    <td>三明治</td>
                    <td>数量</td>
                    <td>饭团</td>
                    <td>数量</td>
                </tr>
                <tr>
                    <td>117001</td>
                    <td>xxxx店</td>
                    <td>2087971</td>
                    <td>10</td>
                    <td>2087971</td>
                    <td>10</td>
                </tr>
                <tr>
                    <td>117002</td>
                    <td>xyxx店</td>
                    <td>2087990</td>
                    <td>12</td>
                    <td>2087971</td>
                    <td>10</td>
                </tr><tr>
                    <td>117003</td>
                    <td>zzzx店</td>
                    <td>2087976</td>
                    <td>1</td>
                    <td>2087971</td>
                    <td>10</td>
                </tr>
            </tbody>
        </table>
        <div id="pic1" style="width: 600px;height:400px;display: none;">
            <img src="{0}"/>
        </div>
        </body>
        </html>
        """.format("./echarts/pic1.png")
        self.msg = MIMEText(mail_body,_subtype="html",_charset="utf-8")

    def work(self):
        print(format("发送邮件", "=^50"))
        self.createHeader("大数据鲜食订购组周通报")
        smtp = smtplib.SMTP_SSL(self.smtpserver,465)
        try:
            smtp.login(self.user,self.passwd)
            smtp.sendmail(self.lfrom,self.lto,self.msg.as_string())
        except Exception as err:
            print(err)
            print(format("邮件发送失败","&^50"))
        else:
            print(format("邮件发送成功","*^50"))
        finally:
            smtp.quit()


if __name__ == "__main__":

    a = MyMail(server="smtp.mxhichina.com",user="bi_dds@today36524.com.cn",passwd="Today36524",tfrom="bi_dds@today36524.com.cn",tto ="wxu-3@today36524.com.cn")
    a.work()