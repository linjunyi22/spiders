# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

# items 定义要爬取的内容字段 	
class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = Field()
    content = Field()
    article = Field()
    fans = Field()

