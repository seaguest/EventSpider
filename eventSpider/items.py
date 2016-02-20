from scrapy.item import Item, Field


class EventItem(Item):
	# define the fields for your item here like:
	url = Field()
	title = Field()
	
	startTime = Field()
	endTime = Field()
	
	location = Field()
	
	organizer = Field()

	keywords = Field()

	introduction = Field()

	image_urls = Field()
	images = Field()
