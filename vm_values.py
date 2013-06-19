# vm_values.py - Virtual Machine Value Type Definitions
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_pool

class NullValue(object):
	# defines a null
	def __str__(self):
		return "<NullValue>"
	def __repr__(self):
		return "Null"
	
class TokenValue(object):
	# defines a type token value
	def __init__(self, moduleId, typeId):
		self.moduleId = moduleId
		self.typeId = typeId
	def moduleId(self):
		return self.moduleId
	def typeId(self):
		return self.typeId
	def __repr__(self):
		return "{0}.{1}".format(self.moduleId, self.typeId)

class RefValue(object):
	# Fields:
	#	ref_index:uint - the reference index to the block
	#	pool:Pool - the pool this block is stored in
	def __init__(self, ref_index, pool):
		self.ref_index = ref_index
		self.pool = pool
	def __repr__(self):
		return "<{0}>".format(self.ref_index)
	def block(self):
		return self.pool.get_block(self.ref_index)

def isNullValue(object):
	if isinstance(object, NullValue):
		return True
	else :
		return False

def isIntValue(object):
	if isinstance(object, int):
		return True
	else :
		return False

def isFloatValue(object):
	if isinstance(object, float):
		return True
	else :
		return False

def isBoolValue(object):
	if isinstance(object, bool):
		return True
	else :
		return False

def isTokenValue(object):
	if isinstance(object, TokenValue):
		return True
	else :
		return False

def isRefValue(object):
	if isinstance(object, RefValue):
		return True
	else:
		return False

def checkTypeOfValue(type, value):
	if type == 'v':
		return True
	elif (type == 'n') and isNullValue(value):
		return True
	elif (type == 'i') and isIntValue(value):
		return True
	elif (type == 'b') and isBoolValue(value):
		return True
	elif (type == 't') and isTokenValue(value):
		return True
	elif (type == 'r') and isRefValue(value):
		return True
	else:
		return False