# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章标题，创建时间，点赞数，收藏数，文章内容，评论数，标签
    title = Field()
    create_time = Field()
    like = Field()
    favorite = Field()
    content = Field()
    comment = Field()
    tags = Field()
