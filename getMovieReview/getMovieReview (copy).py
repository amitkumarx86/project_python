#!/usr/bin/python
import sys
import urllib2 
from bs4 import BeautifulSoup

#BeautifulSoup(html, "lxml")
def getMovieReview(searchString):
	print "............................."*5
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	url = "http://www.google.com/search?q="+searchString+"+ imdb"
	#print url
	page = opener.open(url)
	soup = BeautifulSoup(page,"html.parser")
	finalLink=""
	flag=False
	for cite in soup.findAll('cite'):
		finalLink = cite.text;
		#print finalLink
		if "imdb" in finalLink :
			finalLink="http://"+finalLink
			flag=True
			break
		
	#print "FINAL liNK ="+finalLink
    # code to get info from imdb
	if bool(flag)==True and finalLink:
		page   = urllib2.urlopen(finalLink)
		soup   = BeautifulSoup(page,"html.parser")
		rating = soup.find("div", {"class":"ratingValue"})
		plot   = soup.find("div", {"class":"summary_text"})
		year   = soup.find("span", {"id":"titleYear"})
		plot   = plot.text.strip() # cleansing plot
		newPlot= ""
		if len(plot) > 120:
			count=0
			for c in plot:
				count=count+1
				if count > 120:
					newPlot=plot[:120]+"\n           "+plot[121:]

		# basic info
		if rating:  # check whether movie is rated or not
			print "Rating   : "+rating.text.strip("\n")
			print "Year     : "+year.text.strip().replace('(','').replace(')','')
			print "Plot     : "+newPlot
			

			# info about director, writer and cast
			credit_summary_item = soup.findAll("div",  {"class":"credit_summary_item"})
			for credit_item in credit_summary_item:
				creditList=credit_item.text.strip().replace('See full cast & crew','').replace('\n','').split(':')
				#adjusting spaces between column names and values
				space=8-len(creditList[0].strip())
				spaceString=""
				for i in range(space+1):
					spaceString+=' '
				print creditList[0].strip()+spaceString+":"+' '+creditList[1].strip('\n').strip().replace('|','').replace('    ','')
		else:
			print "Movie not yet rated."
			print "Plot     : "+newPlot
	else:
		print "Movie not in database.. phoo! Please try later."


if __name__== "__main__":
	print "............................."*5
	temp = '+'.join(str(e) for e in sys.argv[1:]).replace('-','').replace('++','+')
        if " " in temp:
			print "                                                        Movie :",temp.strip(" ")
			getMovieReview(temp.replace(" ","+"))   
        else:
			print "                                                        Movie :",temp.replace('+',' ')
			getMovieReview('+'.join(str(e) for e in sys.argv[1:]).replace('-','').replace('++','+'))
	 
