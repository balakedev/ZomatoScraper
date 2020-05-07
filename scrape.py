import scrapy, time, re, random

# Scrapy shell scrapy spider for zomato
# Originally developed by Blake Waldron 20/12/18

class SfScrape2Spider(scrapy.Spider):
	"""docstring for AuthorSpider"""

	name ="zomato"
	start_urls = ["https://www.zomato.com/byron-bay-nsw/byron-bay-restaurants?page=1"]

	def parse(self, response):
		counter = 1
		# gets list of all urls on page 'start_urls'. Gets hred attribute from all links only inside the restaurant list div
		urls = response.css("#orig-search-list > div > div.content > div > article > div.pos-relative.clearfix > div > div.col-s-16.col-m-12.pl0 > div:nth-child(1) > div.col-s-12 > a.result-title::attr(href)").extract()

		for url in urls:
			#get random number between 2-6
			for x in range(1):
     			 randSleep = random.randint(2,6)
     		#if the current 'counter' (restaurant) number is divisible by 15, sleep the random number between 2-6 from randSleep
			if counter % 15 == 0:
				time.sleep(randSleep)

			url = response.urljoin(url)

			#go to the restaurant page (parse_details)
			yield scrapy.Request(url=url, callback=self.parse_details)

			#this restaurant is done, onto the next one! 
			counter = counter + 1


		#Find the next pagination link
		next_page_url = response.css('#search-results-container > div.search-pagination-top.clearfix.mtop > div.row > div.col-l-12 > div > div > a.paginator_item.next.item::attr(href)').extract_first()
		next_page_url = response.urljoin(next_page_url)
		
		#if there is another page, send it it to the parse function to repeat the page scrape
		if next_page_url:
			next_page_url = response.urljoin(next_page_url)
			yield scrapy.Request(url=next_page_url, callback=self.parse)

	#this will extract that data by css / xpath 
	def parse_details(self, response):

		b4title = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segment.res-header-overlay.vr > div > div.res-header-overlay.brbot > div:nth-child(1) > div.col-l-12 > h1 > a::text").extract_first()
		b4suburb = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segment.res-header-overlay.vr > div > div.res-header-overlay.brbot > div:nth-child(1) > div.col-l-12 > div.mb5.pt5.clear > a::text").extract_first()
		b4rating = response.xpath("//div[6]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/text()").extract_first()
		b4phone = response.css("#phoneNoString > span > span > span").extract_first()
		b4price = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segments.mbot > div > div.col-l-1by3.pl0.pr20 > div.mbot.mtop > div > div > span:nth-child(3)").extract_first()

		# hours grab
		b4monday = response.css("[id='res-week-timetable'] > table > tr:nth-child(1) > td:nth-child(2)").extract_first()
		b4tuesday = response.css("[id='res-week-timetable'] > table > tr:nth-child(2) > td:nth-child(2)").extract_first()
		b4wednesday = response.css("[id='res-week-timetable'] > table > tr:nth-child(3) > td:nth-child(2)").extract_first()
		b4thursday = response.css("[id='res-week-timetable'] > table > tr:nth-child(4) > td:nth-child(2)").extract_first()
		b4friday = response.css("[id='res-week-timetable'] > table > tr:nth-child(5) > td:nth-child(2)").extract_first()
		b4saturday = response.css("[id='res-week-timetable'] > table > tr:nth-child(6) > td:nth-child(2)").extract_first()
		b4sunday = response.css("[id='res-week-timetable'] > table > tr:nth-child(7) > td:nth-child(2)").extract_first()
		#end hours grab

		b4dining = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segment.res-header-overlay.vr > div > div.res-header-overlay.brbot > div:nth-child(1) > div.col-l-12 > div.mb5.pt5.clear > span.res-info-estabs.grey-text.fontsize3 > a").extract_first()
		b4cuisine = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segments.mbot > div > div.col-l-1by3.pl0.pr20 > div:nth-child(2) > div > div > a::text").extract_first()
		b4address = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segments.mbot > div > div:nth-child(2) > div:nth-child(3) > div > div > span:nth-child(1)").extract_first()
		b4extras = response.css("#mainframe > div.wrapper.mtop > div > div.res-info-left.col-l-12 > div.ui.segments.mbot > div > div:nth-child(3) > div.pbot0.res-info-group > div").extract_first()
		b4image = response.css("#progressive_image::attr(data-url)").extract_first()
		b4image2 = response.css("#progressive_image > div.photosContainer.header-photo-chrousal > a:nth-child(1) > div::attr(data-original)").extract_first()

		#cast to string
		#b4title = str(b4title);
		#b4suburb = str(b4suburb);
		#b4dining = str(b4dining);
		#b4cuisine  = str(b4cuisine);
		#b4address = str(b4address);
		#b4extras = str(b4extras);
		b4rating = str(b4rating)
		b4price = str(b4price)

		b4monday = str(b4monday)
		b4tuesday = str(b4tuesday)
		b4wednesday = str(b4wednesday)
		b4thursday = str(b4thursday)
		b4friday = str(b4friday)
		b4saturday = str(b4saturday)
		b4sunday = str(b4sunday)

		#cleaning data
		title = re.sub("<.*?>", "", b4title)
		suburb = re.sub("<.*?>", "", b4suburb)
		rating = re.sub("<.*?>", "", b4rating)
		phone =  re.sub("<.*?>", "", b4phone)
		price = re.sub("<.*?>", "", b4price)

		#hours clean
		#monday =  re.sub("<.*?>", " ", b4monday)
		#tuesday =  re.sub("<.*?>", " ", b4tuesday)
		#wednesday =  re.sub("<.*?>", " ", b4wednesday)
		#thursday =  re.sub("<.*?>", " ", b4thursday)
		#friday =  re.sub("<.*?>", " ", b4friday)
		#saturday =  re.sub("<.*?>", " ", b4saturday)
		#sunday =  re.sub("<.*?>", " ", b4sunday)
		#end hours clean


		#Get raw values ( strip of html ) & existence check
		if b4cuisine: 
			cuisine =  re.sub("<.*?>", "", b4cuisine)
		else: 
			cuisine = "Unknown cuisine"

		address =  re.sub("<.*?>", " ", b4address)

		if b4extras is not None:
			extras =  re.sub("<.*?>", " ", b4extras)

		if b4image:
			image =  b4image
		else:	
			image =  str(b4image2)
			image = re.sub("\\?(.*)", "", image)

		if b4dining:
			dining = re.sub("<.*?>", " ", b4dining)
		else:
			dining = "Unknown"


		finalTitle = re.sub("\\n[^A-z]+", "", title)
		finalSuburb = re.sub("\\n[^A-z]+", "", suburb)
		finalDining = re.sub("\\n[^A-z]+", "", dining)
		finalRating = re.sub("\\n[^0-9]+", "", rating)
		finalPhone = re.sub("<.*?>", "", phone)
		finalCuisine = re.sub("<.*?>", "", cuisine)
		finalAddress = re.sub("<.*?>", "", address)
		finalprice = re.sub("<.*?>", "", price)


		if b4extras is not None:
			finalExtras = re.sub("\\n[^A-z]+", "", extras)
		else:
			finalExtras = "We've got no dietary knowledge about this venue! Help out the nibblit community by telling us what you know."
		
		finalImage = image
		#write to json file - scrapy runspider zomatoscrape.py -o scrapeName.json
		yield {
		'title' : finalTitle,
		'suburb' : finalSuburb,
		'dining' : finalDining,
		'rating' : finalRating,
		'phone' : finalPhone,
		'hours' : {
			'monday': b4monday,
			'tuesday': b4tuesday,
			'wednesday': b4wednesday,
			'thursday': b4thursday,
			'friday': b4friday ,
			'saturday': b4saturday,
			'sunday': b4sunday
		},
		'cuisine' : finalCuisine,
		'address' : finalAddress,
		'extras' : finalExtras,
		'image' : finalImage,
		'price' : finalprice
		}