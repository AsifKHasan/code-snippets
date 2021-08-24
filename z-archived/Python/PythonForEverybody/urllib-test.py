#import urllib
#from bs4 import BeautifulSoup

#url = 'http://python-data.dr-chuck.net/comments_255659.html'
#html = urllib.urlopen(url).read()
#soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the span tags
#tags = soup('span')
#sum = 0
#for tag in tags:
    # Look at the parts of a tag
    # sum = sum + int(tag.contents[0])
    # print 'TAG:',tag
    # print 'URL:',tag.get('href', None)
    # print 'Contents:',tag.contents[0]
    # print 'Attrs:',tag.attrs

# print sum





import urllib
from bs4 import BeautifulSoup

count = int(raw_input('Enter Count - '))
position = int(raw_input('Enter Position - '))

url = 'http://python-data.dr-chuck.net/known_by_Kady.html'
for c in range(count):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all of the anchor tags
    tags = soup('a')
    url = tags[position-1].get('href', None)
    print url