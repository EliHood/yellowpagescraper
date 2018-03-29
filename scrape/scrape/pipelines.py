# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import re
import os
import shutil

SRCFILE = '/Users/poweruser/Applications/pythonwork/bbbscrap2/scrape/output%s.csv'
DESTINATION_FOLDER = '/Users/poweruser/Applications/pythonwork/leadparser/newfiles'

class myExporter(object):

    def __init__(self):
        i = 0
        while os.path.exists(SRCFILE % i):
            i += 1
        self.filename = SRCFILE % i
        with open(self.filename, 'w') as output:
            output = csv.writer(output)
            output.writerow(['Email', 'Website', 'Phone Number', 'Location'])

    def process_item(self, item, spider):
        with open(self.filename, 'a') as output:
            output = csv.writer(output)
            output.writerow([item['email'],
                             item['website'],
                             item['phonenumber'],
                             item['location']])
        folder = os.path.join(DESTINATION_FOLDER, os.path.basename(self.filename))
        shutil.copy(self.filename, folder)
        return item

