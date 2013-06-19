# vm_opcode.py - Virtual Machine Opcodes
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_frame
import vm_trace
import vm_exception
import vm_values
import vm_blocks

def def_op_nulary(operation):
	def op_nulary(frame, opcode):
		results = operation()
		frame.push_eval_stack_value(results)
	return op_nulary

def def_op_unary(inType, operation):
	# inType 'v' = Value, 'i' = IntValue, 'f' = FloatValue
	def op_unary(frame, opcode):
		value = frame.pop_eval_stack_value()
		if vm_values.checkTypeOfValue(inType, value):
			results = operation(value)
			frame.push_eval_stack_value(results)
		else:
			raise vm_exception.VMException("InvalidOperationError", "InvalidValueTypeOnEvalStack", opcode, "Frame")
			frame.thread.halt()
	return op_unary

def def_op_binary(inType_a, inType_b, operation):
	def op_binary(frame, opcode):
		value_a = frame.pop_eval_stack_value()
		value_b = frame.pop_eval_stack_value()
		if vm_values.checkTypeOfValue(inType_a, value_a) and vm_values.checkTypeOfValue(inType_b, value_b):
			results = operation(value_a, value_b)
			frame.push_eval_stack_value(results)
		else:
			raise vm_exception.VMException("InvalidOperationError", "InvalidValueTypeOnEvalStack", opcode, "Frame")
			frame.thread.halt()
	return op_binary

def op_NI(frame, opcode):
	raise vm_exception.VMException("InvalidOperationError", "OpcodeNotImplemented", opcode, "Frame")
	frame.thread.halt()

def op_NIO(frame, opcode, operand):
	op_NI(frame, opcode)

def op_NOP(frame, opcode):
	0 + 0

def op_HALT(frame, opcode):
	frame.thread.halt()

def op_LD_CONST(frame, opcode, operand):
	value = frame.get_const(operand)
	frame.push_eval_stack_value(value)

def op_LD_PARAM(frame, opcode, operand):
	value = frame.get_param(operand)
	frame.push_eval_stack_value(value)

def op_LD_LOCAL(frame, opcode, operand):
	value = frame.get_local(operand)
	frame.push_eval_stack_value(value)

def op_ST_LOCAL(frame, opcode, operand):
	value = frame.pop_eval_stack_value()
	frame.set_local(operand, value)

def op_POP(frame, opcode, operand):
	for x in range(0, operand):
		frame.pop_eval_stack_value()

def op_DUP(frame, opcode):
	value = frame.pop_eval_stack_value()
	frame.push_eval_stack_value(value)
	frame.push_eval_stack_value(value)

def op_LD_TYPE(frame, opcode):
	token_val = frame.pop_eval_stack_value()
	if vm_values.isTokenValue(token_val):
		type_val = frame.get_tokens_map()[token_val.__repr__()]
		frame.push_eval_stack_value(type_val)
	else:
		raise vm_exception.VMException("InvalidOperationError", "InvalidValueTypeOnEvalStack", opcode, "Frame")

def op_NEWOBJ(frame, opcode):
	type_ref_value = frame.pop_eval_stack_value()
	if vm_values.isRefValue(type_ref_value):
		type_block = type_ref_value.block()
		if isinstance(type_block, vm_blocks.Type):
			obj_ref_value = frame.get_pool().add_block(vm_blocks.Obj(type_block.instc_fields_count))
			frame.push_eval_stack_value(obj_ref_value)
		else:
			raise vm_exception.VMException("InvalidOperationError", "InvalidBlockKind", opcode, "Frame")
	else:
		raise vm_exception.VMException("InvalidOperationError", "InvalidValueTypeOnEvalStack", opcode, "Frame")

