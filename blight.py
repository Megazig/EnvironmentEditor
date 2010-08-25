#!/usr/bin/python

import sys, os
import shutil
from Struct import Struct
from bfog import *

full_environments = ['MainScene', 'ChikaScene', 'WaterScene', 'FireScene', 'SabakuScene', 'KaiganScene', 'DaishizenScene', 'YukiDayScene', 'SoraScene', 'IwabaScene', 'TorideScene', 'ShiroScene', 'ObakeScene', 'KurayamiChikaScene', 'ObakeOutScene', 'ShinkaiScene', 'SabakuChikaScene', 'KoriChikaScene', 'Fire2Scene', 'KoopaScene', 'Fire3Scene', 'KumoriSoraScene', 'Toride2Scene']
environments = ['MainScene', 'ChikaScene', 'FireScene', 'KaiganScene', 'DaishizenScene', 'YukiDayScene', 'SoraScene', 'IwabaScene', 'TorideScene', 'ShiroScene', 'ObakeScene', 'KurayamiChikaScene', 'ObakeOutScene', 'ShinkaiScene', 'SabakuChikaScene', 'KoriChikaScene', 'Fire2Scene', 'Fire3Scene', 'KumoriSoraScene', 'Toride2Scene']
fogs = ['ChikaScene.bfog','DaishizenScene.bfog','Fire2Scene.bfog','Fire3Scene.bfog','FireScene.bfog','IwabaScene.bfog','KaiganScene.bfog','KoopaScene.bfog','KoriChikaScene.bfog','KumoriSoraScene.bfog','KurayamiChikaScene.bfog','MainScene.bfog','ObakeOutScene.bfog','ObakeScene.bfog','SabakuChikaScene.bfog','SabakuScene.bfog','ShinkaiScene.bfog','ShiroScene.bfog','SoraScene.bfog','Toride2Scene.bfog','TorideScene.bfog','WaterScene.bfog','YukiDayScene.bfog']
lights = ['ChikaScene.blight','DaishizenScene.blight','Fire2Scene.blight','Fire3Scene.blight','FireScene.blight','IwabaScene.blight','KaiganScene.blight','KoopaScene.blight','KoriChikaScene.blight','KumoriSoraScene.blight','KurayamiChikaScene.blight','MainScene.blight','ObakeOutScene.blight','ObakeScene.blight','SabakuChikaScene.blight','SabakuScene.blight','ShinkaiScene.blight','ShiroScene.blight','SoraScene.blight','Toride2Scene.blight','TorideScene.blight','WaterScene.blight','YukiDayScene.blight']


