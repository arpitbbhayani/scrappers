# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import logging
from datetime import datetime


class FileWriterPipeline(object):
    def __init__(self, raw_folder, decrypted_folder):
        self.raw_folder = raw_folder
        self.decrypted_folder = decrypted_folder

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            raw_folder=crawler.settings.get('RAW_FOLDER'),
            decrypted_folder=crawler.settings.get('DECRYPTED_FOLDER'),
        )

    def format_item(self, item, is_final):

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
            item['flag_1'] = 0

        if 'flag_2' not in item:
            item['flag_2'] = 0

        if 'flag_3' not in item:
            item['flag_3'] = 0

        if 'home_odds' not in item:
            item['home_odds'] = ''

        if 'draw_odds' not in item:
            item['draw_odds'] = ''

        if 'away_odds' not in item:
            item['away_odds'] = ''

        item['final'] = '1' is is_final or '0'

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

    def is_valid_item(self, item):
        """Checks if given item is valid (has legitimate entries)
        Ex: Not a header row, not with irregular data
        """
        if 'home_odds' not in item and 'draw_odds' not in item and\
                'away_odds' not in item and 'post_time' not in item:
            return False
        return True

    def are_odds_same(self, str1, str2):
        odds1 = ','.join(str1.split(',')[-4:-1])
        odds2 = ','.join(str2.split(',')[-4:-1])
        return odds1 == odds2

    def process_item(self, item, spider):
        if not self.is_valid_item(item):
            logging.error(item)
            return item

        # Get file path for decrypeted data
        # Format Handicap_HAD/decrypted/2015/04/14/Shakhtar_Dontsk-Braga/Handicap_HAD
        if item.get('post_time') is None:
            return item

        dtobj = datetime.strptime(item.get('post_time'), '%Y-%m-%d %H:%M:%S HKT')

        # match_name = Shakhtar_Dontsk-Braga
        if item.get('home_team') is None or item.get('away_team') is None:
            return item
        match_name = "%s-%s" % (item.get('home_team').strip('"'),
                                item.get('home_team').strip('"'))


        decrypted_filepath = 'Handicap_HAD/decrypted/%s/%s/%s/%s/Handicap_HAD' % (dtobj.year, dtobj.month, dtobj.day, match_name)

        # Check if file needs to be changed
        file_path = os.path.join(self.decrypted_folder, decrypted_filepath)

        save_item = False

        if os.path.isfile(file_path):
            # Check if any odds changed
            with open(file_path, 'r') as data_file:
                last_data = data_file.readlines()[-1].strip()
                item_str = self.format_item(item, False)

                if not self.are_odds_same(last_data, item_str):
                    save_item = True
        else:
            save_item = True

        if save_item:
            parent_dir = os.path.dirname(file_path)
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir)

            # Saving item in file
            with open(file_path, 'a') as data_file:
                item_str = self.format_item(item, False)
                data_file.write(item_str)
                data_file.write('\n')

        return item
