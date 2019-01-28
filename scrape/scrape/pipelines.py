# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import re
import os
import shutil
import pymongo
from scrapy.conf import settings
from scrapy import log


# get current working directory
cwd = os.getcwd()
# get the file 
ourPath = '/output%s.csv'
# appends the file to the working directory
SRCFILE = cwd + os.path.join(ourPath)

DESTINATION_FOLDER = os.path.join( os.getenv('HOME'), 'Downloads')
# MyDest = '/pythonwork/leadparser'

class myExporter(object):

    def __init__(self):
        i = 0
        while os.path.exists(SRCFILE % i):
            i += 1
        self.filename = SRCFILE % i
        with open(self.filename, 'w') as output:
            output = csv.writer(output)
            output.writerow(['Email', 'Website', 'Phone Number', 'Location'])
        connection = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.email = self.collection.find({"email": item['email']})
        self.collection.ensure_index('email', unique=True, dropDups=True)
        self.collection.insert(dict(item))
        log.msg("Item wrote to MongoDB database {}, collection {}, at host {}, port {}".format(
            settings['MONGODB_DATABASE'],
            settings['MONGODB_COLLECTION'],
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']))
        with open(self.filename, 'a') as output:
            output = csv.writer(output)
            output.writerow([item['email'],
                             item['website'],
                             item['phonenumber'],
                             item['location']])
        folder = os.path.join(DESTINATION_FOLDER, os.path.basename(self.filename))
        shutil.copy(self.filename, folder)
        return item

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item