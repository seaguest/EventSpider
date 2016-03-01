#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import scrapy

from eventSpider.items.item import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from eventSpider.util.keywords.keywords import keyWordGenerator
from eventSpider.spiders.douban.util import DoubanDateUtil, DoubanLocationUtil

class doubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    
    # for testing
    testMode = True
    start_urls = [
                  # m "http://www.douban.com/location/wuhan/events/future-all?start=%d" % (i * 10) for i in range(2)
                  "http://www.douban.com/event/26260280"
    ]

    link_extractor = {
                  'page': '//li[@class="list-entry"]/div[@class="pic"]/a/@href',
                  }
    
    # put all xpatg query together
    query = {
             
             'title':'//div[@id="event-info"]/div[@class="event-info"]/h1[@itemprop="summary"]/text()',
             'dates':'//div[@id="event-info"]/div[@class="event-info"]/div[@class="event-detail"][1]/ul/li/text()',
             'region':'//div[@class="event-detail"]/span[@itemprop="address"]/span[@itemprop="region"]/text()',
             'address':'//div[@class="event-detail"]/span[@itemprop="address"]/span[@itemprop="street-address"]/text()',
             'organizer':'//ul[@class="member_photo"]/li/div[@class="member-tip"]/div[@class="detail"]/a/text()',
             'image_urls':'//img[@id="poster_img"]/@src',
             'descripton':'//div[@id="link-report"]/div',
             }

    def parse(self, response):       
        if self.testMode == True:
            yield Request(self.start_urls[0], callback=self.parseEvent)
        else:
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

        region = response.selector.xpath(self.query['region'])[0].extract()
        address = response.selector.xpath(self.query['address'])[0].extract()        
        item['location'] = DoubanLocationUtil.createLocation(region, address)
        
        item['organizer'] = response.selector.xpath(self.query['organizer'])[0].extract()

        item['image_urls'] = response.selector.xpath(self.query['image_urls']).extract()

        item['description'] = response.selector.xpath(self.query['descripton'])[0].extract()

        item['fingerprint'] = str(item.computeFingerprint())

        return item  
    
    
            
