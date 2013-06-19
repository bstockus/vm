# vm_pool.py - Virtual Machine Pool Implementation
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values
import vm_blocks

class Pool(object):
	# Fields:
	#	blocks:dict<uint,Block> - the blocks in this pool
	#	current_index:uint - the current index value
	def __init__(self):
		self.blocks = {}
		self.current_index = 0
	
	def add_block(self, block):
		# Adds the block to this pool, and returns a RefValue
		self.blocks[self.current_index] = block
		ref_value = vm_values.RefValue(self.current_index, self)
		self.current_index += 1
		return ref_value
	
	def get_block(self, ref_index):
		return self.blocks[ref_index]