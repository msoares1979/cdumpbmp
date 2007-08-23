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

import os
import sys
import struct

class CDumpBmpInputError(Exception):
	def __init__(self):
		Exception.__init__()

class lineout:
	def __init__(self, maxcols=16):
		self.maxcols = maxcols
		self.curcols = 0

	def dumpheader(self, name, size, w, h):
		print "/* width=%d" % w, "height=%d */" % h
		print "char bmp%s[%d] = {\n" % (name, size), 

	def dumpfooter(self):
		if self.curcols <> 0:
			print "\n",
		print "};"

	def dumpbyte(self, b):
		"""Dumps each hexadecimal byte on output"""
		if self.curcols == self.maxcols:
			print "\n", 
			self.curcols = 0

		if self.curcols == 0:
			print "\t",
		else:
			print ", ",

		print "0x%02X" % b, 
		self.curcols += 1

def main(filename):
	f = open(filename, 'r')
	header = f.read(2)
	if header <> 'BM':
		print "This doesn't seem a BMP file"
		sys.exit(0)
	b = f.read(4)
	size = struct.unpack("<i", b)[0]
	f.read(4)
	b = f.read(4)
	offset = struct.unpack("<i", b)[0]
	f.read(4)
	b = f.read(4)
	height = struct.unpack("<i", b)[0]
	b = f.read(4)
	width = struct.unpack("<i", b)[0]
	#print filename, offset, size, width, height

	dumper = lineout()
	name = os.path.basename(filename)
	name = name.rsplit(".", 2)[0]
	dumper.dumpheader(name, size, width, height)

	# start bitmap area
	f.seek(offset, 0)
	b = f.read(1)
	while b <> '':
		dumper.dumpbyte(b)
		b = f.read(1)
	dumper.dumpfooter()

def help():
	print "cdumpbmp 1.0 ( http://code.google.com/p/cdumpbmp )"
	print "Usage: cdumpbpm [filename]\n"
	print "EXAMPLE:"
	print "  cdumpbmp foobar.bmp\n"

if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except IndexError:
		help()
