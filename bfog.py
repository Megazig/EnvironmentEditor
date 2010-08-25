from Struct import Struct

class Bfog(object):
	class FOGM(Struct):
		__endian__ = Struct.BE
		def __format__(self):
			self.Magic = Struct.uint32
			self.Length = Struct.uint32
			self.Unk1 = Struct.uint32
			self.Unk2 = Struct.uint32
			self.FOGD_cnt = Struct.uint16
			self.Unk3 = Struct.uint16
		def __str__(self):
			out  = ""
			out += "Magic: %08x\n" % self.Magic
			out += "Length: %08x\n" % self.Length
			out += "Unk1: %08x\n" % self.Unk1
			out += "Unk2: %08x\n" % self.Unk2
			out += "FOGD_Count: %04x\n" % self.FOGD_cnt
			out += "Unk3: %04x\n" % self.Unk3
			return out

	class FOGD(Struct):
		__endian__ = Struct.BE
		def __format__(self):
			self.Magic = Struct.uint32
			self.Length = Struct.uint32
			self.Unk1 = Struct.uint32
			self.Unk2 = Struct.uint32
			self.Float1 = Struct.float
			self.Float2 = Struct.float
			self.Float3 = Struct.float
			self.Float4 = Struct.float
			self.Color = Struct.uint32
			self.Flags = Struct.uint32
			self.Unk5 = Struct.uint32
			self.Unk6 = Struct.uint32
		def __str__(self):
			out  = ""
			out += "Magic: %08x\n" % self.Magic
			out += "Length: %08x\n" % self.Length
			out += "Unk1: %08x (always 0)\n" % self.Unk1
			out += "Unk2: %08x (always 0)\n" % self.Unk2
			out += "Float1: %f (startz)\n" % self.Float1
			out += "Float2: %f (endz)\n" % self.Float2
			out += "Float3: %f (nearz)(always 0)\n" % self.Unk3
			out += "Float4: %f (farz) (always 0)\n" % self.Unk4
			out += "Color: %08x\n" % self.Color
			out += "Flags: %08x (type-0xa, unk-0x1, unk-0x0, unk-0x0)\n" % self.Flags
			out += "Unk5: %08x (always 0)\n" % self.Unk5
			out += "Unk6: %08x (always 0)\n" % self.Unk6
			return out
		def TablePrint(self):
			out  = ""
			#out += "Magic: %08x\n" % self.Magic
			#out += "Length: %08x\n" % self.Length
			#out += "%08x " % self.Unk1
			#out += "%08x " % self.Unk2
			out += "%.1f " % self.Float1
			out += "%.1f " % self.Float2
			#out += "%.1f " % self.Unk3
			#out += "%.1f " % self.Unk4
			out += "%08x " % self.Color
			out += "%08x " % self.Flags
			#out += "%08x " % self.Unk5
			#out += "%08x" % self.Unk6
			return out

	def __init__(self, data=None):
		self.fogm = self.FOGM()
		self.fogds = []
		self.others = []
		if data:
			offset = 0

			self.fogm.unpack( data[offset:offset+len(self.fogm)] )
			offset += len(self.fogm)

			for x in xrange( self.fogm.FOGD_cnt ):
				fogd = self.FOGD()
				fogd.unpack( data[offset:offset+len(fogd) ] )
				offset += len(fogd)
				self.fogds.append(fogd)

			'''
			for x in xrange( self.lght.Other_cnt ):
				other = self.Other()
				other.unpack( data[offset:offset+len(other) ] )
				offset += len(other)
				self.others.append(other)
			'''
	def unpack(self, data=None):
		offset = 0

		self.fogm.unpack( data[offset:offset+len(self.fogm)] )
		offset += len(self.fogm)

		for x in xrange( self.fogm.FOGD_cnt ):
			fogd = self.FOGD()
			fogd.unpack( data[offset:offset+len(fogd) ] )
			offset += len(fogd)
			self.fogds.append(fogd)

		'''
		for x in xrange( self.lght.Other_cnt ):
			other = self.Other()
			other.unpack( data[offset:offset+len(other) ] )
			offset += len(other)
			self.others.append(other)
		'''
	def pack(self):
		out  = ""
		out += self.fogm.pack()
		for fogd in self.fogds:
			out += fogd.pack()
		return out
	def __str__(self):
		out  = ""
		out += str(self.fogm)
		for fogd in self.fogds:
			out += str(fogd)
		return out
	def TablePrint(self):
		out  = ""
		for fogd in self.fogds:
			out += fogd.TablePrint()
			out += "\n"
		return out


