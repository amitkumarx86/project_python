import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
import thread
import sys

out = csv.writer(open("books.csv","w"),lineterminator='\n')
header=['Title','author','year','genre','language','goodread link','amazon link','rating','pages','coverImage']
out.writerow(header)

linkDict = list()
def fetchLinks():
	url = "https://www.goodreads.com/list"
	get_url = requests.get(url)
	get_text = get_url.text
	soup = BeautifulSoup(get_text, "html.parser")
	divs = soup.find_all("ul","listTagsTwoColumn")

	thefile = open('firstLevel.links', 'w')

	for div in divs:
		for a in div.find_all("a"):
			linkDict.append("https://www.goodreads.com"+str(a.get('href')))
		
	next = soup.find("a","actionLink right tagMoreLink").get('href')
	# next = ""
	while(next != ""):
		url = "https://www.goodreads.com"+next
		get_url = requests.get(url)
		get_text = get_url.text
		soup = BeautifulSoup(get_text, "html.parser")
		div = soup.find("div","leftContainer")
		links = div.find_all("a","actionLinkLite")
		for a in links:
			linkDict.append("https://www.goodreads.com"+str(a.get('href')))
		
		
		# call second page link fetching
		print "Got "+str(len(linkDict))+" of type 1 links"
		try:
			# fetchLinks2(linkDict)
			# write in files
			
			for item in linkDict:
  				thefile.write("%s\n" % item)
		except:
			print "fetchLinks2 went wrong"
		linkDict[:] = []


		try:
			next = soup.find("a","next_page").get('href')
		except:
			next = ""

def fetchLinks2(linkDict):
	thefile = open('secondLevel.links', 'a')

	links = list()
	# print linkDict
	print "FetchLink2 called"
	for value in linkDict:
		print value
		get_url = requests.get(value)
		get_text = get_url.text
		soup = BeautifulSoup(get_text, "html.parser")
		linksList = soup.find_all("a","listTitle")
		# print linksList
		links.extend(["https://www.goodreads.com"+str(href.get('href')) for href in linksList])
		next = soup.find("a","next_page").get('href')
		# next = ""
		while(next != ""):
			url = "https://www.goodreads.com"+next
			get_url = requests.get(url)
			get_text = get_url.text
			soup = BeautifulSoup(get_text, "html.parser")
			linksList = soup.find_all("a","listTitle")
			links.extend(["https://www.goodreads.com"+str(href.get('href')) for href in linksList])
			
			print "Got "+str(len(links))+" of type 2 links"
			try:
				# fetchLinks3(links)
				for item in links:
  					thefile.write("%s\n" % item)
			except:
				print "fetchLinks2 went wrong"
			links[:] = []	


			try:
				next = soup.find("a","next_page").get('href')
			except:
				next = ""	

def fetchLinks3(links):
	print "FetchLink3 called"
	finalLinks = list()
	for url in links:
		get_url = requests.get(url)
		get_text = get_url.text
		soup = BeautifulSoup(get_text, "html.parser")
		finalLinks.extend([ "https://www.goodreads.com"+str(href.get('href')) for href in soup.find_all("a","bookTitle")])
		# print finalLinks
		next = soup.find("a","next_page").get('href')
		# next = ""
		while(next != ""):
			url = "https://www.goodreads.com"+next
			get_url = requests.get(url)
			get_text = get_url.text
			soup = BeautifulSoup(get_text, "html.parser")
			finalLinks.extend([ "https://www.goodreads.com"+str(href.get('href')) for href in soup.find_all("a","bookTitle")])
			print "Updating csv with "+str(len(finalLinks))+" books."
			try:
				for url in finalLinks:
					getBookInfo(url)
			except:
				print "temp book update failed"
			print "Updated csv with "+str(len(finalLinks))+" books."
			finalLinks[:] = []


			try:
				next = soup.find("a","next_page").get('href')
			except:
				next = ""
			

def getBookInfo(url):
	# get book attributes 
	get_url = requests.get(url)
	get_text = get_url.text
	soup = BeautifulSoup(get_text, "html.parser")

	if "(" in str(soup.find_all("h1")[0].text.strip()):
		bookTitle = str(soup.find_all("h1")[0].text.strip()).split("(")[0].replace("\n","")
	else:
		bookTitle = str(soup.find_all("h1")[0].text.strip()).split("(")[0].replace("\n","")
	
	coverImage = ""
	rating     = ""
	noOfPages  = ""
	grLink     = url
	amLink     = ""
	pages      = ""
	author     = ""
	year       = ""
	language   = ""
	genre      = ""

	try:
		coverImage = soup.find('img',{'id':"coverImage"}).get('src')
	except:
		print "coverImage not found for "+url
	try:
		rating     = soup.find_all("span",{"class":"average"})[0].text.strip()
	except:
		print "rating not found for "+url
	try:
		noOfPages  = soup.find("span",{"itemprop":"numberOfPages"}).string.strip().split(" ")[0]
	except:
		print "page count not found for "+url
	try:
		author     = soup.find("a",{"class":"authorName"}).text.strip().replace("\n","")
	
	except:
		print "author not found for "+url
	try:
		year       = str(soup.find_all("div","row")[1].text.strip().split("\n")[1].strip())
		year       = re.findall(r"[0-9]{4,4}", year)[0]
	except:
		print "year not found for "+url
	try:
		language   = soup.find("div",{"itemprop":"inLanguage"}).string.strip().replace("\n","")
	
	except:
		print "lang not found for "+url
	try:
		amazonLink = "https://www.goodreads.com"+soup.find_all("a","buttonBar")[1].get('href')
	except:
		print "amazonLink not found for "+url
	try:
		genre = str(soup.find_all("a","actionLinkLite bookPageGenreLink")[0].text.strip())
	except:
		print "genre not availabe for "+url
	l = []
	l.append(str(bookTitle))
	l.append(str(author))
	l.append(str(year))
	l.append(str(genre))
	l.append(str(language))
	l.append(str(grLink))
	l.append(str(amazonLink))
	l.append(str(rating))
	l.append(str(noOfPages))
	l.append(str(coverImage))
	# print l
	out.writerow(l)
	l[:] = []  # empty the list
	 
# starting driver module
if __name__ == "__main__":
	# fetchLinks()
	# fetchLinks2()
	content=""
	fileA = sys.argv[1]

	with open(fileA) as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	# print content
	fetchLinks2(content)
	
	# getBookInfo("https://www.goodreads.com/book/show/11505797-beautiful-disaster")
	# getBookInfo("https://www.goodreads.com/book/show/15842441-effortless")
	
