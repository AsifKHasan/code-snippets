s = '\u09cd' + '\xe2\x80\x8c' +'\u0985'
r = ''
text = u'আমার্‌ পরিচ্‌অয়্‌ '
text.replace(s, r)


import unicodedata

u = 'স্'
for i, c in enumerate(u):
    print(i, '%04x' % ord(c), unicodedata.category(c), end=" ")
    print(unicodedata.name(c))
