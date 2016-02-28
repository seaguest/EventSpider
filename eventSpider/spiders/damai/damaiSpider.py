#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from selenium import webdriver

from eventSpider.items.item import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from eventSpider.spiders.damai.util import DamaiDateUtil
from textAnalyzer.jieba.keywords import keyWordGenerator
from scrapy.contrib.spiders import CrawlSpider

class damaiSpider(CrawlSpider):
    name = "damai"
    allowed_domains = ["damai.cn"]
        
    start_urls = ["http://www.damai.cn/projectlist.do?pageIndex=%d" % (i + 1) for i in range(1)]

    # for testing
    '''    
    start_urls = [
        "http://item.damai.cn/94335.html",
    ]
    '''
    
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
        
    '''
    def parse(self, response):
        link="http://item.damai.cn/94335.html"
        yield Request(link,callback=self.parseEvent)

    '''
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
            dates.append(date.text)

        item = EventItem()
        item['srcUrl'] = response.url        
        item['title'] = response.selector.xpath(self.query['title'])[0].extract()
        item['keywords'] = keyWordGenerator.generateKeywords(item['title'])

        item['eventDate'] = DamaiDateUtil.createEventDate(dates)

        item['location'] = response.selector.xpath(self.query['location'])[0].extract()
        
        item['organizer'] = "damai.cn"

        item['image_urls'] = response.selector.xpath(self.query['image_urls']).extract()

        item['descripton'] = response.selector.xpath(self.query['descripton'])[0].extract()
        
        item['fingerprint'] = str(item.computeFingerprint())

        return item  
