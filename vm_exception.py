# vm_exception.py - Virtual Machine Exceptions
# (c) 2013, Bryan Stockus. All Rights Reserved.

class VMException(Exception):
	def __init__(self, error_type, error_subtype, error_info, error_class):
		self.error_type = error_type
		self.error_subtype = error_subtype
		self.error_info = error_info
		self.error_class = error_class