# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    server_timestamp = scrapy.Field()
    client_timestamp = scrapy.Field()

    home_team = scrapy.Field()
    home_goal = scrapy.Field()
    away_team = scrapy.Field()
    away_goal = scrapy.Field()

    post_time = scrapy.Field()

    flag_1 = scrapy.Field()
    flag_2 = scrapy.Field()
    flag_3 = scrapy.Field()

    home_odds = scrapy.Field()
    draw_odds = scrapy.Field()
    away_odds = scrapy.Field()

    final = scrapy.Field()
