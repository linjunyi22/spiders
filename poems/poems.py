# 抓诗词

import requests
import re
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient


client = MongoClient('localhost',27017)
mydb = client['mydb']
poems = mydb['poems']

# 获取诗词类别url
def category(url,headers):
	categories_url = []
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	categories = soup.select('div.main3 > div.right > div.sons > div.cont')
	for item in categories:
		link = item.select('a') # 获取a 标签		
		for i in link:
			c_url = i.get('href') # 获取链接
			categories_url.append('https://www.gushiwen.org'+c_url) # 类别 url
	return categories_url


# 获取页面内容
def get_one_page(url, headers):
	poems_box = []
	r = requests.get(url,headers)
	soup = BeautifulSoup(r.text, 'lxml')
	poems = soup.select('div.left > div.sons')[0].select('.cont')

	# 正则切割内容
	for item in poems:
		poem = item.select('a')[0].get_text()
		title = re.findall(r'《.*?》', item.select('a')[1].get_text())[0]
		author = re.findall(r'(.*?)《', item.select('a')[1].get_text())[0]
		data = {
			'poem' : poem,
			'title' : title,
			'author': author
		}
		poems_box.append(data)
	return (poems_box)
		

if __name__ == '__main__':
	url = 'https://www.gushiwen.org/shiju/'
	headers = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'zh-CN,zh;q=0.9,la;q=0.8',
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
	}

	for url in category(url,headers):
		for i in get_one_page(url,headers):
			poems.insert(i)

			
