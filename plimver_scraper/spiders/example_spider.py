import scrapy

class ProductionSpider(scrapy.Spider):
    name = 'production'
    allowed_domains = []

    def start_requests(self):
        urls = getattr(self, 'urls', None)
        if urls:
            urls = urls.split(',')
        else:
            # default sample site that allows bots
            urls = ['https://httpbin.org/html']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = {}
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').get() or ''
        item['raw_text'] = response.text
        yield item
