# -*- coding: utf--8 -*-
import urllib.request 
import urllib.error
import re

headers = {
			'Host':'tieba.baidu.com',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
		}

#处理文本多余内容
class TagTool(object):
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD= re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')

    def replace(self,x):
	    x = re.sub(self.removeImg,"",x)
	    x = re.sub(self.removeAddr,"",x)
	    x = re.sub(self.replaceLine,"\n",x)
	    x = re.sub(self.replaceTD,"\t",x)
	    x = re.sub(self.replacePara,"\n    ",x)
	    x = re.sub(self.replaceBR,"\n",x)
	    x = re.sub(self.removeExtraTag,"",x)
	    return x.strip()

class tieba(object):
	#初始化地址和是否仅查看楼主帖子
	def __init__(self, baseUrl,seeLZ):
		self.baseUrl = baseUrl
		self.seeLZ = '?seeLZ=' + str(seeLZ)
		self.tool = TagTool()
		self.file = None
		self.floor = 1
		self.deafultTitle = 'tieba'

	#获取页面源码,第几页由page_num确定
	def get_html(self,page_num):
		try:
			url = self.baseUrl + self.seeLZ + '&pn=' + str(page_num)		
			request = urllib.request.Request(url,headers = headers)
			response = urllib.request.urlopen(request)
			html = response.read().decode('utf-8')
			return html
		except urllib.error.URLError as e:
			if hasattr(e,'code'):
				print('错误编号：',e.code)
			if hasattr(e,'reason'):
				print('错误原因：',e.reason)
			return None

	#获取标题
	def get_title(self,html):
		title_re = re.compile('<title>(.*?)_.*?</title>',re.S)
		result = re.search(title_re,html)
		if result:
			return result.group(1).strip()
		return None

	#获取帖子总页数
	def get_pagenum(self,html):
		page_num_re = re.compile('</span>回复贴，共<span class="red">(.*?)</span>',re.S)
		result = re.search(page_num_re,html)
		if result:
			return result.group(1).strip()
		return None

	#获取每一层楼的内容
	def get_content(self,html):
		content_re = re.compile('<div.*?class="d_post_content j_d_post_content ">(.*?)</div>',re.S)
		items = re.findall(content_re,html)
		contents = []
		for item in items:
			content = '\n' + self.tool.replace(item) + '\n'
			contents.append(content)
		# print(contents)
		return contents

	#写数据
	def write_data(self,contents):
		for item in contents:
			floorLine = '\n' + str(self.floor) + '楼--------------------------------------\n'
			self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	#设置文件
	def set_file_title(self,title):
		if title is not None:
			self.file = open(title + '.txt','w')
		else:
			self.file = open(self.deafultTitle + '.txt','w')



	def start(self):
		index_page = self.get_html(1)
		page_num = self.get_pagenum(index_page)
		title = self.get_title(index_page)
		self.set_file_title(title)
		# print(page_num)
		try:
			for i in range(1,int(page_num)+1):
				print('正在写第' + str(i) + '页数据')
				html = self.get_html(i)
				contents = self.get_content(html)
				self.write_data(contents)
		except IOError as e:
			print('写入失败：' + e.message)
		finally:
			print('写入完成')

url = 'https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1'
spider = tieba(url,1)
spider.start()