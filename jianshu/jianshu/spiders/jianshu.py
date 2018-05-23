import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from jianshu.items import JianshuItem
from scrapy.exceptions import CloseSpider


class jianshu(scrapy.Spider):
    name = 'jianshu'
    # allowed_domains = ['example.com']
    start_urls = ['https://www.jianshu.com/recommendations/collections?page=3&order_by=hot']

    def parse(self, response):
        item = JianshuItem() # 实例化一个 Item 类，存储字段
        selector = Selector(response)
        infos = selector.xpath('//div[@class="collection-wrap"]')
        for info in infos:
        	name = info.xpath('a[1]/h4/text()').extract()[0]
        	content = info.xpath('a[1]/p/text()').extract()
        	article = info.xpath('div/a/text()').extract()[0]
        	fans = info.xpath('div/text()').extract()[0]

        	if content:
        		content = content[0]
        	else:
        		content = ''

        	# 存入 item
        	item['name'] = name
        	item['content'] = content
        	item['article'] = article
        	item['fans'] = fans

        	yield item

        # 前面已经获取了第一页的数据，现在从第二页开始
        urls = ['https://www.jianshu.com/recommendations/collections?page={}&order_by=hot'.format(str(i)) for i in range(2,30)]


        for url in urls:
        	yield Request(url, callback=self.parse)
