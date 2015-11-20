# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time, base64, json, os
import pymongo
from scrapy.exceptions import DropItem

class DatabaseEntryPipeline(object):

    collection_name = 'map'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'frictionle')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            _id = base64.b64encode(item['url'])
            result = self.db[self.collection_name].insert({
                '_id': _id,
                'u': item['url'],
                't': item['title'],
                'c': time.time()
            })
            item['urlb64'] = _id
        except pymongo.errors.DuplicateKeyError:
            raise DropItem("Duplicate item found: %s" % item['url'])
        else:
            return item


class FileWriterPipeline(object):
    def __init__(self, dump_folder):
        self.dump_folder = dump_folder

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            dump_folder=crawler.settings.get('DUMP_FOLDER'),
        )

    def process_item(self, item, spider):
        file_path = os.path.join(self.dump_folder, spider.site, spider.name, item['urlb64'])
        with open(file_path, 'wb') as data_file:
            content = json.dumps(dict(item))
            data_file.write(content)
        return item
