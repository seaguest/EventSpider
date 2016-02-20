import scrapy

from eventSpider.items import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from textAnalyzer.jieba.keywords import keyWordGenerator
import time


class doubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
#    start_urls = [
#        "http://www.damai.cn/projectlist.do",
 #   ]
    start_urls = ["http://www.douban.com/location/wuhan/events/future-all?start=%d" %(i*10) for i in range(1)]
    
    # for testing
    '''
    start_urls = [
        "http://www.douban.com/event/25318078/",
    ]
    def parse(self, response):
        link="http://www.douban.com/event/25318078/"
        yield Request(link,callback=self.parseEvent)
    '''

    def parse(self, response):       
        #time.sleep(2) 

        hxs = HtmlXPathSelector(response)
        links = []
        urls = hxs.select('//li[@class="list-entry"]/div[@class="pic"]/a/@href').extract()
        length=len(urls)
         
        for i in range(0, length):
            links.append(urls[i])
        for link in links:
            yield Request(link,callback=self.parseEvent)
            
    def parseEvent(self, response):
        #filename = response.url.split("/")[4]
        #with open(filename, 'wb') as f:
        #url=response.selector.xpath('//ul[@id="performList"]/div[@class="ri-infos"]/h2/a/@href/text()')[0].extract()
        #f.write(response.body)
        
        item=EventItem()

        item['url']=response.url
        item['title']=response.selector.xpath('//div[@id="event-info"]/div[@class="event-info"]/h1[@itemprop="summary"]/text()')[0].extract()

        item['keywords']=keyWordGenerator.generateKeywords(item['title'])

       #item['startTime']=response.selector.xpath('//div[@id="event-info"]/div[@class="event-info"]/div[@class="event-detail"]/ul[@class="calendar-strs"/li[@class="calendar-str-item"]/text()')[0].extract()
        item['startTime']=response.selector.xpath('//div[@id="event-info"]/div[@class="event-info"]/div[@class="event-detail"][1]/ul/li/text()')[0].extract()

        item['location']=response.selector.xpath('//div[@class="event-detail"]/span[@itemprop="address"]')[0].extract()

        item['organizer']=response.selector.xpath('//ul[@class="member_photo"]/li/div[@class="member-tip"]/div[@class="detail"]/a/text()')[0].extract()

        item['image_urls']=response.selector.xpath('//img[@id="poster_img"]/@src').extract()

        item['introduction']= response.selector.xpath('//div[@id="link-report"]/div')[0].extract()


        return item  
    
    
            