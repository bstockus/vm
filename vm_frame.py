# vm_frame.py - Virtual Machine Frame Type Definitions
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values
import vm_trace	
import vm_blocks
import vm_thread
import vm_exception
import vm_opcode

class Frame(object):
	# A frame object
	# Fields:
	#	thread: Thread - the Thread this frame is running on
	#	frame_proc: Proc - the Proc object this frame is running
	#	params: list<values> - the params passed to this frame
	#	locals: list<values> - the locals used by this frame
	#	inst_ptr: int - the current instruction pointer
	#	eval_stack: list<values> - the evaluation stack
	def __init__(self, thread, frame_proc, params):
		self.thread = thread
		self.frame_proc = frame_proc
		self.params = params
		self.locals = [vm_values.NullValue()] * frame_proc.locals_count
		self.inst_ptr = -1
		self.cycle_count = 0
		self.eval_stack = []
	
	def pop_eval_stack_value(self):
		if len(self.eval_stack) <= 0:
			raise vm_exception.VMException("InvalidOperationError","EvalStackIsEmpty", "", "Frame")
			self.thread.halt()
			return
		else:
			return self.eval_stack.pop()
	
	def push_eval_stack_value(self, value):
		self.eval_stack.append(value)
	
	def get_const(self, index):
		if index >= len(self.frame_proc.consts):
			raise vm_exception.VMException("InvalidOperationError","ConstIndexOutOfBounds", index, "Frame")
			self.thread.halt()
			return
		else:
			return self.frame_proc.consts[index]
	
	def get_param(self, index):
		if index >= len(self.params):
			raise vm_exception.VMException("InvalidOperationError","ParamIndexOutOfBounds", index, "Frame")
			self.thread.halt()
			return
		else:
			return self.params[index]
	
	def get_local(self, index):
		if index >= len(self.locals):
			raise vm_exception.VMException("InvalidOperationError","LocalIndexOutOfBounds", index, "Frame")
			self.thread.halt()
			return
		else:
			return self.locals[index]
	
	def set_local(self, index, value):
		if index >= len(self.locals):
			raise vm_exception.VMException("InvalidOperationError","LocalIndexOutOfBounds", index, "Frame")
			self.thread.halt()
		else:
			self.locals[index] = value
	
	def get_opcode(self):
		self.inst_ptr += 1
		if self.inst_ptr >= len(self.frame_proc.opcodes):
			raise vm_exception.VMException("InvalidOperationError","InstructionPointerOutOfBounds", self.inst_ptr, "Frame")
			self.thread.halt()
			return
		return self.frame_proc.opcodes[self.inst_ptr]
	
	def get_pool(self):
		return self.thread.domain.pool
	
	def get_tokens_map(self):
		return self.thread.domain.tokens_map
	
	def step(self):
		opcode = self.get_opcode()
		self.cycle_count += 1
		vm_opcode.run_opcode(self, opcode)