def op_ST_FIELD(frame, opcode, operand):
	value = frame.pop_eval_stack_value()
	obj_ref_value = frame.pop_eval_stack_value()
	if vm_values.isRefValue(obj_ref_value):
		obj_block = obj_ref_value.block()
		if isinstance(obj_block, vm_blocks.Obj):
			if operand >= len(obj_block.instc_fields):
				raise vm_exception.VMException("InvalidOperationError", "FieldIndexIsOutOfBounds", opcode, "Frame")
			else:
				obj_block.instc_fields[operand] = value
		else:
			raise vm_exception.VMException("InvalidOperationError", "InvalidBlockKind", opcode, "Frame")
	else:
		raise vm_exception.VMException("InvalidOperationError", "InvalidValueTypeOnEvalStack", opcode, "Frame")

# Format: { opcode:int : (needs_operand:bool, function:func(frame, opcode [,operand]), name:int, eval_stack_show:bool, locals_show:bool, [ extended_info:dict], globals_show:bool))}
# Format: extended_info = {d = description:string, o = opcode:string, sb = stack_before:list, sa = stack_after:list, m = method:string} 
Opcodes = {
	99 : (False, op_NI, 'RET', False, False, { 'd':"Returns from the current procedure.", 'sb':['Va'], 'sa':[] })
}

# General Purpose Opcodes (Base = 0)
Opcodes.update({
	0 : (False, op_NOP, 'NOP', False, False, { 'd':"No Operation.", 'sb':[], 'sa':[] }),
	1 : (True, op_POP, 'POP', True, False, { 'd':"Pops num of items of the stack.", 'o':"num", 'sb':['Va'], 'sa':[] }),
	2 : (False, op_DUP, 'DUP', True, False, { 'd':"Duplicates value on top of the stack.", 'sb':['Va'], 'sa':['Va','Va'] }),
	3 : (False, op_NI, 'EX', True, False, { 'd':"Exchanges top two values on the stack", 'sb':['Va','Vb'], 'sa':['Vb','Va'] })
})

# Machine Control Opcodes (Base = 10)
Opcodes.update({
	10 : (False, op_HALT, 'HALT', False, False, {'d':"Halts the thread.", 'o':"", 'sb':[], 'sa':[], 'm':"thread.halt()"}),
	11 : (False, op_NI, 'WAIT', False, False, {'d':"Causes thread to wait for event.", 'o':"", 'sb':[], 'sa':[], 'm':"thread.wait()"}),
	12 : (False, op_NI, 'PAUSE', True, False, {'d':"Causes thread to pause for given duration.", 'o':"", 'sb':['Fa'], 'sa':[], 'm':"thread.pause(a)"})
})

