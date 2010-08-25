
def nullterm(str_plus):
	z = str_plus.find('\0')
	if z != -1:
		return str_plus[:z]
	else:
		return str_plus
				
def hexdump(s,sep=" "):
	return sep.join(map(lambda x: "%02x"%ord(x),s))

def ascii(s):
	s2 = ""
	for c in s:
		if ord(c)<0x20 or ord(c)>0x7e:
			s2 += "."
		else:
			s2 += c
	return s2

def xxd(s):
	length = len(s)
	#print length
	offset = 0
	out = ""
	lines = length / 0x10
	if length % 0x10:
		lines += 1
	#print lines
	for x in xrange(lines):
		line = s[x*0x10:(x+1)*0x10]
		#print line
		out += hexdump(line)
		out += " "
		out += ascii(line)
		out += "\n"
	return out

