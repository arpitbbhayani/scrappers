import scrapy, html2text
from howstuffworks.items import HowstuffworksItem

class ScienceCrawler(scrapy.Spider):
    name = "science"
    allowed_domains = ["science.howstuffworks.com"]
    start_urls = [
        "http://science.howstuffworks.com/engineering/civil"
    ]

    def is_article(self, response):
        if response.css('#Title'):
            return False
        return False


    def getatindex(self, a, index=0):
        if not a:
            return a
        return a[index]

    def mergeall(self, a):
        return ''.join(a)


    def parse_article_page(self, response):
        """
        Returns an item
        """
        item = HowstuffworksItem()
        item['url'] = response.url
        item['title'] = self.getatindex(response.xpath('//*[@id="Title"]//h1/text()').extract())
        item['desc'] = self.mergeall(response.xpath('//*[@id="ArticleWell"]//div[@class="content"]/p/text()').extract())
        item['excerpt'] = item['desc'][:800]
        item['related'] = response.xpath('//*[@id="RelatedLinks0"]//a/@href').extract()
        item['images'] = {
            'inset': response.xpath('//*[@id="ArticleWell"]//img/@src').extract(),
            'fb': self.getatindex(response.xpath('//*[@property="og:image"]/@content').extract())
        }

        if len(item['desc']) < 1000:
            self.logger.warning('Description is less than 1000 chars. Might be fishy %s' % item['url'])
        yield item


    def parse(self, response):
        for article_url in response.css('#ContentLibrary a[class="img"]').xpath('@href').extract():
            yield scrapy.Request(article_url, callback=self.parse_article_page)

        next_buttons = response.xpath('//*[@id="ContentLibrary"]//img[@src="http://s.hswstatic.com/en-us/skins/hsw/arrow-right-3x5-2.png"]')
        for next_button in next_buttons:
             url = self.getatindex(next_button.xpath('../@href').extract())
             yield scrapy.Request(url, callback=self.parse)