# Load/Store Opcodes (Base = 20, 50)
Opcodes.update({
	20 : (True, op_LD_CONST, 'LD_CONST', True, False, {'d':"Loads a constant onto the stack.", 'o':"index", 'sb':[], 'sa':['Va'], 'm':"consts(index) -> a"}),
	21 : (True, op_LD_PARAM, 'LD_PARAM', True, False, {'d':"Loads a parameter onto the stack.", 'o':"index", 'sb':[], 'sa':['Va'], 'm':"params(index) -> a"}),
	22 : (True, op_LD_LOCAL, 'LD_LOCAL', True, False, {'d':"Loads a local onto the stack.", 'o':"index", 'sb':[], 'sa':['Va'], 'm':"locals(index) -> a"}),
	23 : (True, op_ST_LOCAL, 'ST_LOCAL', True, True, {'d':"Stores item from stack into a local.", 'o':"index", 'sb':['Va'], 'sa':[], 'm':"a -> locals(index)"}),
	24 : (False, def_op_nulary(lambda : int(0)), 'LD_0', True, False, {'d':"Loads an IntValue of 0 on the stack.", 'o':"", 'sb':[], 'sa':['Ia'], 'm':"int(0) -> a"}),
	25 : (False, def_op_nulary(lambda : int(1)), 'LD_1', True, False, {'d':"Loads an IntValue of 1 on the stack.", 'o':"", 'sb':[], 'sa':['Ia'], 'm':"int(1) -> a"}),
	26 : (False, def_op_nulary(lambda : int(-1)), 'LD_M1', True, False, {'d':"Loads an IntValue of -1 on the stack.", 'o':"", 'sb':[], 'sa':['Ia'], 'm':"int(-1) -> a"}),
	27 : (False, def_op_nulary(lambda : vm_values.NullValue()), 'LD_NULL', True, False, {'d':"Loads a NullValue on the stack.", 'o':"", 'sb':[], 'sa':['Na'], 'm':"null() -> a"}),
	28 : (False, def_op_nulary(lambda : True), 'LD_TRUE', True, False, {'d':"Loads a BoolValue of True on the stack.", 'o':"", 'sb':[], 'sa':['Ba'], 'm':"bool(true) -> a"}),
	29 : (False, def_op_nulary(lambda : False), 'LD_FALSE', True, False, {'d':"Loads a BoolValue of False on the stack.", 'o':"", 'sb':[], 'sa':['Ba'], 'm':"bool(false) -> a"}),
	50 : (False, op_NI, 'LD_CLASS', True, False, {'d':"Loads class for a given object.", 'o':"", 'sb':['Oa'], 'sa':['Yb'], 'm':"a.class -> b"}),
	51 : (False, op_NI, 'LD_SUPER', True, False, {'d':"Loads super for a given type.", 'o':"", 'sb':['Ya'], 'sa':['Yb'], 'm':"a.super -> b"}),
	52 : (False, op_NI, 'LD_TYPE', True, False, {'d':"Loads type for a given token.", 'o':"", 'sb':['Ta'], 'sa':['Yb'], 'm':"type(a) -> b"}),
	53 : (False, op_NI, 'LD_ITEM', True, False, {'d':"Loads item from an array onto the stack.", 'o':"", 'sb':['Aa','Ub'], 'sa':['Vc'], 'm':"a[b] -> c"}),
	54 : (False, op_NI, 'ST_ITEM', True, False, {'d':"Stores value from stack into item in array.", 'o':"", 'sb':['Aa','Ub','Vc'], 'sa':[], 'm':"c -> a[b]"}),
	55 : (True, op_NIO, 'LD_FIELD', True, False, {'d':"Loads value from field in object or type.", 'o':"index", 'sb':['Za'], 'sa':['Vb'], 'm':"a.field(index) -> b"}),
	56 : (True, op_ST_FIELD, 'ST_FIELD', True, False, {'d':"Stores value from stack into field in object or type.", 'o':"index", 'sb':['Za','Vb'], 'sa':[], 'm':"b -> a.field(index)"}),
	57 : (False, op_NI, 'LD_COUNT', True, False, {'d':"Loads count for array onto stack.", 'o':"", 'sb':['Aa'], 'sa':['Ub'], 'm':"a.count -> b"}),
	58 : (False, op_LD_TYPE, 'LD_TYPE', True, False, {'d':"Loads a TypeRefValue given a TokenRefValue", 'o':"", 'sb':['Ta'], 'sa':['Yb'], 'm':"types[a] -> b"})
})

