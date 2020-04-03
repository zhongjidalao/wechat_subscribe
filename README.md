## 微信订阅消息

填入自己的appid和secret

下面openid部分的代码需要自己写，我只是举了一个mongodb的例子，这里可以使用任何数据库，只要能遍历出来用户的openid并调用message()发送就可以了。

### 在服务器上后台运行

```shell
nohup python3 send_message.py &
```

### 第三方库

- pymongo
- schedule

