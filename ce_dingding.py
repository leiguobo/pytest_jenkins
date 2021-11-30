import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import warnings
import datetime

warnings.filterwarnings("ignore")

nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
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
url3='https://v1.hitokoto.cn/?c=j&encode=json'

r3=requests.get(url3,verify=False)
wangyiyun=r3.json().get("hitokoto")

url4='https://v1.hitokoto.cn/?c=d&encode=json'
r4=requests.get(url4,verify=False)
wenxue=r4.json().get("hitokoto")

# print(r2.text)
city=r2.json().get("result").get("city")
temperature=r2.json().get("result").get("realtime").get("temperature")
realtime=r2.json().get("result").get("realtime").get("info")
direct=r2.json().get("result").get("realtime").get("direct")
power=r2.json().get("result").get("realtime").get("power")
aqi=r2.json().get("result").get("realtime").get("aqi")
humidity=r2.json().get("result").get("realtime").get("humidity")
weather=r2.json().get("result").get("realtime").get("info")

future_temperature=r2.json().get("result").get("future")[0].get("temperature")
future_direct=r2.json().get("result").get("future")[0].get("direct")
future_date=r2.json().get("result").get("future")[0].get("date")
future_weather=r2.json().get("result").get("future")[0].get("weather")

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
     "msgtype": "markdown",
     "markdown": {
         "title":"今日{}天气".format(city),
         "text": "#### 今日{}天气 \n > {}度，{}，{}{}，空气质量指数{}，相对湿度{}% \n**{}** \n > ###### {}发布 [中国天气网](http://www.weather.com.cn/) \n ".format(city,temperature,weather,direct,power,aqi,humidity,wangyiyun,nowtime)
     },
      "at": {
          "atMobiles": [
              "150XXXXXXXX"
          ],
          "atUserIds": [
              "user123"
          ],
          "isAtAll": False,
      }
 }
#图片![screenshot](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fy0.ifengimg.com%2Fnews_spider%2Fdci_2012%2F08%2F91dd6d6f0d8e13b09dddb62d0085f330.jpg&refer=http%3A%2F%2Fy0.ifengimg.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1640849354&t=4745797ed29c98fdd165676f6ca712dd)
body={
     "msgtype": "markdown",
     "markdown": {
         "title":"明日{}天气".format(city),
         "text": "#### 明日{}天气 \n > {}，{}，{} \n**{}** \n > ###### {}发布 [中国天气网](http://www.weather.com.cn/) \n ".format(city,future_temperature,future_weather,future_direct,wenxue,future_date)
     },
      "at": {
          "atMobiles": [
              "150XXXXXXXX"
          ],
          "atUserIds": [
              "user123"
          ],
          "isAtAll": False,
      }
 }
r2=requests.post(url,headers=headers,json=body2,verify=False)
r=requests.post(url,headers=headers,json=body,verify=False)

