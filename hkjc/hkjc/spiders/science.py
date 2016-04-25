import scrapy
import html2text
from hkjc.items import ArticleItem
from urlparse import urlparse
from os.path import splitext, basename

import pytz
import logging
from datetime import datetime

class HKJCCrawler(scrapy.Spider):
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

    def process_team_name(self, name):
        return '"%s"' % name.replace(' ', '_')

    def process_rows(self, rows, server_timestamp):
        items = []
        for row in rows:

            item = ArticleItem()

            temp_rows = row.css('tr::attr(class)').extract()
            if len(temp_rows) == 0:
                continue

            class_attr = temp_rows[0].lower()
            if not ('rhead' in class_attr or 'rchead' in class_attr or 'tdpage' in class_attr):

                # Server timestamp
                dt = server_timestamp.split(' ')
                d = dt[0].replace('/', '-')
                t = dt[1]

                dtobj = datetime.strptime('%s %s' % (d, t), '%d-%m-%y %H:%M')
                dtobj = pytz.timezone("Hongkong").localize(dtobj)
                item['server_timestamp'] = dtobj.strftime('%Y-%m-%d %H:%M:%S %Z')

                # Client timestamp
                dtobj = pytz.timezone("Hongkong").localize(datetime.now())
                item['client_timestamp'] = dtobj.strftime('%Y-%m-%d %H:%M:%S %Z')

                # Fetch Flags
                flags = row.css('td.cflag')
                if len(flags) >= 1:
                    item['flag_1'] = self.get_image_filename(flags[0].css('img::attr(src)').extract()) or 0
                if len(flags) >= 2:
                    item['flag_2'] = self.get_image_filename(flags[1].css('img::attr(src)').extract()) or 0

                # Fetch Venue
                flags = row.css('td.cvenue')
                if len(flags) >= 1:
                    item['flag_3'] = self.get_image_filename(flags[0].css('img::attr(src)').extract()) or 0

                # Fetch teams
                teams = row.css('td.cteams')
                if len(teams) >= 1:
                    all_teams = self.get_raw(teams[0].css('a')[0].extract())

                    tokens = all_teams.split(' vs ')

                    home_team_name = tokens[0].split('[')[0].strip() if '[' in tokens[0] else tokens[0]
                    away_team_name = tokens[1].split('[')[0].strip() if '[' in tokens[1] else tokens[1]

                    item['home_team'] = self.process_team_name(home_team_name)
                    item['away_team'] = self.process_team_name(away_team_name)

                    if len(teams[0].css('a *')) >= 2:
                        item['home_goal'] = self.get_raw(teams[0].css('a *')[1].extract())
                    if len(teams[0].css('a *')) >= 5:
                        item['away_goal'] = self.get_raw(teams[0].css('a *')[4].extract())

                # Fetch Odds
                odds = row.css('td.codds')
                if len(odds) >= 1:
                    item['home_odds'] = self.get_raw(odds[0].extract())
                if len(odds) >= 2:
                    item['draw_odds'] = self.get_raw(odds[1].extract())
                if len(odds) >= 3:
                    item['away_odds'] = self.get_raw(odds[2].extract())

                # Fetch Post Time
                eest = row.css('td.cesst')
                if len(eest) >= 1:
                    tstr = self.get_raw(eest[0].extract())
                    dtobj = datetime.strptime(tstr, '%d/%m %H:%M')
                    if dtobj.year == 1900:
                        dtobj = dtobj.replace(year=datetime.now().year)
                    dtobj = pytz.timezone("Hongkong").localize(dtobj)
                    item['post_time'] = dtobj.strftime('%Y-%m-%d %H:%M:%S %Z')

            items.append(item)

        return items

    def parse_article_page(self, response):
        """
        Returns an item
        """
        articles = []
        odd_tables = response.css('table.tHHA.tOdds')
        server_timestamp = self.get_raw(response.css('#server_datetime').extract()[0])

        for odd_table in odd_tables:
            rows = odd_table.css('tr')
            articles.extend(self.process_rows(rows, server_timestamp))
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
