# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class FileWriterPipeline(object):
    def __init__(self, dump_folder):
        self.dump_folder = dump_folder

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            dump_folder=crawler.settings.get('DUMP_FOLDER'),
        )

    def format_item(self, item):

        if 'server_timestamp' not in item:
            item['server_timestamp'] = ''

        if 'client_timestamp' not in item:
            item['client_timestamp'] = ''

        if 'home_team' not in item:
            item['home_team'] = ''

        if 'home_goal' not in item:
            item['home_goal'] = ''

        if 'away_team' not in item:
            item['away_team'] = ''

        if 'away_goal' not in item:
            item['away_goal'] = ''

        if 'post_time' not in item:
            item['post_time'] = ''

        if 'flag_1' not in item:
            item['flag_1'] = ''

        if 'flag_2' not in item:
            item['flag_2'] = ''

        if 'flag_3' not in item:
            item['flag_3'] = ''

        if 'home_odds' not in item:
            item['home_odds'] = ''

        if 'draw_odds' not in item:
            item['draw_odds'] = ''

        if 'away_odds' not in item:
            item['away_odds'] = ''

        if 'final' not in item:
            item['final'] = ''


        return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
            item['server_timestamp'],
            item['client_timestamp'],
            item['home_team'],
            item['home_goal'],
            item['away_team'],
            item['away_goal'],
            item['post_time'],
            item['flag_1'],
            item['flag_2'],
            item['flag_3'],
            item['home_odds'],
            item['draw_odds'],
            item['away_odds'],
            item['final']
        )

    def process_item(self, item, spider):
        file_path = os.path.join(self.dump_folder, 'temp.txt')
        with open(file_path, 'a') as data_file:
            content = self.format_item(item)
            data_file.write(content)
            data_file.write('\n')
        return item
