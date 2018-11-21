import requests
import pandas
from bs4 import BeautifulSoup
import os


#Used headers/agent because the request was timed out and asking for an agent. 
#Using following code we can fake the agent.
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


SuburbName = (input("Please enter the Suburb Name: "))

pageCount = int((input("Please enter the pageCount: ")))


path = './crawls/'
os.chdir(path)
newFolder = str(SuburbName)
os.makedirs(newFolder)

newPath = './'+newFolder+'/'

os.chdir(newPath)

reqURL = (input("Please enter the URL: "))

pageID = 0;

pageSTR = str(pageID)

theURL = str(reqURL)

counter = 0

for pageID in range(pageCount): 

	response = requests.get(theURL + "&page=" + str(pageID),headers=headers)

	content = response.content
	soup = BeautifulSoup(content,"html.parser")

	top_rest = soup.find_all("div",attrs={"class": "ui cards"})
	# if top_rest:
	# 	print("found outter div.... \n")

	list_tr = top_rest[0].find_all("div",attrs={"class": "content"})
	# if list_tr:
	# 	print("found inner div.... \n")
		

	list_rest =[]
	for tr in list_tr:
		try:
		    dataframe ={}
		    dataframe["rest_name"] = (tr.find("a",attrs={"class": "result-title"})).text.replace('\n', ' ')
		    dataframe["rest_address"] = (tr.find("div",attrs={"class": "col-m-16 search-result-address grey-text nowrap ln22"})).text.replace('\n', ' ')
		    dataframe["rest_hours"] = (tr.find("div",attrs={"class": "res-timing clearfix"})).text.replace('\n', ' ')
		    dataframe["rest_type"] = (tr.find("a",attrs={"class": "zdark ttupper fontsize6"})).text.replace('\n', ' ')

		    counter = counter + 1

		    list_rest.append(dataframe)
		except AttributeError:
			print("ERROR")

	list_rest

	pageID + 1

	print("getting next page: " + str(pageID) + "\n\n")

	df = pandas.DataFrame(list_rest)
	df.to_csv("data" + str(pageID) +".csv",index=False)

print("total number of restraunts found: " + str(counter))