import hashlib
import base64
import hmac
import requests
import time
import warnings

warnings.filterwarnings("ignore")
current_milli_time = lambda: int(round(time.time()))
timestamp=current_milli_time()
# secret='rUMtjwlEKhIXTvmP0WhHch'
secret='SEC33069fdeded6911c982afa2a1637afc94483f467e3e6ec99d208743166e1eff6'

def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')


    return sign

# url='https://open.feishu.cn/open-apis/bot/v2/hook/99688f66-bff9-4b22-85a9-c62db61a5078'
url='https://oapi.dingtalk.com/robot/send?access_token=fd58bef56ad92cb55abb2cc34209d25efe05b136eb06393d3f03e2d9958067d0'
headers = {
    'Content-Type': 'application/json'
}
body={
        "timestamp": timestamp,
        "sign": gen_sign(timestamp, secret),
        "msg_type": "text",
        "content": {
                "text": "request example"
        }
}
r=requests.post(url,headers=headers,json=body,verify=False)
print(r.text)
