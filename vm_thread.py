# vm_thread.py - Virtual Machine Thread
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values
import vm_trace
import vm_frame
import vm_domain
import vm_exception

class Thread(object):
	# A thread object
	# Fields:
	#	domain: Domain - the domain this thread run in
	#	frame_stack: list<Frame> - the frame stack
	#	is_running: bool - the run status of the thread
	def __init__(self, domain, proc):
		self.domain = domain
		self.frame_stack = []
		self.is_running = True
		self.call_proc(proc, [])
	
	def current_frame(self):
		return self.frame_stack[len(self.frame_stack) - 1]
	
	def step(self):
		self.current_frame().step()
	
	def call_proc(self, proc, params):
		vm_trace.print_info("Thread", "Procedure Called (params = {0}, consts = {1})".format(params, proc.consts))
		self.frame_stack.append(vm_frame.Frame(self, proc, params))
	
	def ret_proc(self, ret_value):
		vm_trace.print_info("Thread", "Procedure Returned (return value = {0})".format(ret_value))
		self.frame_stack.pop()
		if len(self.frame_stack) <= 0:
			self.halt()
		else:
			self.current_frame().push_eval_stack_value(ret_value)
	
	def halt(self):
		vm_trace.print_info("Thread", "Thread Halted.")
		self.is_running = False
	