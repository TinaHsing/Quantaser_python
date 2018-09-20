f1 = open("test.text","w")
for i in xrange(109, 119):
	f1.write(chr(i))
f1.close()
f1 = open("test.text","r")
s = '1'
while s != '':
	s = f1.read(1)
	a = ord(s)
	print a
f1.close()
