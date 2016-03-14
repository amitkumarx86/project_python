import urllib
from bs4 import BeautifulSoup

def get_18th_a(links):
  count = 0
  for link in links:
  	count = count + 1
  	if count == 18 : 
  		return link
   

html = urllib.urlopen('http://python-data.dr-chuck.net/known_by_Isobel.html').read()
soup = BeautifulSoup(html)
links = soup('a')
i = 1
a = get_18th_a(links)
print a.text
while i <= 6:
  i = i + 1
  html = urllib.urlopen(a.get('href',None)).read()
  soup = BeautifulSoup(html)
  links = soup('a')
  a = get_18th_a(links)
  print a.text	
