#-*-coding:utf-8-*-

'''
使用 requests 和正则抓取猫眼电影 TOP100写入至文件中
'''

import requests
from requests.exceptions import RequestException
import re
import json
import time


headers = {
        "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Language":'zh-CN,zh;q=0.9,la;q=0.8',
        "Cookie":'_lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic; uuid=1A6E888B4A4B29B16FBA1299108DBE9C6BCE05C9F432B679498134DA40E12047; _csrf=c48e1e9f134391deb436105ab219b41cb950e6b9f99d21c60511baf48bae5bc1; __mta=222696100.1516282706197.1520682241046.1520682891401.23; _lxsdk_s=9dbcc78b3a618fa8b40a2ce874bc%7C%7C2',
        "Host":'maoyan.com',
        "Proxy-Connection":'keep-alive',
        "Referer":'http://maoyan.com/board',
        "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}


#获取单个页面代码
def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        return None
    except RequestException:
        return None

#解析页面并以字典形式存储
def parse_one_page(result):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?<img data-src="(.*?)".*?<a.*?>(.*?)</a>.*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(\d+)</i>.*?</dd>',re.S)
    re_html = re.findall(pattern,result)
    # return re_html
    for item in re_html:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip(),
            'time':item[4],
            'score':item[5] + item[6]
        }

#写文件
def write_data(data):
    with open('top_100.txt','a',encoding='UTF-8') as file:
        file.write(json.dumps(data,ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        # print(item)
        write_data(item)

        
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        # time.sleep(2)
