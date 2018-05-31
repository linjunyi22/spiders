# -*- coding: utf-8 -*-
import scrapy
from panduoduo.items import PanduoduoItem
from datetime import datetime
from scrapy import Request

class PspiderSpider(scrapy.Spider):
    name = 'Pspider'
    # allowed_domains = ['panduoduo.net']
    # start_urls = ['http://www.panduoduo.net/bd/{}'.format(str(i)) for i in range(1, 10)]

    def start_requests(self):
        url = 'http://www.panduoduo.net/bd/1'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'http://www.panduoduo.net'
        tr_list = response.xpath('//table[@class="list-resource"]/tr')[1:]

        for tr in tr_list:
            item = PanduoduoItem()
            title = tr.xpath('td[1]/a/@title').extract()[0]
            doc_link = 'http://www.panduoduo.net' + tr.xpath('td[1]/a/@href').extract()[0]
            tag = tr.xpath('td[2]/a/text()').extract()[0]
            file_size = tr.xpath('td[3]/text()').extract()[0]
            time = tr.xpath('td[6]').xpath('string(.)').extract()[0]
            item['name'] = title
            item['link'] = doc_link
            item['tag'] = tag
            item['size'] = file_size
            item['time'] = time

            yield item

        next_url = response.xpath('//div[@class="page-list"]/a[@title="下一页"]/@href').extract()[0]
        # print(next_url)
        if next_url:
            next_url = base_url + next_url
            yield Request(next_url, callback=self.parse)
