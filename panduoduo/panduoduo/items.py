# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class PanduoduoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 文件名、文件链接、文件大小、收录时间、分类
    name = Field()
    link = Field()
    size = Field()
    time = Field()
    tag = Field()

