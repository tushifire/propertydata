# -*- coding: utf-8 -*-
import scrapy


class AppartSpider(scrapy.Spider):
	name = 'appart'
	allowed_domains = ['www.makaan.com']
	start_urls = ['https://www.makaan.com/pune-residential-property/buy-property-in-pune-city?page=1']
	custom_settings = {
	# specifies exported fields and order
	'FEED_EXPORT_FIELDS': ["price", "bhk", "area","carpetarea","pricepersquare","additionalrooms","status","possesiondate","locality","projectname","age","roadfaceing","bathroom","floor","balconies", "totalfloor","neworold","opensides","facing","overlooking","ownership","amenitiesavailable","amenitiesnot"],
	}
		
	def parse(self, response):
		urls = response.xpath('//div[@data-type="listing-card"]/@itemid').extract()
		for url in urls:
			url = response.urljoin(url)
			yield scrapy.Request(url=url, callback=self.parse_details)

        # follow pagination link
		for i in range(1902,1943):
			pagelink = 'https://www.makaan.com/pune-residential-property/buy-property-in-pune-city?page={}'.format(i)
			next_page_url = response.urljoin(pagelink)
			yield scrapy.Request(url=next_page_url, callback=self.parse)
			#92 pages done 1st hour
		
	#def parse(self,response):
		#f = open("22k24k.txt", "r")
		#line = f.readline()
		#while line:
			#content = line.strip()
			#yield scrapy.Request(url=content, callback=self.parse_details)
			#line = f.readline()	
		#f.close()

	def parse_details(self, response):
		item = {
        	'price' : response.xpath('//span[@class="price"]//meta[@itemprop="price"]/@content').extract(),
        	'bhk' : response.xpath('//h1//span[@class="type"]/text()').extract(),
        	#'address' : response.xpath('//div[@class="p_text"]/span/text()').extract(),
        	#'bedroom' : response.xpath('//div[@class="seeBedRoomDimen"]/text()').extract_first(),
        	'area' :response.xpath('//h1[@class="type-wrap"]//span[@class="size"]/text()').extract(),
        	'carpetarea' : response.xpath('//td[@id="Carpet area"]/text()').extract(),
        	'pricepersquare' : response.xpath('//div[@class="rate-wrap"]/text()').extract(),
        	'additionalrooms' : response.xpath('//td[@id="Additional Rooms"]/text()').extract(),
        	'status' : response.xpath('//td[@id="Status"]/text()').extract(),
        	'possesiondate' : response.xpath('//td[@id="Possession Date"]/text()').extract(),
        	'locality' : response.xpath('//span[@class="ib loc-name"]/text()').extract(),
        	'projectname' : response.xpath('//span[@class="ib"]//span[@itemprop="name"]/text()').extract(),
        	'age' : response.xpath('//td[@id="Age of Property"]/text()').extract(),
        	'roadfaceing' : response.xpath('//td[@id="Road facing main entry"]/text()').extract(),
        	'bathroom' : response.xpath('//td[@id="Bathrooms"]/text()').extract(),
        	'floor' : response.xpath('//td[@id="Floor"]/text()').extract(),
        	'balconies' : response.xpath('//td[@id="Balconies"]/text()').extract(),
        	'totalfloor' : response.xpath('//td[@id="Total Floors"]/text()').extract(),
        	'neworold' : response.xpath('//td[@id="New/Resale"]/text()').extract(),
        	'opensides' :  response.xpath('//td[@id="No. open sides"]/text()').extract(),
        	'facing' : response.xpath('//td[@id="Facing"]/text()').extract(),
        	'overlooking' : response.xpath('//td[@id="Overlooking"]/text()').extract(),
        	'ownership' :response.xpath('//td[@id="Ownership Type"]/text()').extract(),
        	'amenitiesavailable' : response.xpath('//div[@class="icons-list js-list js-mobscroll"]//div[@class="listitem  js-moblist-item"]//div[@class="txt"]/text()').extract(),
        	'amenitiesnot' : response.xpath('//div[@class="icons-list js-list js-mobscroll"]//div[@class="listitem disabled js-moblist-item"]//div[@class="txt"]/text()').extract(),
        	
        	}
		yield item
		

