# ZomatoScraper
Tool for scraping basic information off zomato.


Used for pages that look like the following:
https://www.zomato.com/melbourne/fitzroy-restaurants?all=1&page=2


The scrape.py file will create a folder of the location that you want to scrape and create individual pages .csv files for each page.
 
You can tell it how many pages you wish to scrape

the link you should enter for the scraper to work should look like the following 
https://www.zomato.com/melbourne/fitzroy-restaurants?all=1

	*the scraper will automatically add &page=# at the end.
 

Note: 
===========================================
if you want to merge all the .csv files into a single file, this can be done in cmd by navigating to the file of all the .csv files and typing the following:

copy *.csv fileName.csv

Dependencies are:

bs4 (beautiful soup)
requests
os
pandas

The above can be installed using pip.