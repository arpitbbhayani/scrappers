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
            return True
        return False

    def parse(self, response):
        if not self.is_article(response):
            for article_url in response.css('#ContentLibrary a[class="img"]').xpath('@href').extract():
                yield scrapy.Request(article_url, callback=self.parse)

            next_buttons = response.css('#ContentLibrary .textRight img[src="http://s.hswstatic.com/en-us/skins/hsw/arrow-right-3x5-2.png"]')
            for next_button in next_buttons:
                url = next_button.xpath('../@href').extract()[0]
                yield scrapy.Request(url, callback=self.parse)

        else:

            ht = response.css('#ArticleWell div.content').extract()[0]
            desc = html2text.html2text(ht)

            try:
                image = response.xpath('//*[@id="type-article-structured"]/head/meta[@property="og:image"]/@content').extract()[0]
            except IndexError:
                image = None

            item = HowstuffworksItem()
            item['url'] = response.url
            item['title'] = response.css('#Title .articleTitle')[0].extract()
            item['desc'] = desc
            item['excerpt'] = desc[:997]
            item['image'] = image
            item['article_date'] = None
            yield item
