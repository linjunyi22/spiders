'''
requests + regexp 抓取酷狗 top500歌曲写入文件

'''

import re
import requests


#待爬url列表
url_list = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(index)) for index in range(1,24)]

headers = {
	"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

#获取一个页面的html 代码
def get_one_page(url,headers):
	html = requests.get(url,headers=headers)
	result = html.text
	return result


#解析一个页面，获取内容
def parse_one_page(html):
	pattern = re.compile(r'class="pc_temp_num">.*?(\d+).*?<a.*?"playDwn".*?>(.*?) - (.*?)</a>.*?class="pc_temp_time">.*?(\d+:\d+).*?</span>',re.S)
	re_html = re.findall(pattern,html)
	for item in re_html:
		yield {
			'index':item[0],
			'singer':item[1],
			'song_name':item[2],
			'time':item[3]
		}		
	return re_html


#将内容写进文件
def write_data(content): 
	with open('kugou_top500.txt','a') as file:
		for content_item in content:
			file.write(str(content_item) + '\n')


#遍历top500所有链接
if __name__ == '__main__':
	for url_item in url_list:
		html = get_one_page(url_item)
		content = parse_one_page(html)
		write_data(content)


