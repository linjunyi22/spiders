'''
使用requests 和 beautifulsoup 抓取酷狗 top500的歌曲并写入 mongodb
'''

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

#连接数据库
client = MongoClient()
songs = client.kugou_db.songs

headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

#获取内容，清洗数据
def get_message(url,headers):
	html = requests.get(url,headers=headers)
	soup = BeautifulSoup(html.text,'lxml')
	index = soup.select('.pc_temp_num')
	title = soup.select('.pc_temp_songlist > ul > li > a')
	time = soup.select('.pc_temp_time')

	for index_,title_,time_ in zip(index,title,time):
		data = {
			'index':index_.get_text().strip(),
			'singer':title_.get_text().strip().split('-')[0],
			'song':title_.get_text().strip().split('-')[1],
			'time':time_.get_text().strip()
		}
		#写数据
		song_id = songs.insert(data)
		# print(data)


if __name__ == '__main__':
	url_list = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(index)) for index in range(1,24)]
	for url in url_list:
		get_message(url)
		time.sleep(1)

