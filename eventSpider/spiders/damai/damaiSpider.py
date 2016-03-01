#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from selenium import webdriver

from eventSpider.items.item import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from eventSpider.spiders.damai.util import DamaiDateUtil, DamaiLocationUtil
from eventSpider.util.keywords.keywords import keyWordGenerator
from scrapy.contrib.spiders import CrawlSpider

class damaiSpider(CrawlSpider):
    name = "damai"
    allowed_domains = ["damai.cn"]
        
    # for testing
    start_urls = [
        "http://www.damai.cn/projectlist.do?pageIndex=%d" % (i + 1) for i in range(1)
        # , "http://item.damai.cn/90925.html"
    ]

    
    link_extractor = {
                      'page': '//ul[@id="performList"]/li/div[@class="ri-infos"]/h2/a/@href',
                      }
    
    # put all xpatg query together
    query = {
             'title':'//div[@class="m-goods"]/h2[@class="tt"]/span[@class="txt"]/text()',
             'dates':'//div[@id="performList"]/div[@class="ct"]/ul/li',
             'location':'//div[@class="m-sdbox m-venue"]/div[@class="ct"]/p[@class="txt"]/a[@target="_blank"]/text()',
             'image_urls':'//img[@id="projectPoster"]/@src-original',
             'descripton':'//div[@class="pre"]',
             }

    def __init__(self, **kwargs):
        CrawlSpider.__init__(self)
        self.browser = webdriver.Firefox() 
        
    def __del__(self):
        self.browser.close()
    
    # this method will be called before the spider quits
    def closed(self, reason):
        self.__del__()

    def parseTest(self, response):
        link = "http://item.damai.cn/90925.html"
        yield Request(link, callback=self.parseEvent)
        
    def parse(self, response):       
        # time.sleep(2) 
        
        hxs = HtmlXPathSelector(response)
        links = []
        urls = hxs.select(self.link_extractor['page']).extract()
        length = len(urls)
         
        for i in range(0, length):
            links.append(urls[i])
        for link in links:
            yield Request(link, callback=self.parseEvent)
         
    def parseEvent(self, response):
        '''
        filename = response.url.split("/")[3]
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        '''

        self.browser.get(response.url)

        # date = self.browser.find_elements_by_class_name('itm itm-sel')
        seleniumDates = self.browser.find_elements_by_xpath(self.query['dates'])
        dates = []
        for date in seleniumDates:        
            # only add only if the date is valid, we may see some non date related Chinese
            if DamaiDateUtil.isValidDate(date.text):
                dates.append(date.text)

        item = EventItem()
        item['srcUrl'] = response.url        
        item['title'] = response.selector.xpath(self.query['title'])[0].extract()
        item['keywords'] = keyWordGenerator.generateKeywords(item['title'])

        item['eventDate'] = DamaiDateUtil.createEventDate(dates)

        locationText = response.selector.xpath(self.query['location'])[0].extract()
        regionaddr = DamaiLocationUtil.getRegionAddresse(locationText)
        item['location'] = DamaiLocationUtil.createLocation(regionaddr[0], regionaddr[1])
        
        item['organizer'] = "damai.cn"

        item['image_urls'] = response.selector.xpath(self.query['image_urls']).extract()

        item['description'] = response.selector.xpath(self.query['descripton'])[0].extract()
        
        item['fingerprint'] = str(item.computeFingerprint())

        return item  
