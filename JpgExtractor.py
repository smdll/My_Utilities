import sys, os

def extract(path):
	name = 1
	infile = open(path, 'rb')
	if not os.path.exists('%s_extracted'%path):
		os.mkdir('%s_extracted'%path)
	while 1:
		c = infile.read(1)
		if not c:
			break
		#Head
		if hex(ord(c)) == '0xff':
			c = infile.read(1)
			if hex(ord(c)) == '0xd8':
				c = infile.read(1)
				#APP0/APP1
				if hex(ord(c)) == '0xff':
					c = infile.read(1)
					if hex(ord(c)) in ['0xe0', '0xe1']:
						content = []
						content.append(chr(0xff))
						content.append(chr(0xd8))
						content.append(chr(0xff))
						content.append(c)
						while 1:
							c = infile.read(1)
							if not c:
								break
							#Tail
							if hex(ord(c)) == '0xff':
								content.append(c)
								c = infile.read(1)
								if hex(ord(c)) == '0xd9':
									content.append(c)
									break
								else:
									content.append(c)
							else:
								content.append(c)
						outfile = open('%s_extracted\\%d.jpg'%(path, name), 'wb')
						for i in content:
							outfile.write(i)
						print '%d.jpg saved'%name
						outfile.close()
						name += 1

if __name__ == '__main__':
	if len(sys.argv) != 2:
		exit()
	extract(sys.argv[1])