import scrapy
import time
from ccnCrawler.items import CcncrawlerItem
import logging


class SwSpider(scrapy.Spider):
    name = "sw"

    def start_requests(self):
        yield scrapy.Request(url="https://sw.cau.ac.kr/board/list?boardtypeid=7&menuid=001005005", callback=self.parseSW)
        yield scrapy.Request(url="http://cse.cau.ac.kr/sub05/sub0501.php", callback=self.parseCSE)
        yield scrapy.Request(url="http://ict.cau.ac.kr/20150610/sub05/sub05_01_list.php", callback=self.parseICT)


    def parseSW(self, response):
        url =  "https://sw.cau.ac.kr/board"

        for i in range(1,11):
            item = CcncrawlerItem()
            item['url'] = url+response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) +']/div/p[1]/a/@href').extract()[0][1:]
            try:
                item['title'] = response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) + ']/div/p[1]/a/text()').extract()[1]
            except:
                item['title'] = response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) + ']/div/p[1]/a/text()').extract()[0].strip()
            
            yield {'src':'sw','item':item}
   
    def parseCSE(self, response):
        url = "http://cse.cau.ac.kr/sub05/sub0501.php?"
        for i in range(1,11):
            item = CcncrawlerItem()
            item['url'] = url+response.xpath('//*[@id="listpage_form"]/table/tbody/tr['+str(i)+']/td[3]/a/@href').extract()[0]
            item['title'] = response.xpath('//*[@id="listpage_form"]/table/tbody/tr['+str(i)+']/td[3]/a/text()').extract()[1].strip()
            
            yield {'src':'cse','item':item}

    def parseICT(self,response):
        url = "http://ict.cau.ac.kr/20150610/sub05/sub05_01_list.php?cmd=view&cpage=1&idx="
        for i in range(1,11):
            item = CcncrawlerItem()
            item['url'] = url+response.xpath('/html/body/div/div[4]/div/table/tbody/tr['+str(i)+']/td[2]/a/@href').extract()[0][19:23]
            item['title'] = response.xpath('/html/body/div/div[4]/div/table/tbody/tr['+str(i)+']/td[2]/a/text()').extract()[0]

            yield {'src':'ict','item':item}


        
        
        