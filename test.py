

import requests
import json
from urllib import parse

# 定义请求header
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Key': '332213fa4a9d4288b5668ddd9'}
# 定义请求地址
url = "http://192.168.52.38:5102/translator/translate"
# 通过字典方式定义请求body
FormData = {"src_text": 'hello world'}
# 字典转换k1=v1 & k2=v2 模式 
data = parse.urlencode(FormData)
# 请求方式
content = requests.post(url=url, headers=HEADERS, data=data).text
content = json.loads(content)
print(content)