# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 定义相关字段
    # 排名、电影名、评分、评论人数、概述
    ranking = Field()
    movie_name = Field()
    score = Field()
    score_num = Field()
    overview = Field()
