# vm_blocks.py - Virtual Machine Blocks Implementation
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values

class Block:
	# Fields:
	#	block_kind:enum<int> - the kind of the block {0=Empty, 1=Type, 2=Obj, 3=Array, 4=Proc, 5=Module}
	def __init__(self, block_type):
		self.block_type = block_type


class Type(Block):
	# Fields:
	#	type_id:String - the type's id string
	#	instc_fields_count:uint
	#	class_fields_count:uint
	def __init__(self, instc_fields_count, class_fields_count):
		Block.__init__(self, 1)
		self.instc_fields_count = instc_fields_count
		self.class_fields_count = class_fields_count
	def __repr__(self):
		return "[Type: instc_fields_count={0} class_fields_count={1}]".format(self.instc_fields_count, self.class_fields_count)

class Obj(Block):
	# Fields:
	#	instc_fields:List<Value> - the object's instance fields
	def __init__(self, instc_fields_count):
		Block.__init__(self, 2)
		self.instc_fields = [vm_values.NullValue()] * instc_fields_count
	def __repr__(self):
		return "[Obj: instc_fields={0}]".format(self.instc_fields)

class Array(Block):
	# Fields:
	#	
	def __init__(self):
		Block.__init__(self, 3)

class Module(Block):
	# Fields:
	#	module_id:String - the module's id string
	#	types:List<Type> - the module's types
	#	procs:List<Proc> - the module's procs
	def __init__(self, module_id, types, procs):
		Block.__init__(self, 5)
		self.module_id = module_id
		self.types = types
		self.procs = procs

class Proc(Block):
	# A procedure object
	# Fields:
	#	params_count: int - the number of Params needed by this Proc
	#	locals_count: int - the number of Locals needed by this Proc
	#	consts: list<values> - the constants needed by this Proc
	#	opcodes: list<int> - the opcodes for this Proc
	def __init__(self, params_count, locals_count, consts, opcodes):
		Block.__init__(self, 4)
		self.params_count = params_count
		self.locals_count = locals_count
		self.consts = consts
		self.opcodes = opcodes