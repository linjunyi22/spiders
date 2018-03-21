'''
参照网易云课堂一个教程学习使用 selenium 和 phantomjs
python 3.6
os：mac os
使用 selenium 和 phantomjs 抓取淘宝商品信息
获取搜索框、搜索按钮、下一页等元素， xpath 解析页面，最终把数据写进 mongodb，再点击下一页按钮获取下一页信息，循环操作。
'''

from selenium import webdriver
from lxml import etree
import time
import pymongo

#建立数据库连接
client = pymongo.MongoClient('localhost',27017)
db = client['mydb']
taobao = db['taobao']

driver = webdriver.PhantomJS(executable_path='/Users/linjunyi/phantomjs/bin/phantomjs')
driver.maximize_window() #selenium 操作网页的基础，如果窗口不处在最大化字体，会导致看不到的地方操作不到

def get_page_info(url,page): #传参： url 和从第几页开始爬取	
	driver.get(url)    
	driver.implicitly_wait(10)
	selector = etree.HTML(driver.page_source) #driver.page_source 指获取的页面内容

	#使用 etree 解析页面，返回列表对象，包含所有信息
	infos = selector.xpath('//div[@class="item J_MouserOnverReq  "]')

	#获取单个商品信息，xpath方法为 etree 的方法，与 selenium 的 find_element_xpath 不同，因此可以直接带 text()
	for info in infos:
		goods = info.xpath('div/div/div/a/img/@alt')[0]
		price = info.xpath('div/div/div/strong/text()')[0]
		sell = info.xpath('div/div/div[@class="deal-cnt"]/text()')[0]
		shop = info.xpath('div[2]/div[3]/div[1]/a/span[2]/text()')[0]
		address = info.xpath('div[2]/div[3]/div[2]/text()')[0]
 
		sell = sell[0] if sell else 0 #当售卖次数为零时，返回空列表，因此设置一下
		result = {
			'goods' : goods,
			'price' :price,
			'sell': sell,
			'shop':shop,
			'address' :address
		}
		print(result)
		taobao.insert_one(result)
	print('第{}页爬取完毕'.format(page))
	page += 1
	if page < 10: #抓10页
		next_page(url,page)
	else:
		return None


def next_page(url,page):
	driver.get(url)
	driver.implicitly_wait(10)
	driver.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()
	time.sleep(4)
	get_page_info(driver.current_url,page)


if __name__ == '__main__':
	url = 'https://www.taobao.com'
	driver.get(url)
	driver.implicitly_wait(10)
	driver.find_element_by_id('q').clear #清空搜索框
	driver.find_element_by_id('q').send_keys('家用电器') #输入查询内容
	driver.find_element_by_class_name('btn-search').click() #点击查询按钮
	get_page_info(driver.current_url,1) #driver.current_url 指点击搜索后跳转的 url

