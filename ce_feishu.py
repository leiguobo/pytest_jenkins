import hashlib
import base64
import hmac
import requests
import time,datetime
import warnings

nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
warnings.filterwarnings("ignore")
current_milli_time = lambda: int(round(time.time()))
timestamp=current_milli_time()
secret='rUMtjwlEKhIXTvmP0WhHch'
# secret='SEC33069fdeded6911c982afa2a1637afc94483f467e3e6ec99d208743166e1eff6'


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

def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')


    return sign

url='https://open.feishu.cn/open-apis/bot/v2/hook/99688f66-bff9-4b22-85a9-c62db61a5078'

headers = {
    'Content-Type': 'application/json'
}
# body={
#         "timestamp": timestamp,
#         "sign": gen_sign(timestamp, secret),
#         "msg_type": "text",
#         "content": {
#                 "text": "request example"
#         }
# }


body2={
    "timestamp": timestamp,
    "sign": gen_sign(timestamp, secret),
    "msg_type": "interactive",
    "card": {
        "config": {
                "wide_screen_mode": True,
                "enable_forward": True
        },
        "elements": [{
                "tag": "div",
                "text": {
                        "content": "{}度，{}，{}{}，空气质量指数{}，相对湿度{}% \n **{}** \n {}发布\n ".format(temperature,weather,direct,power,aqi,humidity,wangyiyun,nowtime),
                        "tag": "lark_md"
                }
        }, {
                "actions": [{
                        "tag": "button",
                        "text": {
                                "content": "中国天气网",
                                "tag": "lark_md"
                        },
                        "url": "http://www.weather.com.cn/",
                        "type": "default",
                        "value": {}
                }],
                "tag": "action"
        }],
        "header": {
                "title": {
                        "content": "今日{}天气".format(city),
                        "tag": "plain_text"
                }
        }
    }
}


body={
    "timestamp": timestamp,
    "sign": gen_sign(timestamp, secret),
    "msg_type": "interactive",
    "card": {
        "config": {
                "wide_screen_mode": True,
                "enable_forward": True
        },
        "elements": [{
                "tag": "div",
                "text": {
                        "content": "{}，{}，{} \n**{}** \n {}发布\n ".format(future_temperature,future_weather,future_direct,wenxue,future_date),
                        "tag": "lark_md"
                }
        }, {
                "actions": [{
                        "tag": "button",
                        "text": {
                                "content": "中国天气网",
                                "tag": "lark_md"
                        },
                        "url": "http://www.weather.com.cn/",
                        "type": "default",
                        "value": {}
                }],
                "tag": "action"
        }],
        "header": {
                "title": {
                        "content": "明日{}天气".format(city),
                        "tag": "plain_text"
                }
        }
    }
}


r=requests.post(url,headers=headers,json=body2,verify=False)
r2=requests.post(url,headers=headers,json=body,verify=False)

print(r.text)
