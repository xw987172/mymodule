#coding=utf-8
import smtplib,time,os,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from func.echarts.myecharts import createPic
from func.myhive import myhiveclass,myconf
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
            <title>鲜食订购周通报</title>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/echarts/4.1.0/echarts.js"></script>
        </head>
        <body>
        
        <p>各位：<br/>
        {0}-{1}鲜食商品订销比、报损率周通报如下：<br/><br/>
        </p>
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
        <div id="pic1" style="width: 600px;height:400px;">
            下面应该有图片
            <img src="cid:imageid" alt="imageid"/>
        </div>
        </body>
        </html>
        """
        self.msg = MIMEMultipart("related")
        content = MIMEText(mail_body,_subtype="html",_charset="utf-8")
        self.msg.attach(content)

        img_data = open("./pic1.png","rb").read()
        img = MIMEImage(img_data)
        img.add_header("Content-ID","imageid")
        self.msg.attach(img)

    def createTable(self,sql):
        '''
        创建html中的table
        :param sql:
        :return:
        '''


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