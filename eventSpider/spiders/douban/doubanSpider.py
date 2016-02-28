#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import scrapy

from eventSpider.items.item import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from textAnalyzer.jieba.keywords import keyWordGenerator
from eventSpider.spiders.douban.util import DoubanDateUtil

class doubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    
    # start_urls = ["http://www.douban.com/location/wuhan/events/future-all?start=%d" % (i * 10) for i in range(2)]
    
    link_extractor = {
                  'page': '//li[@class="list-entry"]/div[@class="pic"]/a/@href',
                  }
    
    # put all xpatg query together
    query = {
             
             'title':'//div[@id="event-info"]/div[@class="event-info"]/h1[@itemprop="summary"]/text()',
             'dates':'//div[@id="event-info"]/div[@class="event-info"]/div[@class="event-detail"][1]/ul/li/text()',
             'location':'//div[@class="event-detail"]/span[@itemprop="address"]',
             'organizer':'//ul[@class="member_photo"]/li/div[@class="member-tip"]/div[@class="detail"]/a/text()',
             'image_urls':'//img[@id="poster_img"]/@src',
             'descripton':'//div[@id="link-report"]/div',
             }

    # for testing
 
    start_urls = [
        "http://www.douban.com/event/26260280/",
    ]

    def parse(self, response):
        link = "http://www.douban.com/event/26260280"
        yield Request(link, callback=self.parseEvent)
 

    def parse0(self, response):       
        # time.sleep(2) 

        hxs = HtmlXPathSelector(response)
        links = []
        urls = hxs.select().extract(self.link_extractor['page'])
        length = len(urls)
         
        for i in range(0, length):
            links.append(urls[i])
        for link in links:
            yield Request(link, callback=self.parseEvent)
       
    def parseEvent(self, response):        
        item = EventItem()

        item['srcUrl'] = response.url
        item['title'] = response.selector.xpath(self.query['title'])[0].extract()
        item['keywords'] = keyWordGenerator.generateKeywords(item['title'])

        '''
            customized dates needs to be checked, multiple class "calendar-str-item"
        '''
        dateText = response.selector.xpath(self.query['dates'])[0].extract()
        item['eventDate'] = DoubanDateUtil.createEventDate(dateText)

        item['location'] = response.selector.xpath(self.query['location'])[0].extract()

        item['organizer'] = response.selector.xpath(self.query['organizer'])[0].extract()

        item['image_urls'] = response.selector.xpath(self.query['image_urls']).extract()

        item['descripton'] = response.selector.xpath(self.query['descripton'])[0].extract()

        item['fingerprint'] = str(item.computeFingerprint())

        return item  
    
    
            
