import hashlib
import urllib
import random
import json
import http.client


def show(message: str, max_size: int):
    """
    英文排版转换
    :param message:
    :param max_size:
    :return:
    """
    words = message.split()
    step = 0
    out = []
    t = []
    for word in words:
        this_len = len(word)
        step += this_len
        t.append(word)
        if step > max_size:
            out.append(' '.join(t))
            t = []
            step = 0
    out.append(' '.join(t))
    return '\n'.join(out)


def ch_show(message: str, max_size: int):
    """
    中文排版转换
    :param message:
    :param max_size:
    :return:
    """
    size = len(message)
    n = size // max_size
    out = []
    for i in range(n):
        out.append(message[i * max_size: i * max_size + max_size])
    out.append(message[n * max_size:])
    return '\n'.join(out)


html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>TSTK</tit' \
       'le></head><body style="font-size: 1.6em;"><div STYLE="width: 80%;height:40px;text-align:' \
       ' center; margin-left: 10%;margin-top:10px;background-color: #bf242a;padding-top: 10px;color' \
       ': #fff"><a style="text-decoration: none;color:#fff" href="https://space.bilibili.com/299973729" ' \
       'target="_blank">TSTK 翻译工具</a></div><div STYLE="width: 80%; margin-left: 10%; ' \
       'margin-top: 30px; text-indent: 50px">{}</div><div STYLE="width: 80%;text-indent: 50px; margin-' \
       'left: 10%;margin-top: 10px;border-top-color: red; border-top-style: solid; padding-top: 10px">' \
       '{}</div></body></html>'


def translate(message: str, appid, secretKey):
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'zh'
    httpClient = None
    salt = random.randint(32768, 65536)
    q = message
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', url)
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        return json.loads(result_all)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def extract_result(message, appid, secretKey):
    p = translate(message, appid, secretKey)
    return p.get('trans_result', [{'src': ' ', 'dst': ' '}])[0]['dst']
