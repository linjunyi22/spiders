# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from ..items import ArticlespiderItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/']

    def start_requests(self):
        url = 'http://blog.jobbole.com/all-posts/'
        yield Request(url, self.next_parse)

    def next_parse(self, response):
        next_page = response.xpath('//div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract()[0]
        post_url = response.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]/'
                           'div[@class="post-meta"]/p/a[1]/@href').extract()
        # 处理数据
        for url in post_url:
            yield Request(url=url, callback=self.post_parse)

        yield Request(url=next_page, callback=self.next_parse)

    def post_parse(self, response):
        item = ArticlespiderItem()
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_time = response.xpath('//div[@class="entry-meta"]/p/text()').extract()[0].strip().replace('·', '').strip()
        like = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0]
        # 有些文章没有收藏数，直接赋值0
        favorite = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0].replace(' 收藏', '')
        match_re = re.match(".*?(\d+).*", favorite)
        if not match_re:
            favorite = '0'

        # 有些文章没有评论数，取到数据后正则判断一下，没有的话就直接赋值 0 条评论
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].replace(' 评论', '')
        match_re = re.match(".*?(\d+).*", comment_nums)
        if not match_re:
            comment_nums = '0'

        content = response.xpath('//div[@class="entry"]').extract()[0]
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # 把无用的'评论'字符串剔除掉
        tag_list = [i for i in tag_list if '评论' not in i]
        tags = ','.join(tag_list)

        item['title'] = title
        item['create_time'] = create_time
        item['like'] = like
        item['favorite'] = favorite
        item['content'] = content
        item['comment'] = comment_nums
        item['tags'] = tags

        yield item
