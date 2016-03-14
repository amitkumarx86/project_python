import urllib
import json


data = urllib.urlopen('http://python-data.dr-chuck.net/comments_247991.json').read()
js = json.loads(data)

count = 0
sum = 0
data = js["comments"]
for line in data:
    sum = sum + line["count"]
    count = count + 1
print "Count:", count
print "Sum:", sum

