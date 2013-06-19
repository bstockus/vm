# vm_domain.py - Virtual Machine Domain
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values
import vm_trace
import vm_thread
import vm_exception
import vm_pool

class Domain(object):
	# A Domain object
	# Fields:
	#	threads: list<Thread> - the threads running in this domain
	#	pool: list<Blocks> - the block pool for this domain
	#	modules: list<Module> - the modules loaded into this domain
	#	tokens_map:dict<TokenValue,TypeRefValue> - the token to type map
	def __init__(self, token_types):
		# token_types:dict<TokenValue,TypeBlock>
		self.threads = []
		self.pool = vm_pool.Pool()
		self.module = []
		self.tokens_map = {}
		for token_value,type_block in token_types.items():
			type_ref_value = self.pool.add_block(type_block)
			self.tokens_map[token_value.__repr__()] = type_ref_value
	
	def spawn_thread(self, proc):
		# Spawns a new thread in the domain running proc
		self.threads.append(vm_thread.Thread(self, proc))
	
	def run(self):
		# Only supports single-threading at this time
		vm_trace.print_info("Domain", "Running Domain...")
		try:
			while self.threads[0].is_running:
				self.threads[0].step()
		except vm_exception.VMException as e:
			#Handle VM Exception
			vm_trace.print_error(e.error_class, e.error_type, e.error_subtype, e.error_info)
		finally:
			vm_trace.print_info("Domain", "Finished Running Domain...")
			