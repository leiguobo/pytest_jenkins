import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import warnings

warnings.filterwarnings("ignore")

timestamp = str(round(time.time() * 1000))
secret = 'SEC33069fdeded6911c982afa2a1637afc94483f467e3e6ec99d208743166e1eff6'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
# print(timestamp)
# print(sign)
url2='http://apis.juhe.cn/simpleWeather/query?city=%E8%A5%BF%E6%B9%96&key=0383967f2621fd1d834191f831d3c47a'
r2=requests.post(url2,verify=False)
print(r2.json())
city=r2.json().get("result").get("city")
temperature=r2.json().get("result").get("realtime").get("temperature")
realtime=r2.json().get("result").get("realtime").get("info")




url='https://oapi.dingtalk.com/robot/send?access_token=fd58bef56ad92cb55abb2cc34209d25efe05b136eb06393d3f03e2d9958067d0&timestamp=%s&sign=%s'%(timestamp,sign)
headers = {
    'Content-Type': 'application/json'
}
# body={
#     "msgtype": "text",
#     "text": {
#           "content":[{
#               '':"今日天气",
#               '城市':r2.json().get("result").get("city"),
#               '温度':r2.json().get("result").get("realtime").get("temperature"),
#               '天气状况':r2.json().get("result").get("realtime").get("info"),
#           },
#               {'':"明日天气",
#               '城市':r2.json().get("result").get("city"),
#               '温度':r2.json().get("result").get("future")[0].get("temperature"),
#               '天气状况':r2.json().get("result").get("future")[0].get("weather"),}
#           ]}
#           }

body2={
    "msgtype": "text",
    "text": {
          "content":{
               "text":"今日天气\n城市：%s\n温度：%s\n天气状况：%s"%(city,temperature,realtime)
          }
          }}
r=requests.post(url,headers=headers,json=body2,verify=False)
print(r.text)

