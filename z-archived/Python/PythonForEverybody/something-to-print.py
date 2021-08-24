import re

# print("Here comes the print")

x = 'asif.hasan@gmail.com'
y = re.findall('\S+@\S+?', x)
print (y)