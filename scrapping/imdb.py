import requests
from bs4 import BeautifulSoup, SoupStrainer
import csv


out = csv.writer(open("movies.csv","w"),lineterminator='\n')
header=['Movie Name','link','year']
out.writerow(header)

years = []
response = requests.get('http://www.imdb.com/year/').content
links = BeautifulSoup(response, "html.parser",parseOnlyThese=SoupStrainer('a', href=True)).find_all("a", href=True)
for link in links:
    if 'release_date' in link['href']:
    	link1 = "http://www.imdb.com"+link['href']
    	if link1[-4:] > "1903": 
    		years.append("http://www.imdb.com"+link['href'])


for year_link in years:
	movie_get_url = year_link
	year = movie_get_url[-4:]
	response1 = requests.get(movie_get_url).content
	m_count=0
	flag = True
	while(flag):
		try:
			links = BeautifulSoup(response1,"html.parser", parseOnlyThese=SoupStrainer('a', href=True)).find_all("a", href=True)
			for link in links:
			    if (link is not None  and '/title/' in link['href'] ):
			    	movie_name = link.string
			    	if(movie_name != 'X' and movie_name is not None):
			    		movie_url = "http://www.imdb.com"+link['href']
			    		# print movie_name,movie_url
			    		l = []
			    		l.append(movie_name.encode('utf-8'))
			    		l.append(movie_url)
			    		l.append(year)
			    		# print l
			    		out.writerow(l)
			    		l[:] = []  # empty the list
			    		m_count = m_count+1

			soup = BeautifulSoup(response1)
			next = soup.find_all('a', {'class': ['lister-page-next next-page']})
			if next : 
				movie_get_url = "http://www.imdb.com/search/title"+next[0]['href']
				# print movie_get_url
				response1 = requests.get(movie_get_url).content		
			else: 
				flag=False
			print year+" got "+str(m_count)
		except:
			print "error happened"
	
		
# print movies
