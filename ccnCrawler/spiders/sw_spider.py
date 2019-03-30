import scrapy
import time
from ccnCrawler.items import CcncrawlerItem
import logging


class SwSpider(scrapy.Spider):
    name = "sw"

    def start_requests(self):
        urls = [
            "https://sw.cau.ac.kr/board/list?boardtypeid=7&menuid=001005005",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url =  "https://sw.cau.ac.kr/board"

        for i in range(1,11):
            item = CcncrawlerItem()
            logging.error(i)
            logging.error(response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) + ']/div/p[1]/a/text()').extract())

            item['url'] = url+response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) +']/div/p[1]/a/@href').extract()[0][1:]
            try:
                item['title'] = response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) + ']/div/p[1]/a/text()').extract()[1]
            except:
                item['title'] = response.xpath('//*[@id="boardForm"]/div[2]/ul/li['+ str(i) + ']/div/p[1]/a/text()').extract()[0].strip()
            
            yield {'src':'sw','item':item}

        
        
        