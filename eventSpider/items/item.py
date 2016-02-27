from scrapy.item import Item, Field


'''
	this item is used to store the craled information
'''
class EventItem(Item):
	# define the fields for your item here like:
	srcUrl = Field()
	
	title = Field()
	
	eventDate = Field()

	location = Field()
	
	organizer = Field()

	keywords = Field()

	introduction = Field()
	
	''' we hash the event key words, date, location to make sure a event is unique'''
	hashcode = Field()

	image_urls = Field()
	images = Field()


'''
	This object is used to filter request URL
'''
class VisitedURL(Item):
	url = Field()
	orgDupURL = Field()