class Blight(object):
	class LGHT(Struct):
		__endian__ = Struct.BE
		def __format__(self):
			self.Magic     = Struct.uint32
			self.Length    = Struct.uint32
			self.Flags     = Struct.uint32
			self.Unk1      = Struct.uint32
			self.LOBJ_cnt  = Struct.uint16
			self.Other_cnt = Struct.uint16
			self.Unk2      = Struct.uint32
			self.Unk3      = Struct.uint32
			self.Unk4      = Struct.uint32
			self.Unk5      = Struct.uint32
			self.Unk6      = Struct.uint32
		def __str__(self):
			out  = ""
			out += "Magic: %08x\n" % self.Magic
			out += "Length: %08x\n" % self.Length
			out += "Flags: %08x\n" % self.Flags
			out += "Unk1: %08x\n" % self.Unk1
			out += "LOBJ_Count: %04x\n" % self.LOBJ_cnt
			out += "Other_Count: %04x\n" % self.Other_cnt
			out += "Unk2: %08x\n" % self.Unk2
			out += "Unk3: %08x\n" % self.Unk3
			out += "Unk4: %08x\n" % self.Unk4
			out += "Unk5: %08x\n" % self.Unk5
			out += "Unk6: %08x\n" % self.Unk6
			return out
		def TablePrint(self):
			out  = ""
			out += "%08x " % self.Magic
			out += "%08x " % self.Length
			out += "%08x " % self.Flags
			out += "%08x " % self.Unk1
			out += "%04x " % self.LOBJ_cnt
			out += "%04x " % self.Other_cnt
			out += "%08x " % self.Unk2
			out += "%08x " % self.Unk3
			out += "%08x " % self.Unk4
			out += "%08x " % self.Unk5
			out += "%08x" % self.Unk6
			return out

	class LOBJ(Struct):
		__endian__ = Struct.BE
		def __format__(self):
			self.Magic = Struct.uint32
			self.Length = Struct.uint32
			self.Flags = Struct.uint32
			self.Unk1 = Struct.uint32
			self.Unk2 = Struct.uint32
			self.Unk3 = Struct.uint32
			self.X = Struct.float
			self.Y = Struct.float
			self.Z = Struct.float
			self.Unk4 = Struct.uint32
			self.Unk5 = Struct.uint32
			self.Unk6 = Struct.uint32
			self.Intensity = Struct.float
			self.color1 = Struct.uint32
			self.color2 = Struct.uint32
			self.dirX = Struct.float
			self.dirY = Struct.float
			self.dirZ = Struct.float
			self.Unk7 = Struct.uint32
			self.Unk8 = Struct.uint32
		def __str__(self):
			out  = ""
			out += "Magic: %08x\n" % self.Magic
			out += "Length: %08x\n" % self.Length
			out += "Flags: %08x (always 02000000)\n" % self.Flags
			out += "Unk1: %08x (always 0)\n" % self.Unk1
			out += "Unk2: %08x (00 00 type on)\n" % self.Unk2
			out += "Unk3: %08x (00 number 06 flags\n" % self.Unk3
			out += "XPos: %f\n" % self.X
			out += "YPos: %f\n" % self.Y
			out += "ZPos: %f\n" % self.Z
			out += "Unk4: %08x\n" % self.Unk4
			out += "Unk5: %08x\n" % self.Unk5
			out += "Unk6: %08x\n" % self.Unk6
			out += "Intensity: %f (always 1.0)\n" % self.Intensity
			out += "Color1: %08x\n" % self.color1
			out += "Color2: %08x\n" % self.color2
			out += "XDir: %f (always 90.0)\n" % self.dirX
			out += "YDir: %f (always 0.5)\n" % self.dirY
			out += "ZDir: %f (always 0.5)\n" % self.dirZ
			out += "Unk7: %08x (always 0)\n" % self.Unk7
			out += "Unk8: %08x\n" % self.Unk8
			return out
		def TablePrint(self):
			out  = ""
			#out += "%08x " % self.Magic
			#out += "%08x " % self.Length
			#out += "%08x " % self.Flags
			#out += "%d " % self.Unk1
			out += "%08x " % self.Unk2
			out += "%08x " % self.Unk3
			#out += "%.1f " % self.X
			#out += "%.1f " % self.Y
			#out += "%.1f " % self.Z
			out += "%08x " % self.Unk4
			out += "%08x " % self.Unk5
			out += "%08x " % self.Unk6
			#out += "%.1f " % self.Intensity
			out += "%08x " % self.color1
			out += "%08x " % self.color2
			#out += "%.1f " % self.dirX
			#out += "%.1f " % self.dirY
			#out += "%.1f " % self.dirZ
			#out += "%d " % self.Unk7
			out += "%08x" % self.Unk8
			return out

	class Other(Struct):
		__endian__ = Struct.BE
		def __format__(self):
			self.Unk1 = Struct.uint32
			self.Unk2 = Struct.uint32
		def __str__(self):
			out  = ""
			out += "Unk1: %08x\n" % self.Unk1
			out += "Unk2: %08x\n" % self.Unk2
			return out

	def __init__(self, data=None):
		self.lght = self.LGHT()
		self.lobjs = []
		self.others = []
		if data:
			offset = 0

			self.lght.unpack( data[offset:offset+len(self.lght)] )
			offset += len(self.lght)

			for x in xrange( self.lght.LOBJ_cnt ):
				lobj = self.LOBJ()
				lobj.unpack( data[offset:offset+len(lobj) ] )
				offset += len(lobj)
				self.lobjs.append(lobj)

			for x in xrange( self.lght.Other_cnt ):
				other = self.Other()
				other.unpack( data[offset:offset+len(other) ] )
				offset += len(other)
				self.others.append(other)
	def unpack(self, data):
		offset = 0

		self.lght.unpack( data[offset:offset+len(lght)] )
		offset += len(lght)

		for x in xrange( self.lght.LOBJ_cnt ):
			lobj = self.LOBJ()
			lobj.unpack( data[offset:offset+len(lobj) ] )
			offset += len(lobj)
			self.lobjs.append(lobj)

		for x in xrange( self.lght.Other_cnt ):
			other = self.Other()
			other.unpack( data[offset:offset+len(other) ] )
			offset += len(other)
			self.others.append(other)
	def pack(self):
		out  = ""
		out += self.lght.pack()
		for lobj in self.lobjs:
			out += lobj.pack()
		for other in self.others:
			out += other.pack()
		return out

	def __str__(self):
		out  = ""
		out += str(self.lght)
		for x in self.lobjs:
			out += str(x)
		for x in self.others:
			out += str(x)
		return out

	def TablePrint(self):
		out  = ""
		for x in self.lobjs:
			out += x.TablePrint()
			out += "\n"
		return out

	def GetDifferences(self):
		for x in xrange( len(self.lobjs) ):
			if self.lobjs[x].Flags != 0x02000000:
				print "Flags wrong: %08x (%d)" % (self.lobjs[x].Flags, x)
		for x in xrange( len(self.lobjs) ):
			if self.lobjs[x].Unk1 != 0:
				print "Unk1 wrong: %08x (%d)" % (self.lobjs[x].Unk1, x)
		for x in xrange( len(self.lobjs) ):
			if self.lobjs[x].Unk2 != 1:
				print "Unk2 wrong: %08x (%d)" % (self.lobjs[x].Unk2, x)
		for x in xrange( len(self.lobjs) ):
			if self.lobjs[x].Unk3 != 1:
				print "Unk3 wrong: %08x (%d)" % (self.lobjs[x].Unk3, x)
		for x in xrange( len(self.lobjs) ):
			if (self.lobjs[x].Unk3 & 0x0000ff00) != 0x0600:
				print "Unk3 byte3 wrong: %08x (%d)" % (self.lobjs[x].Unk3 & 0xff00, x)
		for x in xrange( len(self.lobjs) ):
			print "Position: %.1f %.1f %.1f (%d)" % (self.lobjs[x].X,self.lobjs[x].Y,self.lobjs[x].Z, x)
			print "Color: %08x %08x" % (self.lobjs[x].color1, self.lobjs[x].color2)

