# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy.conf import settings

#
# class PanduoduoPipeline(object):
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False) + '\n'
#         with open('text.json', 'a', encoding='utf-8') as file:
#             file.write(line)
#         return item


class PanduoduoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost:27017')
        duoduodb = client['test']
        panduoduo = duoduodb['panduoduo']
        self.post = panduoduo

    def process_item(self, item, spider):
        info = dict(item)
        self.post.insert(info)
        return item
