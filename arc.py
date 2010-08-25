from Struct import Struct
import common

class U8Header(Struct):
	__endian__ = Struct.BE
	def __format__(self):
		self.magic = Struct.uint32
		self.rootnode_offset = Struct.uint32
		self.header_size = Struct.uint32
		self.data_offset = Struct.uint32
		self.zeroes = Struct.string(16)
	def __str__(self):
		out  = ""
		out += "Magic: %08x(should be 0x55aa382d)" % self.magic
		out += "\n"
		out += "Rootnode offset: %08x\n" % self.rootnode_offset
		out += "Header size: %08x\n" % self.header_size
		out += "Data offset: %08x" % self.data_offset
		return out

class U8Node(Struct):
	__endian__ = Struct.BE
	def __format__(self):
		self.type = Struct.uint16
		self.name_offset = Struct.uint16
		self.data_offset = Struct.uint32
		self.size = Struct.uint32
	def __str__(self):
		out  = ""
		out += "Type: %04x\n" % self.type
		out += "Name Offset: %04x\n" % self.name_offset
		out += "Data Offset: %08x\n" % self.data_offset
		out += "Size: %08x" % self.size
		return out

def GetRootNodeOff(buffer):
	header = U8Header()
	header.unpack(buffer[:len(header)])
	return header.rootnode_offset

def GetRootNode(buffer):
	off = GetRootNodeOff(buffer)
	node = U8Node()
	node.unpack(buffer[off:off+len(node)])
	return node

def GetNode(buffer, offset):
	node = U8Node()
	node.unpack(buffer[offset:offset+len(node)])
	return node

def GetNodeName(buffer, offset):
	nodes_off = GetRootNodeOff(buffer)
	rootnode = GetRootNode(buffer)
	node = GetNode(buffer, offset)
	return common.nullterm(buffer[nodes_off+(rootnode.size*len(rootnode))+node.name_offset:])

def ListNodes(buffer, off, size, curr):
	list = []
	for x in xrange(size-curr):
		curr += 1
		node = GetNode(buffer, off)
		name = GetNodeName(buffer, off)
		offset = node.data_offset
		off += len(node)
		if node.type == 0x0000:			 # file
			list.append((name, offset))
		elif node.type == 0x0100:		   # folder
			#print node
			#print GetNodeName(buffer, off-len(node))
			sub, total = ListNodes(buffer, off, node.size,curr)
			list.append((name, sub))
			x += (node.size-curr)
			off += len(node)*(node.size-curr)
			curr += node.size-curr
	return list, size

def GetFileTree(buffer):
	tree = []
	off = GetRootNodeOff(buffer)
	rootnode = GetRootNode(buffer)
	off += len(rootnode)

	tree, total = ListNodes(buffer, off, rootnode.size - 1, 1)
	return tree

def FindFileOff(buffer, filename):
	rootnode = GetRootNode(buffer)
	off = GetRootNodeOff(buffer)
	nodes_off = off

	off += len(rootnode)
	for x in xrange(rootnode.size - 1):
		node = GetNode(buffer, off)
		name = GetNodeName(buffer, off)
		if name == filename and node.type == 0x0000:
			return node.data_offset
		off += len(node)
	return 0

def FindFile(buffer, filename):
	file = ""
	rootnode = GetRootNode(buffer)
	off = GetRootNodeOff(buffer)
	nodes_off = off

	off += len(rootnode)
	for x in xrange(rootnode.size - 1):
		node = GetNode(buffer, off)
		name = GetNodeName(buffer, off)
		if name == filename and node.type == 0x0000:
			file = buffer[node.data_offset:node.data_offset+node.size]
			break
		off += len(node)
	return file

