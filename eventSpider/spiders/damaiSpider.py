import scrapy

from eventSpider.items.item import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
import time
from eventSpider.items.dateUtil import DamaiDateUtil

class damaiSpider(scrapy.Spider):
    name = "damai"
    allowed_domains = ["damai.cn"]

    #start_urls = ["http://www.damai.cn/projectlist.do?pageIndex=%d" %(i+1) for i in range(1)]

    # for testing    
    start_urls = [
        "http://item.damai.cn/94335.html",
    ]

    def parse(self, response):
        link="http://item.damai.cn/94335.html"
        yield Request(link,callback=self.parseEvent)

    '''
    def parse(self, response):       
        #time.sleep(2) 
        
        hxs = HtmlXPathSelector(response)
        links = []
        urls = hxs.select('//ul[@id="performList"]/li/div[@class="ri-infos"]/h2/a/@href').extract()
        length=len(urls)
         
        for i in range(0, length):
            links.append(urls[i])
        for link in links:
            yield Request(link,callback=self.parseEvent)
            
    '''
    def parseEvent(self, response):
        '''
        filename = response.url.split("/")[3]
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        '''
        item=EventItem()
        item['srcUrl']=response.url
        
        item['title']=response.selector.xpath('//div[@class="m-goods"]/h2[@class="tt"]/span[@class="txt"]/text()')[0].extract()
        
        dateText = response.selector.xpath('//div[@class="m-sdbox m-showtime"]/div[@class="ct"]/span[@class="txt"]/text()')[0].extract()
        item['eventDate']=DamaiDateUtil.createEventDate(dateText);


        item['location']=response.selector.xpath('//div[@class="m-sdbox m-venue"]/div[@class="ct"]/p[@class="txt"]/a[@target="_blank"]/text()')[0].extract()
        
        item['organizer']="damai.cn"

        item['image_urls']=response.selector.xpath('//img[@id="projectPoster"]/@src-original').extract()

        item['introduction']=response.selector.xpath('//div[@class="pre"]')[0].extract()
        return item  
