import hashlib
import urllib
import random
import json
import http.client




def translate(txt):
    myurl = 'https://translate.google.cn/?sl=auto&tl=zh-CN&text={}'.format(txt)

    httpClient = None

    try:
        httpClient = http.client.HTTPConnection('translate.google.cn')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        return json.loads(result_all)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


t = translate('yes')
print(t)