def CheckFogds():
	dir = "Env_course.arc.unpacked/fog"
	files = os.listdir(dir)
	for file in files:
		print "FILE: %s" % file
		print "-=-=-=-=-=-=-=-"
		bfog = Bfog(open(dir + "/" + file, 'rb').read())
		for x in bfog.fogds:
			assert x.Unk1 == 0
			assert x.Unk2 == 0
			assert x.Unk3 == 0
			assert x.Unk4 == 0
			assert x.Unk5 == 0
			assert x.Unk6 == 0
			if x.Float1 == 0 and x.Float2 == 0 and x.Color == 0:
				continue
			print x.TablePrint()
	dir = "Env_movie.arc.unpacked/fog"
	files = os.listdir(dir)
	for file in files:
		print "FILE: %s" % file
		print "-=-=-=-=-=-=-=-"
		bfog = Bfog(open(dir + "/" + file, 'rb').read())
		for x in bfog.fogds:
			assert x.Unk1 == 0
			assert x.Unk2 == 0
			assert x.Unk3 == 0
			assert x.Unk4 == 0
			assert x.Unk5 == 0
			assert x.Unk6 == 0
			if x.Float1 == 0 and x.Float2 == 0 and x.Color == 0:
				continue
			print x.TablePrint()
	dir = "Env_world.arc.unpacked/fog"
	files = os.listdir(dir)
	for file in files:
		print "FILE: %s" % file
		print "-=-=-=-=-=-=-=-"
		bfog = Bfog(open(dir + "/" + file, 'rb').read())
		for x in bfog.fogds:
			assert x.Unk1 == 0
			assert x.Unk2 == 0
			assert x.Unk3 == 0
			assert x.Unk4 == 0
			assert x.Unk5 == 0
			assert x.Unk6 == 0
			if x.Float1 == 0 and x.Float2 == 0 and x.Color == 0:
				continue
			print x.TablePrint()

