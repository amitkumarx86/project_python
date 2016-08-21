import gzip
import re
from StringIO import StringIO
import urllib2
from bs4 import BeautifulSoup
import webbrowser
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium import webdriver
import subprocess
    

#download torrent    
def download_video(ilink):
    print "Video getting downloaded..."
    bashCommnad = 'youtube-dl -f best '+ilink
    output = subprocess.check_output(['bash','-c', bashCommnad])
    print output

# ------------------------------------------------------------------------------
# start of the code
#-------------------------------------------------------------------------------
search_keyword_1=raw_input("Enter search keyword:")
search_keyword = search_keyword_1.replace(" ", "+")
link = "https://www.youtube.com/results?search_query=" + search_keyword
#open the link
page = urllib2.urlopen(link)
soup = BeautifulSoup(page)
#print soup.find_all("a")
video_div = soup.find_all('div', class_="yt-lockup-content")

video_data=dict()
for div in video_div:
  view_div = div.find_all('ul',class_="yt-lockup-meta-info")
  temp = '' + str(view_div[0])
  view = ''.join(re.findall('</li><li>([0-9].*)views',temp)).strip()
  if view == '' : continue 
  video_link = "https://www.youtube.com" + div.find('a').get("href")
  video_data[video_link] = float(view.replace(',',''))


temp = sorted([(v,k) for k,v in video_data.items()])  

print "Found " + str(len(temp)) +" videos,"
print "How many you want to download:"
number = float(raw_input())
count = 0
for ilink in video_data:
  count = count +1
  if count > number : break
  print "Serial Number :" + str(count)
  download_video(ilink)
