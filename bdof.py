#!/usr/bin/python

import sys, os
from Struct import Struct

class Bdof(Struct):
	__endian__ = Struct.BE
	def __format__(self):
		self.Magic = Struct.string(4)
		self.Length = Struct.uint32
		self.Unk1 = Struct.uint32
		self.Unk2 = Struct.uint32
		self.Unk3 = Struct.uint16
		self.Unk4 = Struct.uint16
		self.Unk5 = Struct.uint16
		self.Unk6 = Struct.uint16
		self.Float1 = Struct.float
		self.Float2 = Struct.float
		self.Float3 = Struct.float
		self.Float4 = Struct.float
		self.Float5 = Struct.float
		self.Float6 = Struct.float
		self.Float7 = Struct.float
		self.Float8 = Struct.float
		self.Float9 = Struct.float
		self.FloatA = Struct.float
		self.Unk7 = Struct.uint32
		self.Unk8 = Struct.uint32
		self.Unk9 = Struct.uint32
		self.UnkA = Struct.uint32
	def __str__(self):
		out  = ""
		out += "Magic: %s\n" % self.Magic
		out += "Length: %08x\n" % self.Length
		out += "Unk1: %08x\n" % self.Unk1
		out += "Unk2: %08x\n" % self.Unk2
		out += "Unk3: %04x\n" % self.Unk3
		out += "Unk4: %04x\n" % self.Unk4
		out += "Unk5: %04x\n" % self.Unk5
		out += "Unk6: %04x\n" % self.Unk6
		out += "Float1: %f\n" % self.Float1
		out += "Float2: %f\n" % self.Float2
		out += "Float3: %f\n" % self.Float3
		out += "Float4: %f\n" % self.Float4
		out += "Float5: %f\n" % self.Float5
		out += "Float6: %f\n" % self.Float6
		out += "Float7: %f\n" % self.Float7
		out += "Float8: %f\n" % self.Float8
		out += "Float9: %f\n" % self.Float9
		out += "FloatA: %f\n" % self.FloatA
		out += "Unk7: %08x\n" % self.Unk7
		out += "Unk8: %08x\n" % self.Unk8
		out += "Unk9: %08x\n" % self.Unk9
		out += "UnkA: %08x\n" % self.UnkA
		return out

def main():
	data = ""
	with open(sys.argv[1], 'rb') as fp:
		data = fp.read()

	dof = Bdof()
	dof.unpack( data[:len(dof)] )
	print dof

if __name__ == "__main__":
	main()
