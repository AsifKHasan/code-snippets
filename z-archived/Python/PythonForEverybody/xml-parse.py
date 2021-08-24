import urllib
import xml.etree.ElementTree as ET

address = raw_input('Enter location: ')
if len(address) < 1 :
    address = 'http://python-data.dr-chuck.net/comments_255656.xml'

uh = urllib.urlopen(address)
data = uh.read()
tree = ET.fromstring(data)
result = tree.findall('.//count')
count = len(result)
sum = 0
for n in result:
    c = int(n.text)
    sum = sum + c
    
print 'Count:',count
print 'Sum:',sum