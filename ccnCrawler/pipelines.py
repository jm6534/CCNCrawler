# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

import json

#
#class CcncrawlerPipeline(object):
#    def process_item(self, item, spider):
#        return item

class JsonPipeline(object):
    
    def __init__(self):
        #move (old)new.json to history
        self.historyFile = open("history.json", 'rt', encoding='UTF-8')
        self.newFile = open("new.json","rt", encoding='UTF-8')
        try:
            self.old = json.loads(self.historyFile.read())
        except:
            self.old = json.loads("[]")
        try:
            self.new = json.loads(self.newFile.read())
        except:
            self.new  =json.loads("[]")
        self.historyFile.close()
        self.newFile.close()
        
        with open("history.json","wt",encoding='UTF-8') as outfile:
            json.dump(self.old+self.new, outfile, indent=4,ensure_ascii = False)
        
        self.historyFile = open("history.json", 'rt', encoding='UTF-8')
        self.articles = json.loads(self.historyFile.read())
        self.newFile = open("new.json", 'wb')
        self.exporter = JsonItemExporter(self.newFile, encoding='utf-8', ensure_ascii=False, indent = 4)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.newFile.close()
 
    def process_item(self, item, spider):
        for article in self.articles:
            if (item["title"] == article["title"]):
                return
        self.exporter.export_item(item)
