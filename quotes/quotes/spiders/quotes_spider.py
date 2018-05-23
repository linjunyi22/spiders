import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # Spider的标识。它在项目中必须是独一无二的，不能为不同的Spider设置相同的名称

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1',
            'http://quotes.toscrape.com/page/2',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes-{}.html'.format(page)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {}'.format(filename))