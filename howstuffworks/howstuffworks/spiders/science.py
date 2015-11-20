import scrapy, html2text
from howstuffworks.items import ArticleItem

class ScienceCrawler(scrapy.Spider):
    name = "science"
    site = "howstuffworks"
    allowed_domains = ["science.howstuffworks.com"]
    start_urls = [
        "http://science.howstuffworks.com/engineering/civil",
        "http://science.howstuffworks.com/materials-science-channel.htm",
        "http://science.howstuffworks.com/engineering/structural",
        "http://science.howstuffworks.com/devices-channel.htm",
        "http://science.howstuffworks.com/robots-channel.htm",
        "http://science.howstuffworks.com/environmental/conservation",
        "http://science.howstuffworks.com/environmental/energy",
        "http://science.howstuffworks.com/environmental/green-science",
        "http://science.howstuffworks.com/environmental/earth",
        "http://science.howstuffworks.com/environmental/terms",
        "http://science.howstuffworks.com/environmental/green-tech",
        "http://science.howstuffworks.com/nature/climate-weather",
        "http://science.howstuffworks.com/nature/natural-disasters",
        "http://science.howstuffworks.com/innovation/big-thinkers",
        "http://science.howstuffworks.com/innovation/everyday-innovations",
        "http://science.howstuffworks.com/innovation/inventions",
        "http://science.howstuffworks.com/innovation/new-inventions",
        "http://science.howstuffworks.com/innovation/science-questions",
        "http://science.howstuffworks.com/innovation/edible-innovations",
        "http://science.howstuffworks.com/innovation/famous-inventors",
        "http://science.howstuffworks.com/innovation/nasa-inventions",
        "http://science.howstuffworks.com/innovation/repurposed-inventions",
        "http://science.howstuffworks.com/innovation/scientific-experiments",
        "http://science.howstuffworks.com/life/biology-fields",
        "http://science.howstuffworks.com/life/cellular-microscopic",
        "http://science.howstuffworks.com/life/fungi",
        "http://science.howstuffworks.com/life/inside-the-mind",
        "http://science.howstuffworks.com/life/botany",
        "http://science.howstuffworks.com/life/evolution",
        "http://science.howstuffworks.com/life/genetic",
        "http://science.howstuffworks.com/military-aircraft-channel.htm",
        "http://science.howstuffworks.com/biological-warfare-channel.htm",
        "http://science.howstuffworks.com/explosives-channel.htm",
        "http://science.howstuffworks.com/future-military-technology.htm",
        "http://science.howstuffworks.com/personal-finance-in-military.htm",
        "http://science.howstuffworks.com/surveillance-stealth-channel.htm",
        "http://science.howstuffworks.com/military/army-careers",
        "http://science.howstuffworks.com/military-branches-channel.htm",
        "http://science.howstuffworks.com/firearms-channel.htm",
        "http://science.howstuffworks.com/naval-technology-channel.htm",
        "http://science.howstuffworks.com/soldiers-channel.htm",
        "http://science.howstuffworks.com/tanks-fighting-vehicles-channel.htm",
        "http://science.howstuffworks.com/acoustics-channel.htm",
        "http://science.howstuffworks.com/electricity-channel.htm",
        "http://science.howstuffworks.com/history-of-physics-channel.htm",
        "http://science.howstuffworks.com/math-concepts",
        "http://science.howstuffworks.com/mechanics-channel.htm",
        "http://science.howstuffworks.com/optics-channel.htm",
        "http://science.howstuffworks.com/chemistry-channel.htm",
        "http://science.howstuffworks.com/forensic-science-channel.htm",
        "http://science.howstuffworks.com/magnetism-channel.htm",
        "http://science.howstuffworks.com/matter-channel.htm",
        "http://science.howstuffworks.com/nuclear-science-channel.htm",
        "http://science.howstuffworks.com/dictionary/astronomy-terms",
        "http://science.howstuffworks.com/dictionary/biology-terms",
        "http://science.howstuffworks.com/dictionary/famous-scientists",
        "http://science.howstuffworks.com/dictionary/meteorological-terms",
        "http://science.howstuffworks.com/dictionary/petrology-terms",
        "http://science.howstuffworks.com/dictionary/awards-organizations",
        "http://science.howstuffworks.com/dictionary/chemistry-terms",
        "http://science.howstuffworks.com/dictionary/geology-terms",
        "http://science.howstuffworks.com/dictionary/physics-terms",
        "http://science.howstuffworks.com/dictionary/plant-terms",
        "http://science.howstuffworks.com/science-vs-myth/afterlife",
        "http://science.howstuffworks.com/science-vs-myth/extrasensory-perceptions",
        "http://science.howstuffworks.com/science-vs-myth/unexplained-phenomena",
        "http://science.howstuffworks.com/science-vs-myth/everyday-myths",
        "http://science.howstuffworks.com/science-vs-myth/strange-creatures",
        "http://science.howstuffworks.com/science-vs-myth/what-if",
        "http://science.howstuffworks.com/space/aliens-ufos",
        "http://science.howstuffworks.com/future-space-channel.htm",
        "http://science.howstuffworks.com/space-exploration-channel.htm",
        "http://science.howstuffworks.com/astronomy-channel.htm",
        "http://science.howstuffworks.com/spaceflight-channel.htm",
        "http://science.howstuffworks.com/space-transportation-systems-channel.htm",
        "http://science.howstuffworks.com/transport/engines-equipment",
        "http://science.howstuffworks.com/transport/flight"
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
        item = ArticleItem()
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
