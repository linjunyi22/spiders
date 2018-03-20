'''
requests +  lxml 抓取链家网上广深杭租房数据
python 3.6
os:mac os
'''


from lxml import etree
import requests
import time


headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9,la;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'	
}


#获取页面
def get_page(url,headers):
	try:
		response = requests.get(url,headers=headers)
		if response.status_code == 200:
			html = response.text
			return html
		return '请求失败'
	except RequestException as e:
		return '请求出错'


#解析内容
def parse_page(html):
	#存数据容器
	data_box = []
	#lxml 解析
	selector = etree.HTML(html)
	infos = selector.xpath('//ul[@class="sellListContent"]/li')	#xpath 返回列表
	# print(len(infos))

	for info in infos:
		title = info.xpath('div/div/a/text()')[0]
		details = info.xpath('div/div[2]/div/text()')[0].replace('|','').strip()
		floor = info.xpath('div/div[3]/div')[0].xpath('string(.)')
		tag = info.xpath('div/div[5]')[0].xpath('string(.)')
		totalprice = info.xpath('div/div[6]/div')[0].xpath('string(.)')
		unitprice = info.xpath('div/div[6]/div[2]/span/text()')[0]

		data = {
			'title':title,
			'details':details,
			'floor':floor,
			'tag':tag,
			'totalprice':totalprice,
			'unitprice':unitprice
		}
		data_box.append(data)
	return data_box


#写数据
def main():
	cities = ['sh','gz','sz','hz']#城市列表
	#抓100页
	url_list = ['https://{0}.lianjia.com/ershoufang/pg{1}/'.format(city,str(i)) for city in cities for i in range(1,101)]
	count = 0

	for url in url_list:
		count += 1	#计数，每抓一个城市，用横线分割一下	
		html = get_page(url,headers)
		data = parse_page(html)
		with open('lianjia.txt','a',encoding='utf8') as file:
			for unit_data in data:
				print(unit_data)								
				file.write(str(unit_data))
				if count == 100:
					file.write('\n{}\n'.format('-'*30))
					count = 0

if __name__ == '__main__':
	main()


