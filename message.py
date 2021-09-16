import json    # 用于存储和信息交换的库
import requests   # 导入HTTP库
import threading   # 导入线程库

class WeChat():   # 定义类

    def __init__(self, appId, appSecret):
        self.appId = appId
        self.appSecret = appSecret

    def getAccessToken(self):
        # 1.获取accessToken, (access_token 相当于一把钥匙，调用接口凭证)
        # https请求方式: GET
        # https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appId}&secret={self.appSecret}'   # 绑定url
        resp = requests.get(url).json()   # 得到的数据是json形式的，所以直接通过json去调用
        accessToken = resp.get('access_token')   # 接收的数据是字典形式，通过key去取得它的值
        return accessToken   # 返回已处理的值

    def sendMessage(self, opendId, message):
        # 2.利用accessToken来发送微信的通知
        # http请求方式: POST
        # https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN
        url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.getAccessToken()}'   # 绑定url
        requestsData = {
            "touser": opendId,   # 传入自己的openId
            "msgtype": "text",   # text表示要发送的是文本
            "text":
                {
                    "content": message   # message表示发送的数据
                }
        }

        requestsString = json.dumps(requestsData, ensure_ascii=False)   # 将字典的数据转换成字符串发送,定义不把中文转换为ASCII码
        requestsData = requestsString.encode('utf-8')   # 使用ASCII编码把字符串编译成二进制的数据
        requests.post(url, data=requestsData)   # 发送数据

appId = 'wxd91bf30880814e6b'   # 测试号ID
appSecret = 'd794e68c23b7428dce04189518b2baba'   # 测试号秘钥
opendId = 'o6mI260g-G4OUM1XZupLTePa3VhQ'   # openId为发送给谁
message = "人脸匹配成功,门已开启!"   # 定义要发送的数据

weChatTools = WeChat(appId, appSecret)  # 传入自己的ID和秘钥
weChatTools.sendMessage(opendId, message)  # 发送数据

def ready():
    weChatTools = WeChat(appId, appSecret)   # 传入自己的ID和秘钥
    weChatTools.sendMessage(opendId, message)   # 发送数据

def send():
    demo = threading.Thread(target=ready)   # 创建一个多线程对象
    demo.start()   # 开启多线程
