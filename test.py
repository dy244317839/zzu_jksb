#coding = utf-8
import os
import configparser
import sendmail
import json

# email = sendmail.mail()
# email.mail("haha","1647757891@qq.com")
json_filename = './post_data.json'
post_data = {}
post_data['uid'] = ''
post_data['upw'] = ''
post_data['smbtn'] = '进入健康状况上报平台'
post_data['hh28'] = '686'
with open(json_filename,'w',encoding='UTF-8') as f:
    json.dump(post_data,f)
with open(json_filename,encoding='UTF-8') as f:
    test = json.load(f)
    print(test)

#print(submit_data['myvs_13a'])
# proDir = os.path.split(os.path.realpath(__file__))[0]
# configPath = os.path.join(proDir,"config.ini")
# parser = configparser.ConfigParser()
# parser.read(configPath,encoding='UTF-8')
# send_mail = {}
# send_mail = parser.items('sendmail')
# host_server = send_mail[0][1]
# print(send_mail[0][1])
# print(parser.get("userdata",'username'))