def CheckLobjs():
	dir = "Env_course.arc.unpacked/light"
	files = os.listdir(dir)
	for file in files:
		blight = Blight(open(dir + "/" + file, 'rb').read())
		if blight.lght.Magic != 0x4c474854:
			continue
		for x in blight.lobjs:
			assert x.Unk1 == 0
			assert x.Flags == 0x02000000
			assert x.Intensity == 1.0
			assert x.dirX == 90.0
			assert x.dirY == 0.5
			assert x.dirZ == 0.5
			assert x.Unk7 == 0
			if x.Unk8 == 0:
				continue
			print x.TablePrint()
	dir = "Env_movie.arc.unpacked/light"
	files = os.listdir(dir)
	for file in files:
		blight = Blight(open(dir + "/" + file, 'rb').read())
		if blight.lght.Magic != 0x4c474854:
			continue
		for x in blight.lobjs:
			assert x.Unk1 == 0
			assert x.Flags == 0x02000000
			assert x.Intensity == 1.0
			assert x.dirX == 90.0
			assert x.dirY == 0.5
			assert x.dirZ == 0.5
			assert x.Unk7 == 0
			if x.Unk8 == 0:
				continue
			print x.TablePrint()
	dir = "Env_world.arc.unpacked/light"
	files = os.listdir(dir)
	for file in files:
		blight = Blight(open(dir + "/" + file, 'rb').read())
		if blight.lght.Magic != 0x4c474854:
			continue
		for x in blight.lobjs:
			assert x.Unk1 == 0
			assert x.Flags == 0x02000000
			assert x.Intensity == 1.0
			assert x.dirX == 90.0
			assert x.dirY == 0.5
			assert x.dirZ == 0.5
			assert x.Unk7 == 0
			if x.Unk8 == 0:
				continue
			print x.TablePrint()

def CheckLght():
	#FIXME
	dir1 = "Env_course.arc.unpacked/light"
	files = os.listdir(dir1)
	dir = "Env_movie.arc.unpacked/light"
	files += os.listdir(dir)
	dir = "Env_world.arc.unpacked/light"
	files += os.listdir(dir)
	for file in files:
		blight = Blight(open(dir1 + "/" + file, 'rb').read())
		if blight.lght.Magic != 0x4c474854:
			continue
		print blight.lght.TablePrint()
	'''
	dir = "Env_movie.arc.unpacked/light"
	files = os.listdir(dir)
	for file in files:
		blight = Blight(open(dir + "/" + file, 'rb').read())
		if blight.lght.Magic != 0x4c474854:
			continue
		print blight.lght.TablePrint()
	dir = "Env_world.arc.unpacked/light"
	files = os.listdir(dir)
	for file in files:
		blight = Blight(open(dir + "/" + file, 'rb').read())
		if blight.lght.Magic != 0x4c474854:
			continue
		print blight.lght.TablePrint()
	'''

def CreateBfogTests():
	''' Float1 Test
	i = 16500.0
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = i
		i -= 1000.0
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Float2 Test
	i = 16600.0
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float2 = i
		i += 1500.0
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Color Test
	i = 0x320232ff
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Color = i
		i += 0x00140000
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Color Alpha Test
	i = 0x323232ff
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Color = i
		i -= 0x00000010
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Flags Test 1
	flags = [0x00010000,0x02010000,0x04010000,0x05010000,0x06010000,0x07010000,0x0a010000,0x0a010000,0x0c010000,0x0c010000,0x0d010000,0x0e0100000,0x0f010000,0x01010000,0x08010000,0x09010000,0x0b010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000,0x0a010000]
	indx = 0
	i = 0x0a010000
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Flags = flags[indx]
		indx += 1
		i += 0x01000000
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Flags Test 2
	i = 0x0a000000
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Flags = i
		i += 0x00010000
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Unk3 Test - NO RESULTS
	i = 0.0
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Unk3 = i
		i += 500.0
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Unk4 Test - NO RESULTS
	i = 0.0
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Unk4 = i
		i += 500.0
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	''' Unk1 Test - NO RESULTS
	i = 0x00000000
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Unk1 = i
		i += 0x11111111
		if i > 0xffffffff:
			i = 0x00000000
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''
	#''' Unk2 Test - NO RESULTS
	i = 0x00000000
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Unk2 = i
		i += 0x11111111
		if i > 0xffffffff:
			i = 0x00000000
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	#'''
	''' Default Test
	i = 0x0a010000
	for fog in environments:
		filein = open('Env_course.arc.unpacked/fog/ChikaScene.bfog', 'rb').read()
		bfog = Bfog(filein)
		bfog.fogds[1].Float1 = 6500.0
		bfog.fogds[1].Flags = i
		file = open('Env_course.arc.editme/fog/'+fog+'.bfog', 'wb')
		file.write( bfog.pack() )
		file.close()
	'''

