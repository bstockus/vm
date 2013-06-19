# vm_trace.py - Virtual Machine Trace Helpers
# (c) 2013, Bryan Stockus. All Rights Reserved.

def term(cmd):
	return "\033[" + cmd + "m"
def termn(cmds):
	output = ""
	for s in cmds:
		output += "\033[" + s + "m"
	return output

def print_error(error_class, error_type, error_reason, error_description):
	print ("\007" + termn(['91','1']) + "[ERROR:" + term('4') + "{3}" + termn(['0','91','1']) + "] {0}: {1} ({2})" + term('0')).format(error_type, error_reason, error_description, error_class)

def print_frame_trace(inst_ptr, opcode, operand, desc, results, locals, evalsShow, localsShow, cycle_count):
	output = ( termn(['94','1']) + "[TRACE:" + term('4') + "Frame" + termn(['0', '1', '94']) + "]" + term('0') + " " + term('94') + "{2:04}: " + termn(['0', '92']) + "{0:04X}" + term('0') + " " + term('1') + "{1:>10}").format(inst_ptr, opcode, cycle_count)
	if operand == "":
		output += "    " + term('0')
	else:
		output += (" {0:02X} " + term('0')).format(operand)
	if evalsShow:
		output += ("(" + term('93') + "{0} => {1}" + term('0') + ") ").format(desc, results)
	if localsShow:
		output += ("(" + term('95') + "{0}" + term('0') + ")").format(locals)
	print output

def print_info(trace_class, trace_message):
	print (termn(['37','1']) + "[INFO:" + term('4') + "{0}" + termn(['0', '37', '1']) + "]" + term('0') + " " + term('37') + "{1}" + term('0')).format(trace_class, trace_message)