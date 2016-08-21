import urllib2
from bs4 import BeautifulSoup
import sys


def __getLyrics(search_keyword):        
	link = "http://search.azlyrics.com/search.php?q=" + search_keyword
    #open the link
	print "waiting for result.."
	print link
	page = urllib2.urlopen(link)
	soup = BeautifulSoup(page,'lxml')
	finalLink = ""
	for line in soup.find_all('a'):
		if ( "/lyrics/" in line.get('href')):
			if ( line.get('href').split('/')[-1].split(".html")[0]  in search_keyword.replace('+','').lower().replace(" ","")) :
				finalLink = line.get('href')
				break;
                
	if finalLink != "" :
		page = urllib2.urlopen(finalLink)
		soup = BeautifulSoup(page,'lxml')
		for divHolder in soup.find_all('div',class_="col-xs-12 col-lg-8 text-center"):
			for divChild in divHolder.contents:
				if(len(divChild) > 75):
					for d in divChild.contents:
						if ("Usage of azlyrics.com content" in d or " " not in d):
							continue
						else:
							if (len(d.strip()) != 0):
								print str(d).replace('\n','')
	if finalLink == "":
		print "Lyrics not found."       
    #print "done"

    
status=""
try :
    url = "https://www.google.com"
    urllib2.urlopen(url)
    status = "Connected"
except :
    status = "Not connect"



if (status == "Connected"):
    __getLyrics('+'.join(str(e) for e in sys.argv[1:]).replace('-','').replace('++','+'))
else:
    print status

