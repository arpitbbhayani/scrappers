import scrapy

class ScienceCrawler(scrapy.Spider):
    name = "science"
    allowed_domains = ["science.howstuffworks.com"]
    start_urls = [
        "http://science.howstuffworks.com/"
    ]

    def parse(self, response):
        for c in response.css('#WhatsinsideBody ul li div.unit a'):
            link = c.xpath('@href').extract()[0]
            text = c.xpath('text()').extract()[0]
            print link
