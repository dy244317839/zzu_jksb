#coding=utf-8


## 请自行填写user_data中前四行对应数据，以及mail模块中需要的邮箱设置
## 多用户打卡的话，只需在user_data里，复制添加新字典即可
import urllib
import json
import requests
import re
from bs4 import BeautifulSoup
import sendmail
import time
from smtplib import SMTP_SSL
import sys


host = 'jksb.v.zzu.edu.cn'
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            
            'Host':host}
hea1 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
            'Referer':"https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0",
            'Host':host}
hea2 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
            'Referer':"https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb",
            'Host':host}
hea3 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
            'Host':host}

jksb_data = {
    'day6': '',
    'did': '',
    'door':'' ,
    'men6': '',
    'ptopid': '',
    'sid': ''
}

# verify_path = "/etc/ssl/certs"
verify_path = False
class jksb:
    def __init__(self,user_data,post_data,submit_data):
        self.user_data = user_data
        self.post_data = post_data
        self.submit_data = submit_data

    # 获取post请求中的ptopid和sid
    def re_id(self,url): 
        # data = url.text
        data = ''.join(url)
        # print(data)
        data = data.split('=')
        sid = data[2]
        ptopid = data[1].split('&')
        ptopid = ptopid[0]
        self.submit_data['ptopid'] = ptopid
        self.submit_data['sid'] = sid
    
    def re_url(self,html):
        html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
        
        html = html.text
        soup1 = BeautifulSoup(html,'lxml')
        datas = soup1.find('script')
        datas = datas.string
        pattern = re.compile(r'window.location="(http.*?)"', re.I | re.M)
        url = pattern.findall(datas)
        return url

    def re_url1(self,html):
        html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
        html = html.text
        soup1 = BeautifulSoup(html,'lxml')
        datas = soup1.find('iframe')
    
        url = datas['src']
        return url

    # 判断今日是否填报过
    def re_content(self,html):
        html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
        html = html.text
        soup1 = BeautifulSoup(html,'lxml')
        
        datas = soup1.find('span')
        datas = datas.string
        datas.encoding = 'utf-8'

        if datas=="今日您已经填报过了":
            return False
        else:
            post_data = soup1.findAll('input')
            res = []
            for data in post_data:
                res.append(data['value'])
            jksb_data['day6'] = res[0]
            jksb_data['did'] = res[1]
            jksb_data['door'] = res[2]
            jksb_data['men6'] = res[3]
            jksb_data['ptopid'] = res[4]
            jksb_data['sid'] = res[5]
            self.submit_data['day6'] = jksb_data['day6']
            self.submit_data['door'] = jksb_data['door']
            self.submit_data['men6'] = jksb_data['men6']
            return True
    def post_url(self):
        session = requests.Session()
        html = session.post('https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login',  data = self.post_data,headers = hea1,verify = verify_path)
        url = self.re_url(html)
        print(url)
        if len(url)>0:
            self.re_id(url[0])
            return url[0]
        else:
            return 0
    def get_url1(self,url):
        session = requests.Session()
        html = session.get(url,headers = hea,verify = verify_path)
        url = self.re_url1(html)
        if len(url)>0:
            return url
        else:
            return 0
    def get_url2(self,url):
        session = requests.Session()
        html = session.get(url,headers = hea,verify = verify_path)
        return self.re_content(html)
    def jksb(self):
        url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
        session = requests.Session()
        html = session.post(url,data = jksb_data, headers = hea3,verify = verify_path)
        html = session.post(url,data = self.submit_data,headers = hea2,verify = verify_path)
        html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
        html = html.text
        soup1 = BeautifulSoup(html,'lxml')
        content = soup1.find('div',style="width:296px;height:100%;font-size:14px;color:#333;line-height:26px;float:left;")
        return content.string
