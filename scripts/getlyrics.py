#!/usr/bin/env python
import sys
import urllib2 
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup

def __getLyrics(searchString):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = "http://www.google.com/search?q="+searchString+"+lyrics"
    #print url
    page = opener.open(url)
    soup = BeautifulSoup(page)
    finalLink=""
    for cite in soup.findAll('cite'):
        finalLink = cite.text;
        #print finalLink
        if "songlyricsmint" in finalLink or "/.../" in finalLink: 
            continue
        if "azlyrics" in finalLink or "lyricsmint" in finalLink or "hindilyrics" in finalLink:
            break
    finalLink="http://"+finalLink
    #print finalLink
    if str(finalLink) != "" and "azlyrics" in str(finalLink):
        #print finalLink
        page = urllib2.urlopen(finalLink)
        soup = BeautifulSoup(page)
        count = 0
        count2 = 1
        for divHolder in soup.findAll('div'):
            for divChild in divHolder.contents:
                if "Usage of azlyrics.com content" in divChild:
                    count=1
                    continue    
                if "Submit Corrections" in str(divChild) and count == 1:
                    count2 = 0
                if count == 1 and count2 == 1 and str(divChild) not in "<br />":
                    print str(divChild).replace('\n','')
                    
    elif "lyricsmint" in str(finalLink):
        #print finalLink           
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        page = opener.open(finalLink)
        soup = BeautifulSoup(page)
        count=0
        for divHolder in soup.findAll('div', { "id" : "lyric" }):
            print str(divHolder).replace("<br />","\n").replace("<p>","\n").replace("</p>","\n").replace("<div id=\"lyric\"><h2>","").replace("</h2>","\n").replace("</div>","")
    elif "hindilyrics" in str(finalLink):
        #print finalLink
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        page = opener.open(finalLink)
        soup = BeautifulSoup(page)
        for divHolder in soup.find('pre'):
            print ''.join(str(e) for e in str(divHolder.contents)).replace("[u","").replace("(","").replace(")","").replace("'\\n\\n","").replace("\\r","\n").replace("\\n']","")
    else:
        print "Lyrics not found"



if __name__ == "__main__":
    
    status="Connected"
    if (status == "Connected"):
        temp = '+'.join(str(e) for e in sys.argv[1:]).replace('-','').replace('++','+')
        if " " in temp:
            __getLyrics(temp.replace(" ","+"))   
        else:
            __getLyrics('+'.join(str(e) for e in sys.argv[1:]).replace('-','').replace('++','+'))
    else:
        print status