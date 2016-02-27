import scrapy

from eventSpider.items.item import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from textAnalyzer.jieba.keywords import keyWordGenerator
import time
from eventSpider.items.dateUtil import DoubanDateUtil


class doubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    
    start_urls = ["http://www.douban.com/location/wuhan/events/future-all?start=%d" %(i*10) for i in range(2)]
    
    # for testing
    '''    
    start_urls = [
        "http://www.douban.com/event/26314891/",
    ]

    def parse(self, response):
        link="http://www.douban.com/event/26314891/"
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

        item['srcUrl']=response.url
        item['title']=response.selector.xpath('//div[@id="event-info"]/div[@class="event-info"]/h1[@itemprop="summary"]/text()')[0].extract()

        item['keywords']=keyWordGenerator.generateKeywords(item['title'])

        '''
            customized dates needs to be checked, multiple class "calendar-str-item"
        '''
         #item['startTime']=response.selector.xpath('//div[@id="event-info"]/div[@class="event-info"]/div[@class="event-detail"]/ul[@class="calendar-strs"/li[@class="calendar-str-item"]/text()')[0].extract()
        dateText = response.selector.xpath('//div[@id="event-info"]/div[@class="event-info"]/div[@class="event-detail"][1]/ul/li/text()')[0].extract()
        item['eventDate']=DoubanDateUtil.createEventDate(dateText)

        item['location']=response.selector.xpath('//div[@class="event-detail"]/span[@itemprop="address"]')[0].extract()

        item['organizer']=response.selector.xpath('//ul[@class="member_photo"]/li/div[@class="member-tip"]/div[@class="detail"]/a/text()')[0].extract()

        item['image_urls']=response.selector.xpath('//img[@id="poster_img"]/@src').extract()

        item['introduction']= response.selector.xpath('//div[@id="link-report"]/div')[0].extract()


        return item  
    
    
            