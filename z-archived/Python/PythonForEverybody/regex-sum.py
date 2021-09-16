import re

#name = raw_input("Enter file:")
#if len(name) < 1 : name = "regex_sum_255654.txt"
#handle = open(name)
handle = open("regex_sum_255654.txt")
text = handle.read()

numbers = re.findall('[0-9]+', text)
sum = 0
for num in numbers:
    sum = sum + int(num)
    
print sum
