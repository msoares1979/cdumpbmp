#!/usr/bin/python

import cdumpbmp
import unittest
import os

_tmpfilename = 'tmpfile.bmp'

class TestDumpBMP(unittest.TestCase):
	def setUp(self):
		self.file = open(_tmpfilename, "w")
		self.file.truncate(0)

	def tearDown(self):
		os.unlink(_tmpfilename)

	def test_null_file(self):
		self.failUnlessRaises(cdumpbmp.CDumpBmpInputError, cdumpbmp.read_input, self.file)

	def test_zerolen_bmp(self):
		zerolenpat = 'BM'\
				'\x00\x00\x00\x00\x00\x00\x00\x00\x3e\x00\x00\x00\x28\x00\x00\x00\x00\x00'\
				'\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x74\x01\x00'\
				'\x00\xb8\x0b\x00\x00\xb8\x0b\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00'\
				'\x00\x00\x00\x00\xff\xff\xff\x00'
		expected = 'char bmpdata[0] = {\n}\n'
		self.file.write(zerolenpat)
		cdumpbmp.read_input(self.file)
		self.assertEquals(cdumpbmp.format() == "Windows 3.x")
		self.assertEquals(cdumpbmp.get_height() == 0)
		self.assertEquals(cdumpbmp.get_width() == 0)
		self.assertEquals(cdumpbmp.get_depth() == 1)
		self.assertEquals(cdumpbmp.output() == expected)

if __name__ == '__main__':
	unittest.main()
