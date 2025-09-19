import requests
import json
import os

def send_wechat_message():
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=deb5014d-2b07-4540-93e2-51a93afcd9b2"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "中秋节礼品领取",
                    "description": "今年中秋节公司有豪礼相送",
                    "url": "fleamarket://awesome_detail?id=968729830637&flutter=true",
                    "picurl": "http://img.alicdn.com/bao/uploaded/i4/O1CN01910VoY1JOIGlIUGI9_!!4611686018427379946-0-fleamarket.jpg"
                }
            ]
        }
    }

    try:
        os.environ['no_proxy'] = '*'
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an HTTPError for bad responses
        result = response.json()
        if result.get("errcode") == 0:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {result.get('errmsg')}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    send_wechat_message()