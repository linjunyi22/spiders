# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanItem
from scrapy import Request


class DoubanSpider(scrapy.Spider):
    name = 'Douban'
    # allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
    	item = DoubanItem()
    	movies = response.xpath('//ol[@class="grid_view"]/li')
    	for movie in movies:
    		ranking = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
    		movie_name = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()[0]
    		score = movie.xpath('.//div[@class="star"]/span[2]/text()').extract()[0]
    		score_num = movie.xpath('.//div[@class="star"]/span[4]/text()').extract()[0]
    		try:
    			overview = movie.xpath('.//p[@class="quote"]/span/text()').extract()[0]
    		except Exception as e:
    			overview = ''
    		
    		item['ranking'] = ranking
    		item['movie_name'] = movie_name
    		item['score'] = score
    		item['score_num'] = score_num
    		item['overview'] = overview

    		yield item

    		next_url = response.xpath('//span[@class="next"]/a/@href').extract()
    		if next_url:
    			next_url = 'https://movie.douban.com/top250' + next_url[0]
    			yield Request(next_url)



