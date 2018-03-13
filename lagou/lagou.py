'''
requests对ajax 请求的数据进行抓取。先分析其 ajax 请求的 url，
然后通过chrome开发者工具查看其 post 参数，发起请求获取内容，然后解析入库。
python 版本：3.6
os：mac os
'''

import json
import time
import math

import requests
import pymongo

#mongodb数据库连接
client = pymongo.MongoClient('localhost',27017)
mydb = client['mydb']
lagou = mydb['lagou']

headers = {
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9,la;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'26',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie':'_ga=GA1.2.1010629292.1516194511; user_trace_token=20180117210841-751ccfe2-b73c-4360-9034-358b56858816; LGUID=20180117210846-8d290e38-fb87-11e7-a26c-525400f775ce; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519564052; LGSID=20180225210731-d6ae6406-1a2c-11e8-b092-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUs0fVuFp00000Pe4pNb00000rzh9_H.THL0oUhY1x60UWdBmy-bIfK15yn1m16znHcznj0snvwhm160IHY3wbm4wj7anHIaPWT4rHbLrHNKwbc1nW9Arjb3wDRvw6K95gTqFhdWpyfqn101n1csPHnsPausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYEUZ0EpZwVUaqWUvdVUv38pZwVUjqdIAdxTvqdThP-5ydxmvuxmLKYgvF9pywdgLKW0APzm1YYnWb4n6%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117470%26attach%3Dlocation%253D%2526linkName%253Dlogo%2526linkText%253D%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D15%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rqlang%3Dcn%26inputT%3D1302; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; _gid=GA1.2.1106339931.1519564052; X_HTTP_TOKEN=46b3c23196920fbf54652e7771e04632; _putrc=C573E13ECC74F34D; JSESSIONID=ABAAABAAAIAACBI864C6F6B9BFC095FC282ED9973D12396; login=true; unick=%E6%9E%97%E4%BF%8A%E6%AF%85; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; gate_login_token=17db3b85cc03baf1a558b5e4f44e4e18f0b1d002f1d93d30; index_location_city=%E5%B9%BF%E5%B7%9E; TG-TRACK-CODE=index_search; SEARCH_ID=a37cce63249042a9ac829da3b9d49fb9; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519564116; LGRID=20180225210835-fcf45f84-1a2c-11e8-b092-5254005c3644',
	'Host':'www.lagou.com',
	'Origin':'https://www.lagou.com',
	'Referer':'https://www.lagou.com/jobs/list_python?',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
	'X-Anit-Forge-Code':'0',
	'X-Anit-Forge-Token':'None',
	'X-Requested-With':'XMLHttpRequest'
}

#获取要抓取的页数
def get_page_num(url):
	params = {
		'first': 'true',
		'pn': '1',
		'kd': 'Python'
	}

	html = requests.post(url,data=params, headers=headers)
	json_data = json.loads(html.text)
	total_count = json_data['content']['positionResult']['totalCount'] #ajax 返回的json 数据中的招聘企业总数
	# page_number = math.ceil(total_count / 15) #每页展示15家，整除后得到抓取页数
	get_info(url,2)


#获取具体数据
def get_info(url,page):
	for pn in range(1,page + 1):
		params = {
			'first': 'true' if pn ==1 else 'false',
			'pn': str(pn),
			'kd': 'Python'
		}

		#每一页具体数据抓取
		try:
			html = requests.post(url, data=params, headers=headers)
			json_data = json.loads(html.text)
			results = json_data['content']['positionResult']['result'] #企业招聘详情
			for result in results:
					#json数据
					infos = {
						'businessZones':result['businessZones'],
						'city':result['city'],
						'companyFullName':result['companyFullName'],
						'companyLabelList':result['companyLabelList'],
						'companySize':result['companySize'],
						'district':result['district'],
						'education':result['education'],
						'explain':result['explain'],
						'financeStage':result['financeStage'],
						'firstType':result['firstType'],
						'formatCreateTime':result['formatCreateTime'],
						'gradeDescription':result['gradeDescription'],
						'imState':result['imState'],
						'industryField':result['industryField'],
						'industryLables':result['industryLables'],
						'jobNature':result['jobNature'],
						'positionAdvantage':result['positionAdvantage'],
						'positionName':result['positionName'],
						'salary':result['salary'],
						'secondType':result['secondType'],
						'workYear':result['workYear']
					}
					print('-'*20)
					print(infos)
					lagou.insert_one(infos)

			time.sleep(2)
		except requests.exceptions.ConnectionError:
			return None			
	print('Done!')


if __name__ == '__main__':
	url = 'https://www.lagou.com/jobs/positionAjax.json'
	get_page_num(url)




