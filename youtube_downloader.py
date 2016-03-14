import gzip
import re
from StringIO import StringIO
import urllib2
from bs4 import BeautifulSoup
import webbrowser
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium import webdriver
import os
import subprocess
    
#-----------------------------------------------------------------------------
#download video
def download_video(ilink,directory):
    print "Video getting downloaded..."
    bashCommnad = "youtube-dl -f best -o '"+ directory +"/%(title)s' "+ilink 
    print bashCommnad
    output = subprocess.check_output(['bash','-c', bashCommnad])
    print output
    
    
#-----------------------------------------------------------------------------    
#get video links
def get_links(link):
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
  return video_data

# -------------------------------------------------------------------------------
# start of the MAIN
#-------------------------------------------------------------------------------
search_keyword_1=raw_input("Enter search keyword:")
search_keyword = search_keyword_1.replace(" ", "+")
link = "https://www.youtube.com/results?search_query=" + search_keyword


# declaring dic for video links
video_data=dict()
video_data = get_links(link) # calling first time get link func

#sort based on number of reviews
temp = sorted([(v,k) for k,v in video_data.items()])  # this is optional

print "Found " + str(len(temp)) +" videos in first step,"
print "Do you want more videos:y/n"
response = raw_input()
if response == "Y" or response == "y" :
  #Add more videos if available
  print "Getting more videos..."
  video_list=list()
  page = urllib2.urlopen(link)
  soup = BeautifulSoup(page)
  more_video_div = soup.find_all('a', class_="yt-uix-button  yt-uix-pager-button yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default")
  for link in more_video_div:
    video_link = "https://www.youtube.com" + link.get("href")
    video_list.append(video_link)
  
  # calling function to get the video links
  
  for link in video_list:
    temp_video_data=dict()
    temp_video_data = get_links(link) # calling first time get link func
    for k,v in temp_video_data.items():
      video_data[k] = v
    
# download procedure inputs
print "Found " + str(len(video_data.keys())) +" videos,"
print "How many you want to download:"
number = float(raw_input())
print "Do you want to download sorted by number of views:y/n"
response = raw_input()
if response == "Y" or response == "y":
  temp = sorted([(v,k) for k,v in video_data.items()])  # this is optional
count = 0

# videos downloaded without sorting
directory="~/Downloads/"+search_keyword_1.upper().replace(" ","_")
print directory
if not os.path.exists(directory):
    os.makedirs(directory)


for ilink in video_data:
  count = count +1
  if count > number : break
  print "Serial Number :" + str(count)
  download_video(ilink,directory)