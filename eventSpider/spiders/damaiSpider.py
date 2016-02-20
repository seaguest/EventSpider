import scrapy

from eventSpider.items import EventItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
import time

class damaiSpider(scrapy.Spider):
    name = "damai"
    allowed_domains = ["damai.cn"]
#    start_urls = [
#        "http://www.damai.cn/projectlist.do",
 #   ]
    start_urls = ["http://www.damai.cn/projectlist.do?pageIndex=%d" %(i+1) for i in range(10)]

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
            
    def parseEvent(self, response):
        #filename = response.url.split("/")[3]
        #with open(filename, 'wb') as f:
        # url=response.selector.xpath('//ul[@id="performList"]/div[@class="ri-infos"]/h2/a/@href/text()')[0].extract()
        #f.write(response.body)
        item=EventItem()
        item['url']=response.url
        
        item['title']=response.selector.xpath('//div[@class="m-goods"]/h2[@class="tt"]/span[@class="txt"]/text()')[0].extract()
        
        item['startTime']=response.selector.xpath('//div[@class="m-sdbox m-showtime"]/div[@class="ct"]/span[@class="txt"]/text()')[0].extract()
        
        item['location']=response.selector.xpath('//div[@class="m-sdbox m-venue"]/div[@class="ct"]/p[@class="txt"]/a[@target="_blank"]/text()')[0].extract()
        
        item['organizer']="damai.cn"

        item['image_urls']=response.selector.xpath('//img[@id="projectPoster"]/@src-original').extract()

        item['introduction']=response.selector.xpath('//div[@class="pre"]')[0].extract()
        return item  
            