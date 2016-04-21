import scrapy
import html2text
from hkjc.items import ArticleItem
from urlparse import urlparse
from os.path import splitext, basename

import logging

class ScienceCrawler(scrapy.Spider):
    name = "hkjc"
    site = "hkjc"
    allowed_domains = ["bet.hkjc.com"]
    base_domain = "http://bet.hkjc.com"
    start_urls = [
        "http://bet.hkjc.com/football/odds/odds_hha.aspx?ci=en-US",
    ]

    def get_raw(self, htmltext):
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        return converter.handle(htmltext).strip()

    def get_image_filename(self, image_url):
        if type(image_url) != list or len(image_url) == 0:
            return None

        disassembled = urlparse(image_url[0])
        filename, file_ext = splitext(basename(disassembled.path))
        return filename

    def process_rows(self, rows):
        items = []
        for row in rows:

            item = ArticleItem()

            temp_rows = row.css('tr::attr(class)').extract()
            if len(temp_rows) == 0:
                continue

            class_attr = temp_rows[0].lower()
            if not ('rhead' in class_attr or 'rchead' in class_attr or 'tdpage' in class_attr):
                flags = row.css('td.cflag')
                if len(flags) >= 1:
                    item['flag_1'] = self.get_image_filename(flags[0].css('img::attr(src)').extract())
                if len(flags) >= 2:
                    item['flag_2'] = self.get_image_filename(flags[1].css('img::attr(src)').extract())

            items.append(item)

        return items

    def parse_article_page(self, response):
        """
        Returns an item
        """
        articles = []
        odd_tables = response.css('table.tHHA.tOdds')
        for odd_table in odd_tables:
            rows = odd_table.css('tr')
            articles.extend(self.process_rows(rows))
        return articles

    def parse(self, response):
        for article in self.parse_article_page(response):
            yield article

        page_buttons = response.css('#tblOdds a')

        for page_button in page_buttons:
            link_text = self.get_raw(page_button.extract())
            if link_text.lower() == 'next':
                next_link = page_button.xpath('@href').extract()
                if len(next_link) >= 0:
                    yield scrapy.Request(self.base_domain + next_link[0], callback=self.parse)


        # next_buttons = response.xpath('//*[@id="ContentLibrary"]//img[@src="http://s.hswstatic.com/en-us/skins/hsw/arrow-right-3x5-2.png"]')
        # for next_button in next_buttons:
        #      url = self.getatindex(next_button.xpath('../@href').extract())
        #      yield scrapy.Request(url, callback=self.parse)
