import requests
import json
import pymongo
import schedule
import time
import signal
import sys


#强制退出不报错
def Quit(signum, frame):
    print("Quit")
    sys.exit()


signal.signal(signal.SIGINT, Quit)
signal.signal(signal.SIGTERM, Quit)


#这里填写appid和secret
appid = ""
secret = ""


#获取access_token
def access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid, secret)

    r = requests.get(url)

    json = r.json()

    token = json["access_token"]

    #读取access_token，写入txt文档
    fb = open('access_token.txt', 'w', encoding='utf-8')
    fb.write(token)


# access_token()


#这里获取用户的appid，填入一次发送一次，appid来自自己的数据库
def message(touser):
    for token in open('access_token.txt'):
        url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + token

    #模板id填自己申请的id，字段名称都要对应
    body = {
        "touser": touser,
        "template_id": "kuyJzYVUJNgWGNRa31-eR5KdEdvZtWBlqF2XDbs3BtE",
        "page": "pages/index/index",
        "lang":"zh_CN",
        "data": {
            "thing1": {
                "value": "每日刷题"
            },
            "thing7": {
                "value": "政治考研"
            },
            "thing5": {
                "value": "每天刷题，每天进步"
            }
        }
    }

    response  = requests.post(url, json = body)
    return response

# message(touser)

#读取mongodb中的openid，调用message()函数发送，这里可以根据自己的数据库来写
def mongo():
    myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
 
    dblist = myclient.list_database_names()

    mydb = myclient["examination"]
    mycol = mydb["user"]

    #循环遍历数据库中的openid，每遍历出来一个，就放进message方法里发送一次，遍历完之后，就给所有用户发送了
    for x in mycol.find({},{ "_id": 0, "openid": 1}):
        message(x['openid'])


# mongo()


#用schedule设置执行时间
if __name__ == '__main__':
    #这一句的意思是每天22：20获取一次access_token
    schedule.every().day.at("22:20").do(access_token)
    #这句的意思是，每天的21：30，发送一次订阅消息
    schedule.every().day.at("22:30").do(mongo)
    while True:
        schedule.run_pending()
        time.sleep(1)