# Integer Opcodes (Base = 30)
Opcodes.update({
	30 : (False, def_op_binary('i', 'i', lambda x, y : int(x + y)), 'IADD', True, False, {'d':"Adds the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a + b -> c"}),
	31 : (False, def_op_binary('i', 'i', lambda x, y : int(x - y)), 'ISUB', True, False, {'d':"Subtracts the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a - b -> c"}),
	32 : (False, def_op_binary('i', 'i', lambda x, y : int(x * y)), 'IMUL', True, False, {'d':"Multiplies the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a * b -> c"}),
	33 : (False, def_op_binary('i', 'i', lambda x, y : int(x / y)), 'IDIV', True, False, {'d':"Divides the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a / b -> c"}),
	34 : (False, def_op_unary('i', lambda x : int(x * -1)), 'INEG', True, False, {'d':"Negates the IntValue on top of the stack.", 'o':"", 'sb':['Ia'], 'sa':['Ib'], 'm':"-a -> b"}),
	35 : (False, def_op_unary('i', lambda x : int(x + 1)), 'IING', True, False, {'d':"Increments the IntValue on top of the stack.", 'o':"", 'sb':['Ia'], 'sa':['Ib'], 'm':"++a -> b"}),
	36 : (False, def_op_unary('i', lambda x : int(x - 1)), 'IDEC', True, False, {'d':"Decrements the IntValue on top of the stack.", 'o':"", 'sb':['Ia'], 'sa':['Ib'], 'm':"--a -> b"}),
	37 : (False, op_NI, 'IAND', True, False, {'d':"Bitwise Ands the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a && b -> c"}),
	38 : (False, op_NI, 'INOT', True, False, {'d':"Bitwise Nots the top IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia'], 'sa':['Ib'], 'm':"not(a) -> b"}),
	39 : (False, op_NI, 'IIOR', True, False, {'d':"Bitwise Ors the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a || b -> c"}),
	40 : (False, op_NI, 'IREM', True, False, {'d':"Finds the remainder of the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a % b -> c"}),
	41 : (False, op_NI, 'ISHL', True, False, {'d':"Shifts the IntValue left by the given amount.", 'o':"", 'sb':['Ia','Ub'], 'sa':['Ic'], 'm':"a << b -> c"}),
	42 : (False, op_NI, 'ISHR', True, False, {'d':"Shifts the IntValue right by the given amount.", 'o':"", 'sb':['Ia','Ub'], 'sa':['Ic'], 'm':"a >> b -> c"}),
	43 : (False, op_NI, 'IXOR', True, False, {'d':"Bitwise Exclusive Ors the top two IntValues and puts the results on the stack.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Ic'], 'm':"a XOR b -> c"}),
	44 : (False, def_op_binary('i', 'i', lambda x, y : bool(x == y)), 'ICMP_EQ', True, False, {'d':"Compares two IntValues on top of the stack for equality.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Bc'], 'm':"a == b -> c"}),
	45 : (False, def_op_binary('i', 'i', lambda x, y : bool(x != y)), 'ICMP_NE', True, False, {'d':"Compares two IntValues on top of the stack for non-equality.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Bc'], 'm':"a != b -> c"}),
	46 : (False, def_op_binary('i', 'i', lambda x, y : bool(x < y)), 'ICMP_LT', True, False, {'d':"Compares if the two IntValues on top of the stack are less than.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Bc'], 'm':"a < b -> c"}),
	47 : (False, def_op_binary('i', 'i', lambda x, y : bool(x <= y)), 'ICMP_LE', True, False, {'d':"Compares if the two IntValues on top of the stack are less than or equal.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Bc'], 'm':"a <= b -> c"}),
	48 : (False, def_op_binary('i', 'i', lambda x, y : bool(x > y)), 'ICMP_GT', True, False, {'d':"Compares if the two IntValues on top of the stack are greater than.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Bc'], 'm':"a > b -> c"}),
	49 : (False, def_op_binary('i', 'i', lambda x, y : bool(x >= y)), 'ICMP_GE', True, False, {'d':"Compares if the two IntValues on top of the stack are greater than or equal.", 'o':"", 'sb':['Ia','Ib'], 'sa':['Bc'], 'm':"a >= b -> c"})
})

# Object/Array Opcodes (Base = 60)
Opcodes.update({
	60 : (False, op_NI, 'NEWARRAY', True, False, {'d':"Creates a new array with the given dimensions.", 'o':"", 'sb':['Ua'], 'sa':['Ab'], 'm':"new[a] -> b"}),
	61 : (False, op_NEWOBJ, 'NEWOBJ', True, False, {'d':"Creates a new object with the given type.", 'o':"", 'sb':['Ta'], 'sa':['Ob'], 'm':"new a() -> b"})
})

# Testing Opcodes (Base = 70)
Opcodes.update({
	70 : (False, op_NI, 'ISINT', True, False, {'d':"Determines of the top Value is an IntValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isint(a) -> b"}),
	71 : (False, op_NI, 'ISFLOAT', True, False, {'d':"Determines of the top Value is an FloatValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isfloat(a) -> b"}),
	72 : (False, op_NI, 'ISBOOL', True, False, {'d':"Determines of the top Value is an BoolValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isbool(a) -> b"}),
	73 : (False, op_NI, 'ISCHAR', True, False, {'d':"Determines of the top Value is an CharValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"ischar(a) -> b"}),
	74 : (False, op_NI, 'ISNULL', True, False, {'d':"Determines of the top Value is an NullValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isnull(a) -> b"}),
	75 : (False, op_NI, 'ISTOKEN', True, False, {'d':"Determines of the top Value is an TokenValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"istoken(a) -> b"}),
	76 : (False, op_NI, 'ISREF', True, False, {'d':"Determines of the top Value is an RefValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isref(a) -> b"}),
	77 : (False, op_NI, 'ISARRAY', True, False, {'d':"Determines of the top Value is an ArrayRefValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isarray(a) -> b"}),
	78 : (False, op_NI, 'ISOBJ', True, False, {'d':"Determines of the top Value is an ObjRefValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"isobj(a) -> b"}),
	79 : (False, op_NI, 'ISTYPE', True, False, {'d':"Determines of the top Value is an TypeRefValue.", 'o':"", 'sb':['Va'], 'sa':['Bb'], 'm':"istype(a) -> b"})
})

# Conversion Opcodes (Base = 80)
Opcodes.update({
	81 : (False, op_NI, 'I2F', True, False, {'d':"Converts IntValue to FloatValue.", 'o':"", 'sb':['Ia'], 'sa':['Fb'], 'm':"float(a) -> b"}),
	82 : (False, op_NI, 'I2C', True, False, {'d':"Converts IntValue to CharValue.", 'o':"", 'sb':['Ia'], 'sa':['Cb'], 'm':"char(a) -> b"}),
	83 : (False, def_op_unary('i', lambda x : bool(x)), 'I2B', True, False, {'d':"Converts IntValue to BoolValue.", 'o':"", 'sb':['Ia'], 'sa':['Bb'], 'm':"bool(a) -> b"}),
	84 : (False, def_op_unary('b', lambda x : int(x)), 'B2I', True, False, {'d':"Converts BoolValue to IntValue.", 'o':"", 'sb':['Ba'], 'sa':['Ib'], 'm':"int(a) -> b"}),
	85 : (False, op_NI, 'C2I', True, False, {'d':"Converts CharValue to IntValue.", 'o':"", 'sb':['Ca'], 'sa':['Ib'], 'm':"int(a) -> b"}),
	86 : (False, op_NI, 'F2I', True, False, {'d':"Converts FloatValue to IntValue.", 'o':"", 'sb':['Fa'], 'sa':['Ib'], 'm':"int(a) -> b"})
})

def run_opcode(frame, opcode):
	if opcode in Opcodes:
		opspec = Opcodes[opcode]
		inst_ptr = frame.inst_ptr
		old_eval_stack = list(frame.eval_stack)
		if opspec[0]:
			#This operation needs an operand
			operand = frame.get_opcode()
			opspec[1](frame, opcode, operand)
			vm_trace.print_frame_trace(inst_ptr, opspec[2], operand, old_eval_stack, frame.eval_stack, frame.locals, opspec[3], opspec[4], frame.cycle_count)
		else:
			opspec[1](frame, opcode)
			vm_trace.print_frame_trace(inst_ptr, opspec[2], "", old_eval_stack, frame.eval_stack, frame.locals, opspec[3], opspec[4], frame.cycle_count)
	else:
		raise vm_exception.VMException("InvalidOperationError","UnknownOpcode", opcode, "Frame")
		frame.thread.halt()