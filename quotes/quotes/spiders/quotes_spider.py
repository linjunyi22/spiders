import scrapy

from scrapy import cmdline

cmdline.execute('scrapy crawl quotes'.split())


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # Spider的标识。它在项目中必须是独一无二的，不能为不同的Spider设置相同的名称

# first-step
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1',
    #         'http://quotes.toscrape.com/page/2',
    #     ]
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    #
    # def parse(self, response):
    #     page = response.url.split('/')[-2]
    #     filename = 'quotes-{}.html'.format(page)
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file {}'.format(filename))

    start_urls = [
        'http://quotes.toscrape.com/page/1',
        'http://quotes.toscrape.com/page/2',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
