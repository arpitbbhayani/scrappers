import scrapy, html2text
from wallpaperswide.items import WallpaperItem

class WallpaperCrawler(scrapy.Spider):
    name = "wallpaper"
    site = "wallpaperswide.com"
    allowed_domains = ["wallpaperswide.com"]
    base_url = 'http://wallpaperswide.com'
    start_urls = [
        "http://wallpaperswide.com/love-desktop-wallpapers.html"
    ]
    priorities = [
        '1366x768',
        '1280x768',
        '1280x720',
        '1440x900',
        '1600x900',
        '1280x1024',
        '1280x960',
        '960x600',
        '800x600'
    ]

    def is_wallpaper(self, response):
        if response.css('#wallpaper-resolutions'):
            return False
        return False

    def getatindex(self, a, index=0):
        if not a:
            return a
        return a[index]

    def mergeall(self, a):
        return ''.join(a)


    def parse_wallpaper_page(self, response):
        """
        Returns an item
        """
        item = WallpaperItem()
        image_url = None
        for resolution in WallpaperCrawler.priorities:
            xp = '//div[@id="wallpaper-resolutions"]/a[text()="%s"]/@href' % resolution
            link = response.xpath(xp).extract()
            if link:
                image_url = WallpaperCrawler.base_url + self.getatindex(link)
                break

        if image_url:
            item['image_url'] = image_url
            yield item
        else:
            self.logger.warning('No images found for given resolution %s' % response.url)


    def parse(self, response):
        for wallpaper_page_url in response.xpath('//div[@id="content"]//ul[@class="wallpapers"]/li//a/@href').extract():
            wallpaper_page_url = WallpaperCrawler.base_url + wallpaper_page_url
            yield scrapy.Request(wallpaper_page_url, callback=self.parse_wallpaper_page)

        next_urls = response.xpath('//*[@id="content"]/div[@class="pagination"]/a[contains(text(),"Next")]/@href').extract()
        for next_url in next_urls:
            next_url = WallpaperCrawler.base_url + next_url
            yield scrapy.Request(next_url, callback=self.parse)