def CreateBlightTests():
	''' On / Off Test
	i = 0
	for light in lights:
		filein = open('Env_course.arc.unpacked/light/ChikaScene.blight', 'rb').read()
		blight = Blight(filein)
		for lobj in blight.lobjs:
			lobj.Unk2 = i
		#blight.lobjs[1] = 1
		#i -= 1000.0
		file = open('Env_course.arc.editme/light/'+light, 'wb')
		file.write( blight.pack() )
		file.close()
	'''
	''' Type Test
	i = 1
	for light in environments:
		filein = open('Env_course.arc.unpacked/light/ChikaScene.blight', 'rb').read()
		blight = Blight(filein)
		for lobj in blight.lobjs:
			lobj.Unk2 = i
		#blight.lobjs[1] = 1
		i += 0x0100
		file = open('Env_course.arc.editme/light/'+light+'.blight', 'wb')
		file.write( blight.pack() )
		file.close()
	'''
	''' Intensity Test
	i = -1.0
	for light in environments:
		filein = open('Env_course.arc.unpacked/light/ChikaScene.blight', 'rb').read()
		blight = Blight(filein)
		for lobj in blight.lobjs:
			lobj.Intensity = i
		#blight.lobjs[1] = 1
		i += 0.5
		file = open('Env_course.arc.editme/light/'+light+'.blight', 'wb')
		file.write( blight.pack() )
		file.close()
	'''
	''' Xdir Test
	i = 20.0
	for light in environments:
		filein = open('Env_course.arc.unpacked/light/ChikaScene.blight', 'rb').read()
		blight = Blight(filein)
		for lobj in blight.lobjs:
			lobj.dirX = i
		#blight.lobjs[1] = 1
		i += 10.0
		file = open('Env_course.arc.editme/light/'+light+'.blight', 'wb')
		file.write( blight.pack() )
		file.close()
	'''
	''' Ydir Test
	i = -2.0
	for light in environments:
		filein = open('Env_course.arc.unpacked/light/ChikaScene.blight', 'rb').read()
		blight = Blight(filein)
		for lobj in blight.lobjs:
			lobj.dirY = i
		#blight.lobjs[1] = 1
		i += 0.5
		file = open('Env_course.arc.editme/light/'+light+'.blight', 'wb')
		file.write( blight.pack() )
		file.close()
	'''

def SetupEditmeFolder():
	curr = os.getcwd()
	unpacked = curr + "/Env_course.arc.unpacked"
	editme = curr + "/Env_course.arc.editme"
	chika = "ChikaScene"
	for x in full_environments:
		shutil.copy( unpacked + "/fog/" + chika + ".bfog", editme + "/fog/" + x + ".bfog")
		shutil.copy( unpacked + "/light/" + chika + ".blight", editme + "/light/" + x + ".blight")
		shutil.copy( unpacked + "/light/" + chika + ".blmap", editme + "/light/" + x + ".blmap")

def main():
	#curr = os.getcwd()
	if len(sys.argv) > 1:
		if sys.argv[1] == "--setup":
			SetupEditmeFolder()
		elif sys.argv[1] == "--create-bfogs":
			CreateBfogTests()
		elif sys.argv[1] == "--create-blights":
			CreateBlightTests()
		else:
			file = open(sys.argv[1], 'rb').read()
			if sys.argv[1][-7:] == ".blight":
				blight = Blight(file)
				print blight.TablePrint()
				#blight.GetDifferences()
			else:
				bfog = Bfog(file)
				print bfog.TablePrint()
				print bfog
	else:
		#CheckLght()
		#CheckLobjs()
		CheckFogds()

if __name__ == "__main__":
	main()

