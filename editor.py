#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from sys import argv
from Struct import *

import arc
import common
import blight
import bfog
import bdof

class SceneTab(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.layout = QVBoxLayout()
		self.text = QLabel('Scene Tab not implemented')
		self.layout.addWidget(self.text)

		self.setLayout(self.layout)


class LightTab(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.currentLight = None

		self.layout = QVBoxLayout()

		#"""
		self.fileList = []
		self.dropDown = QComboBox()
		self.dropDown.currentIndexChanged.connect(self.fileC)
		self.layout.addWidget(self.dropDown)
		#"""

		#"""
		self.lightDrop = QComboBox()
		self.lightDrop.currentIndexChanged.connect(self.lightC)
		self.layout.addWidget(self.lightDrop)
		#"""

		#"""
		self.fieldsLayout = QGridLayout()

		fields = (('Flags','0x02000000'),('Unk1','0x00000000'),
			('Unk2','0x00000000'), ('Unk3','0x00000000'),
			('XPos','0.0'), ('YPos','0.0'),
			('ZPos','0.0'), ('Unk4','0x00000000'),
			('Unk5','0x00000000'), ('Unk6','0x00000000'),
			('Intensity','1.0'), ('Color1','0x00000000'),
			('Color2','0x00000000'), ('XDir','90.0'),
			('YDir','0.5'), ('ZDir','0.5'),
			('Unk7','0x00000000'), ('Unk8','0x00000000'))

		self.field = [0 for x in xrange(len(fields))]
		self.fieldL = [0 for x in xrange(len(fields))]
		self.fieldV = [0 for x in xrange(len(fields))]

		for i in xrange(len(fields)):
			self.field[i] = QHBoxLayout()
			self.fieldL[i] = QLabel(fields[i][0])
			self.fieldV[i] = QLineEdit(fields[i][1])
			self.fieldV[i].editingFinished.connect(self.Update)
			self.field[i].addWidget(self.fieldL[i])
			self.field[i].addWidget(self.fieldV[i])
			self.fieldsLayout.addLayout(self.field[i],i,0)

		self.layout.addLayout(self.fieldsLayout)
		#"""

		self.setLayout(self.layout)

	def populate(self, list, buffer):
		self.fileList = []
		for x in xrange(len(list) / 2):
			self.fileList.append(list[x*2])
		self.dropDown.clear()
		l = []
		for x in list:
			if x[0][-6:] == 'blight':
				l.append(x[0])
		self.dropDown.addItems(l)
		self.fileC(0)

	def fileC(self, index):
		if self.currentLight:
			self.Save()
		self.oldDropDownIndex = index
		offs = self.fileList[index][1]
		buffer = main_window.fileBuffer
		self.currentLight = blight.Blight(buffer[offs:])
		#print "%08x" % self.currentLight.lght.Magic
		#assert self.currentLight.lght.Magic == 0x4c474854
		self.setLightDropCombo(index)

	def setLightDropCombo(self, index):
		count = 0
		self.lightDrop.clear()
		l = []
		for light in self.currentLight.lobjs:
			l.append(str(count))
			count += 1
		self.lightDrop.addItems(l)
		self.setFields(0)

	def setFields(self, index):
		lobj = self.currentLight.lobjs[index]
		#print "%08x" % lobj.Magic
		#assert lobj.Magic == 0x4c4f424a
		self.fieldV[0].setText("0x%08x" % lobj.Flags)
		self.fieldV[1].setText("0x%08x" % lobj.Unk1)
		self.fieldV[2].setText("0x%08x" % lobj.Unk2)
		self.fieldV[3].setText("0x%08x" % lobj.Unk3)
		self.fieldV[4].setText(str(lobj.X))
		self.fieldV[5].setText(str(lobj.Y))
		self.fieldV[6].setText(str(lobj.Z))
		self.fieldV[7].setText("0x%08x" % lobj.Unk4)
		self.fieldV[8].setText("0x%08x" % lobj.Unk5)
		self.fieldV[9].setText("0x%08x" % lobj.Unk6)
		self.fieldV[10].setText("0x%08x" % lobj.Intensity)
		self.fieldV[11].setText("0x%08x" % lobj.color1)
		self.fieldV[12].setText("0x%08x" % lobj.color2)
		self.fieldV[13].setText(str(lobj.dirX))
		self.fieldV[14].setText(str(lobj.dirY))
		self.fieldV[15].setText(str(lobj.dirZ))
		self.fieldV[16].setText("0x%08x" % lobj.Unk7)
		self.fieldV[17].setText("0x%08x" % lobj.Unk8)

	def lightC(self, index):
		self.setFields(index)

	def Update(self):
		if not self.currentLight:
			return
		i = self.lightDrop.currentIndex()
		self.currentLight.lobjs[i].Flags = \
			int(str(self.fieldV[0].text())[2:], 16)
		self.currentLight.lobjs[i].Unk1 = \
			int(str(self.fieldV[1].text())[2:], 16)
		self.currentLight.lobjs[i].Unk2 = \
			int(str(self.fieldV[2].text())[2:], 16)
		self.currentLight.lobjs[i].Unk3 = \
			int(str(self.fieldV[3].text())[2:], 16)
		self.currentLight.lobjs[i].X = \
			float(str(self.fieldV[4].text()))
		self.currentLight.lobjs[i].Y = \
			float(str(self.fieldV[5].text()))
		self.currentLight.lobjs[i].Z = \
			float(str(self.fieldV[6].text()))
		self.currentLight.lobjs[i].Unk4 = \
			int(str(self.fieldV[7].text())[2:], 16)
		self.currentLight.lobjs[i].Unk5 = \
			int(str(self.fieldV[8].text())[2:], 16)
		self.currentLight.lobjs[i].Unk6 = \
			int(str(self.fieldV[9].text())[2:], 16)
		self.currentLight.lobjs[i].Intensity = \
			int(str(self.fieldV[10].text())[2:], 16)
		self.currentLight.lobjs[i].color1 = \
			int(str(self.fieldV[11].text())[2:], 16)
		self.currentLight.lobjs[i].color2 = \
			int(str(self.fieldV[12].text())[2:], 16)
		self.currentLight.lobjs[i].dirX = \
			float(str(self.fieldV[13].text()))
		self.currentLight.lobjs[i].dirY = \
			float(str(self.fieldV[14].text()))
		self.currentLight.lobjs[i].dirZ = \
			float(str(self.fieldV[15].text()))
		self.currentLight.lobjs[i].Unk7 = \
			int(str(self.fieldV[16].text())[2:], 16)
		self.currentLight.lobjs[i].Unk8 = \
			int(str(self.fieldV[17].text())[2:], 16)

	def getLightOffsets(self):
		index = self.oldDropDownIndex
		offs = self.fileList[index][1]
		buffer = main_window.fileBuffer
		len = struct.unpack('>I', buffer[offs+4:offs+8])[0]
		return (offs, len)

	def Save(self):
		offs, length = self.getLightOffsets()
		start = main_window.fileBuffer[:offs]
		middle = self.currentLight.pack()
		end = main_window.fileBuffer[offs+length:]
		main_window.fileBuffer = start + middle + end


class FogTab(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.currentFog = None

		self.layout = QVBoxLayout()

		#"""
		self.fileList = []
		self.dropDown = QComboBox()
		self.dropDown.currentIndexChanged.connect(self.fileC)
		self.layout.addWidget(self.dropDown)
		#"""

		#"""
		self.fogDrop = QComboBox()
		self.fogDrop.currentIndexChanged.connect(self.fogC)
		self.layout.addWidget(self.fogDrop)
		#"""

		#"""
		self.fieldsLayout = QGridLayout()

		fields = (('Unk1','0x00000000'), ('Unk2','0x00000000'),
			('StartZ','0.0'), ('EndZ','0.0'),
			('NearZ','0.0'), ('FarZ','0.0'),
			('Color','0x00000000'), ('Flags','0x00000000'),
			('Unk5','0x00000000'), ('Unk6','0x00000000'))

		self.field = [0 for x in xrange(len(fields))]
		self.fieldL = [0 for x in xrange(len(fields))]
		self.fieldV = [0 for x in xrange(len(fields))]

		for i in xrange(len(fields)):
			self.field[i] = QHBoxLayout()
			self.fieldL[i] = QLabel(fields[i][0])
			self.fieldV[i] = QLineEdit(fields[i][1])
			self.fieldV[i].editingFinished.connect(self.Update)
			self.field[i].addWidget(self.fieldL[i])
			self.field[i].addWidget(self.fieldV[i])
			self.fieldsLayout.addLayout(self.field[i],i,0)

		self.layout.addLayout(self.fieldsLayout)
		#"""

		self.setLayout(self.layout)

	def populate(self, list, buffer):
		self.fileList = list
		self.dropDown.clear()
		l = []
		for x in list:
			l.append(x[0])
		self.dropDown.addItems(l)
		self.fileC(0)

	def fileC(self, index):
		if self.currentFog:
			self.Save()
		self.oldDropDownIndex = index
		offs = self.fileList[index][1]
		buffer = main_window.fileBuffer
		self.currentFog = bfog.Bfog(buffer[offs:])
		self.setFogDropCombo(index)

	def setFogDropCombo(self, index):
		count = 0
		self.fogDrop.clear()
		l = []
		for fog in self.currentFog.fogds:
			l.append(str(count))
			count += 1
		self.fogDrop.addItems(l)
		self.setFields(0)

	def setFields(self, index):
		fogd = self.currentFog.fogds[index]
		self.fieldV[0].setText("0x%08x" % fogd.Unk1)
		self.fieldV[1].setText("0x%08x" % fogd.Unk2)
		self.fieldV[2].setText(str(fogd.Float1))
		self.fieldV[3].setText(str(fogd.Float2))
		self.fieldV[4].setText(str(fogd.Float3))
		self.fieldV[5].setText(str(fogd.Float4))
		self.fieldV[6].setText("0x%08x" % fogd.Color)
		self.fieldV[7].setText("0x%08x" % fogd.Flags)
		self.fieldV[8].setText("0x%08x" % fogd.Unk5)
		self.fieldV[9].setText("0x%08x" % fogd.Unk6)

	def fogC(self, index):
		self.setFields(index)

	def Update(self):
		if not self.currentFog:
			return
		i = self.fogDrop.currentIndex()
		self.currentFog.fogds[i].Unk1 = \
			int(str(self.fieldV[0].text())[2:], 16)
		self.currentFog.fogds[i].Unk2 = \
			int(str(self.fieldV[1].text())[2:], 16)
		self.currentFog.fogds[i].Float1 = \
			float(str(self.fieldV[2].text()))
		self.currentFog.fogds[i].Float2 = \
			float(str(self.fieldV[3].text()))
		self.currentFog.fogds[i].Float3 = \
			float(str(self.fieldV[4].text()))
		self.currentFog.fogds[i].Float4 = \
			float(str(self.fieldV[5].text()))
		self.currentFog.fogds[i].Color = \
			int(str(self.fieldV[6].text())[2:], 16)
		self.currentFog.fogds[i].Flags = \
			int(str(self.fieldV[7].text())[2:], 16)
		self.currentFog.fogds[i].Unk5 = \
			int(str(self.fieldV[8].text())[2:], 16)
		self.currentFog.fogds[i].Unk6 = \
			int(str(self.fieldV[9].text())[2:], 16)

	def getFogOffsets(self):
		index = self.oldDropDownIndex
		offs = self.fileList[index][1]
		buffer = main_window.fileBuffer
		len = struct.unpack('>I', buffer[offs+4:offs+8])[0]
		return (offs, len)

	def Save(self):
		offs, length = self.getFogOffsets()
		start = main_window.fileBuffer[:offs]
		middle = self.currentFog.pack()
		end = main_window.fileBuffer[offs+length:]
		main_window.fileBuffer = start + middle + end


class DofTab(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.currentDof = None

		self.layout = QVBoxLayout()

		#"""
		self.fileList = []
		self.dropDown = QComboBox()
		self.dropDown.currentIndexChanged.connect(self.fileC)
		self.layout.addWidget(self.dropDown)
		#"""

		#"""
		self.fieldsLayout = QGridLayout()

		fields = (('Unk1','0x00000000'), ('Unk2','0x00000000'),
			('Unk3','0x0000'), ('Unk4','0x0000'),
			('Unk5','0x0000'), ('Unk6','0x0000'),
			('Float1','0.0'), ('Float2','0.0'),
			('Float3','0.0'), ('Float4','0.0'),
			('Float5','0.0'), ('Float6','0.0'),
			('Float7','0.0'), ('Float8','0.0'),
			('Float9','0.0'), ('FloatA','0.0'),
			('Unk7','0x00000000'), ('Unk8','0x00000000'),
			('Unk9','0x00000000'), ('UnkA','0x00000000'))

		self.field = [0 for x in xrange(len(fields))]
		self.fieldL = [0 for x in xrange(len(fields))]
		self.fieldV = [0 for x in xrange(len(fields))]

		for i in xrange(len(fields)):
			self.field[i] = QHBoxLayout()
			self.fieldL[i] = QLabel(fields[i][0])
			self.fieldV[i] = QLineEdit(fields[i][1])
			self.fieldV[i].editingFinished.connect(self.Update)
			self.field[i].addWidget(self.fieldL[i])
			self.field[i].addWidget(self.fieldV[i])
			self.fieldsLayout.addLayout(self.field[i],i,0)

		self.layout.addLayout(self.fieldsLayout)
		#"""

		self.setLayout(self.layout)

	def populate(self, list, buffer):
		self.fileList = list
		self.dropDown.clear()
		l = []
		for x in list:
			if x[0][-4:] == 'bdof':
				l.append(x[0])
		self.dropDown.addItems(l)
		self.fileC(0)

	def fileC(self, index):
		if self.currentDof:
			self.Save()
		self.oldDropDownIndex = index
		#offs = self.fileList[index][1]
		name = self.dropDown.itemText(index)
		offs = arc.FindFileOff(main_window.fileBuffer, name)
		buffer = main_window.fileBuffer
		self.currentDof = bdof.Bdof()
		self.currentDof.unpack(buffer[offs:offs+len(self.currentDof)])
		self.setFields()

	def setFields(self):
		dof = self.currentDof
		self.fieldV[0].setText("0x%08x" % dof.Unk1)
		self.fieldV[1].setText("0x%08x" % dof.Unk2)
		self.fieldV[2].setText("0x%04x" % dof.Unk3)
		self.fieldV[3].setText("0x%04x" % dof.Unk4)
		self.fieldV[4].setText("0x%04x" % dof.Unk5)
		self.fieldV[5].setText("0x%04x" % dof.Unk6)
		self.fieldV[6].setText(str(dof.Float1))
		self.fieldV[7].setText(str(dof.Float2))
		self.fieldV[8].setText(str(dof.Float3))
		self.fieldV[9].setText(str(dof.Float4))
		self.fieldV[10].setText(str(dof.Float5))
		self.fieldV[11].setText(str(dof.Float6))
		self.fieldV[12].setText(str(dof.Float7))
		self.fieldV[13].setText(str(dof.Float8))
		self.fieldV[14].setText(str(dof.Float9))
		self.fieldV[15].setText(str(dof.FloatA))
		self.fieldV[16].setText("0x%08x" % dof.Unk7)
		self.fieldV[17].setText("0x%08x" % dof.Unk8)
		self.fieldV[18].setText("0x%08x" % dof.Unk9)
		self.fieldV[19].setText("0x%08x" % dof.UnkA)

	def Update(self):
		if not self.currentDof:
			return
		self.currentDof.Unk1 = \
			int(str(self.fieldV[0].text())[2:], 16)
		self.currentDof.Unk2 = \
			int(str(self.fieldV[1].text())[2:], 16)
		self.currentDof.Unk3 = \
			int(str(self.fieldV[2].text())[2:], 16)
		self.currentDof.Unk4 = \
			int(str(self.fieldV[3].text())[2:], 16)
		self.currentDof.Unk5 = \
			int(str(self.fieldV[4].text())[2:], 16)
		self.currentDof.Unk6 = \
			int(str(self.fieldV[5].text())[2:], 16)
		self.currentDof.Float1 = \
			float(str(self.fieldV[6].text()))
		self.currentDof.Float2 = \
			float(str(self.fieldV[7].text()))
		self.currentDof.Float3 = \
			float(str(self.fieldV[8].text()))
		self.currentDof.Float4 = \
			float(str(self.fieldV[9].text()))
		self.currentDof.Float5 = \
			float(str(self.fieldV[10].text()))
		self.currentDof.Float6 = \
			float(str(self.fieldV[11].text()))
		self.currentDof.Float7 = \
			float(str(self.fieldV[12].text()))
		self.currentDof.Float8 = \
			float(str(self.fieldV[13].text()))
		self.currentDof.Float9 = \
			float(str(self.fieldV[14].text()))
		self.currentDof.FloatA = \
			float(str(self.fieldV[15].text()))
		self.currentDof.Unk7 = \
			int(str(self.fieldV[16].text())[2:], 16)
		self.currentDof.Unk8 = \
			int(str(self.fieldV[17].text())[2:], 16)
		self.currentDof.Unk9 = \
			int(str(self.fieldV[18].text())[2:], 16)
		self.currentDof.UnkA = \
			int(str(self.fieldV[19].text())[2:], 16)

	def getDofOffsets(self):
		index = self.oldDropDownIndex
		#offs = self.fileList[index][1]
		name = self.dropDown.itemText(index)
		#print name
		offs = arc.FindFileOff(main_window.fileBuffer, name)
		buffer = main_window.fileBuffer
		len = struct.unpack('>I', buffer[offs+4:offs+8])[0]
		return (offs, len)

	def Save(self):
		offs, length = self.getDofOffsets()
		start = main_window.fileBuffer[:offs]
		middle = self.currentDof.pack()
		end = main_window.fileBuffer[offs+length:]
		main_window.fileBuffer = start + middle + end


class MainGUI(QWidget):
	openFile = None
	savedName = ""
	fileBuffer = ""

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.resize(800,600)
		self.setWindowTitle('Environment Editor')

		self.gridLayout=QGridLayout()
		self.gridLayout.setSpacing(2)
		self.setLayout(self.gridLayout)

		self.openButton=QPushButton('Open')
		self.openButton.clicked.connect(self.Open)
		self.gridLayout.addWidget(self.openButton,0,0)
		self.saveButton=QPushButton('Save')
		self.saveButton.clicked.connect(self.Save)
		self.gridLayout.addWidget(self.saveButton,0,1)
		self.saveAsButton=QPushButton('SaveAs')
		self.saveAsButton.clicked.connect(self.SaveAs)
		self.gridLayout.addWidget(self.saveAsButton,0,2)
		self.exitButton=QPushButton('Exit')
		self.exitButton.clicked.connect(self.Exit)
		self.gridLayout.addWidget(self.exitButton,0,3)

		self.tab=QTabWidget()
		self.dofTab = DofTab()
		self.tab.addTab(self.dofTab, 'dof')
		self.fogTab = FogTab()
		self.tab.addTab(self.fogTab, 'fog')
		self.lightTab = LightTab()
		self.tab.addTab(self.lightTab, 'light')
		self.sceneTab = SceneTab()
		self.tab.addTab(self.sceneTab, 'scene')
		self.gridLayout.addWidget(self.tab,1,0,4,4)

	def Open(self):
		self.openFile = QFileDialog.getOpenFileName(self, 'Choose an environment archive', '', 'Archives (*.arc);;All Files(*)')
		if not self.openFile:
			return
		with open(self.openFile, 'rb') as fp:
			self.fileBuffer = fp.read()
		list = arc.GetFileTree(self.fileBuffer)
		#f = arc.FindFile(self.fileBuffer, "Fire3Scene.blight")
		#print common.xxd(f)
		for x in list:
			if x[0] == "dof":
				self.dofTab.populate(x[1], self.fileBuffer)
			elif x[0] == "fog":
				self.fogTab.populate(x[1], self.fileBuffer)
			elif x[0] == "light":
				self.lightTab.populate(x[1], self.fileBuffer)
			elif x[0] == "scene":
				pass
			else:
				print "Found unknown folder:", x[0]

	def SaveAs(self):
		self.savedName = QFileDialog.getSaveFileName(self, 'Choose an environment archive', '', 'Archives (*.arc);;All Files(*)')

	def Save(self):
		#DO DOF
		self.dofTab.Save()
		#DO FOG
		self.fogTab.Save()
		#DO LIGHT
		self.lightTab.Save()
		#DO SCENE
		if not self.savedName:
			self.savedName = QFileDialog.getSaveFileName(self, 'Choose an environment archive', '', 'Archives (*.arc);;All Files(*)')
			if not self.savedName:
				return
		with open(self.savedName, 'wb') as fp:
			fp.write(self.fileBuffer)

	def Exit(self):
		sys.exit(0)

if __name__ == "__main__":
	app = QApplication(argv)
	global main_window
	main_window = MainGUI()
	main_window.show()
	exit(app.exec_())

