import scrapy


class IodpSpider(scrapy.Spider):
    name = 'iodp'
    allowed_domains = ['web.iodp.tamu.edu']

    def parse(self, response):
        pass
