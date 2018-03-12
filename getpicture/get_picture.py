'''
爬取动态加载的图片,对使用 ajax 请求的 url 发起请求，先提取页面的 img 标签，再取 src 链接，对 src 链接发起请求，获取图片内容。
python 3.6
os:Mac os
'''
import requests
import re
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool


headers = {
	'Accpet':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_picture(url_list):
	photos = []	
	html = requests.get(url_list,headers=headers)
	soup = BeautifulSoup(html.text,'lxml')
	imgs = soup.select('div.l-container.home-page > div.photos > article > a.js-photo-link > img')

	#遍历图片标签以获取图片链接
	for img in imgs:
		photo = img.get('src')
		photos.append(photo)
	
	#本机写入路径
	path = '/Users/linjunyi/Desktop/spider/getpicture/picture/'

	# 遍历请求每个图片链接，获取图片内容
	for item in photos:
		data = requests.get(item,headers=headers)
		photo_name = re.findall(r'\d+/(.*?)\?h',item) #图片链接中图片名称，返回列表
		if photo_name: #判断一下，只写抓取到的数据
			# 写数据
			with open(path + photo_name[0],'wb') as file:
				file.write(data.content)
			# print(photo_name)

#只抓取10页数据，
url_list = ['https://www.pexels.com/?page={}'.format(str(index)) for index in range(1,11)]

if __name__ == '__main__':
	#多进程
	pool = Pool(processes=4)
	pool.map(get_picture,url_list)
	print('done!')

	# start1 = time.time()
	# for url in url_list:
	# 	get_picture(url)
	# 	time.sleep(1)
	# end1 = time.time()
	# print('单进程爬虫：',end1 - start1)


