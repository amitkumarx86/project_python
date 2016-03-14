import urllib
import xml.etree.ElementTree as ET

address = raw_input('Enter Url: ')
print "Retrieving:"+ address
uh = urllib.urlopen(address)
data = uh.read()
xml_data = ET.fromstring(data)
print 'Retrieved',len(xml_data),'characters'
counts = xml_data.findall('.//count')
count = 0
sum = 0
for temp in counts:
    count = count + 1
    sum = sum + int(temp.text)

print "Count:" + str(count)
print "Sum:" + str(sum)