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

    def process_item(self, item, spider):
        file_path = os.path.join(self.dump_folder, 'temp.txt')
        with open(file_path, 'a') as data_file:
            content = str(item)
            data_file.write(content)
        return item
