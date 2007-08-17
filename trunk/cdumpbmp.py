#!/usr/bin/python

# Converts BMP files to C hexadecimal arrays

# B0-1: 'BM' prefix
# B5-2: bitmap size
# B9-6: zero
# B13-10: bitmap start offset
# B17-14: 0x00000028 ???
# B21-18: height
# B25-22: width

# Hexdump output
# 00000000  42 4d b2 01 00 00 00 00  00 00 3e 00 00 00 28 00 |BM........>...(.|
# 00000010  00 00 4c 00 00 00 1f 00  00 00 01 00 01 00 00 00 |..L.............|
# 00000020  00 00 74 01 00 00 b8 0b  00 00 b8 0b 00 00 02 00 |..t.............|
# 00000030  00 00 02 00 00 00 00 00  00 00 ff ff ff 00 ff ff |................|

import sys

class lineout:
	def __init__(self, maxcols=16):
		self.maxcols = maxcols
		self.curcols = 0

	def dumpheader(self, name, size, w, h):
		print "/* width=%d height=%d */\n" % (w, h)
		print "char bmp", name, "[", size, "] = {\n\t"

	def dumpfooter():
		print "};\n"

	def dumpbyte(self, b):
		"""Dumps each hexadecimal byte on output"""
		if self.curcols != 0:
			print ", "

		if self.curcols == self.maxcols:
			print "\n\t"
			self.curcols = 0

		print "0x%02X" % int(b)

def main(filename):
	f = open(filename, 'r')
	header = f.read(2)
	if header <> 'BM':
		print "This doesn't seem a BMP file"
		sys.exit(0)
	size = f.read(4)
	f.read(4)
	offset = f.read(4)
	f.read(4)
	height = f.read(4)
	width = f.read(4)
	print filename, offset, size, width, height

	dumper = lineout()
	dumper.dumpheader(filename, size, width, height)

	# start bitmap area
	f.seek(offset, 0)
	b = f.read(1)
	while b <> '':
		dumper.dumpbyte(b)
		b = f.read(1)
	dumper.dumpfooter()

if __name__ == '__main__':
	main(sys.argv[1])
