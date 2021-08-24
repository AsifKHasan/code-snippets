import json
import urllib

address = raw_input('Enter location: ')
data = urllib.urlopen(address).read()
info = json.loads(data)
count = len(info)
sum = 0
for i in info['comments']:
	sum = sum + i['count']
	
print('Count:', str(count))
print('Sum:', str(sum))
