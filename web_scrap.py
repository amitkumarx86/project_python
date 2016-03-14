import urllib
from bs4 import BeautifulSoup


html = urllib.urlopen('http://python-data.dr-chuck.net/comments_247990.html').read()
soup = BeautifulSoup(html)
spans = soup('span')
count = 0
sum = 0
for span in spans:
    count = count + 1
    sum = sum + float(span.text)

print "Count " + str(count)
print "Sum " + str(sum)

