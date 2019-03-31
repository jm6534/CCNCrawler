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
        self.list = ['sw','cse','ict']
        self.historyFiles = {}
        self.articles = {}
        self.exporters = {}
        self.newFiles = {}

        for element in self.list:          
            #move (old)new.json to history
            self.moveToHistory(element)
            #open history files to deal with json data
            self.historyFiles[element] = open("history_"+element+".json", 'rt', encoding='UTF-8')      
            self.articles[element] = json.loads(self.historyFiles[element].read())
            #open new files to write json data
            self.newFiles[element] = open("new_"+element+".json", 'wb')
            self.exporters[element] = JsonItemExporter(self.newFiles[element], encoding='utf-8', ensure_ascii=False, indent = 4)
            self.exporters[element].start_exporting()
 
    def close_spider(self, spider):
        #close all 'new' files
        for element in self.list:
            self.exporters[element].finish_exporting()
            self.historyFiles[element].close()
            self.newFiles[element].close()
        #combine all new json file to new.json
        self.combineNewJson()

 
    def process_item(self, item, spider):
        self.compareAndWrite(item)

    def moveToHistory(self,element):
        historyFile = open("history_"+element+".json", 'rt', encoding='UTF-8')
        newFile = open("new_"+element+".json","rt", encoding='UTF-8')
        try:
            self.old = json.loads(historyFile.read())
        except:
            self.old = json.loads("[]")
        try:
            self.new = json.loads(newFile.read())
        except:
            self.new  =json.loads("[]")
        historyFile.close()
        newFile.close()
        
        with open("history_"+element+".json","wt",encoding='UTF-8') as outfile:
            json.dump(self.old+self.new, outfile, indent=4,ensure_ascii = False)

    def compareAndWrite(self,item):
        for article in self.articles[item['src']]:
            if (item['item']["title"] == article["title"]):
                return
        self.exporters[item['src']].export_item(item['item'])
        return

    def combineNewJson(self):
        newData = {}
        newData1 = []
        for element in self.list:
            jsonFile = open('new_'+element+'.json','rt',encoding='UTF-8')
            newData[element] = json.loads(jsonFile.read())
            newData1 += newData[element]
            jsonFile.close()
        

        with open('new.json','wt',encoding='UTF-8') as outfile:
            json.dump(newData1, outfile, indent=4,ensure_ascii = False)