# vm_print.py - Virtual Machine Opcodes Printer
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values
import vm_frame
import vm_blocks
import vm_domain
import vm_opcode

StackDescMapping = {
	'V' : "Value",
	'I' : "IntValue",
	'F' : "FloatValue",
	'B' : "BoolValue",
	'C' : "CharValue",
	'N' : "NullValue",
	'T' : "TokenValue",
	'R' : "Ref",
	'A' : "ArrayRef",
	'O' : "ObjRef",
	'Y' : "TypeRef",
	'Z' : "ObjOrTypeRef",
	'U' : "UIntValue"
}

def parse_stack_description_list(sdlb, sdla):
	output = "..."
	for sd in sdlb:
		#Parse before stack descriptors
		output += ", "
		type = sd[0]
		type_name = StackDescMapping[type]
		output += type_name + ":" + sd[1]
	output += " --> ..."
	for sd in sdla:
		#Parse before stack descriptors
		output += ", "
		type = sd[0]
		type_name = StackDescMapping[type]
		output += type_name + ":" + sd[1]
	return output
		
# FORMAT: [(opcode:int, name:string, description:string, stack_effects:string, operation:string, is_implemented:bool, is_operand:bool), ...]
def parse_opcodes():
	opcodes = vm_opcode.Opcodes
	output = "Operations:"
	output_list = []
	for k,v in opcodes.items():
		if len(v) >= 6:
			output += "\n"
			ext_info = v[5]
			#Print bytecode and name
			output += "{0:02X} {1:>10}".format(k, v[2])
			out_opcode = k
			#Print operand if there
			out_name = ""
			out_is_operand = False
			if v[0]:
				output += " {0:<5}".format(ext_info['o'])
				out_name = "{0} {1}".format(v[2], ext_info['o'])
				out_is_operand = True
			else:
				output += "      "
				out_name = "{0}".format(v[2])
			#Print operand description
			output += " : {0}".format(ext_info['d'])
			out_description = ext_info['d']
			#Print stack results
			out_stack_effects = ""
			if ('sb' in ext_info) and ('sa' in ext_info):
				output += " (" + parse_stack_description_list(ext_info['sb'], ext_info['sa']) + ")"
				out_stack_effects = parse_stack_description_list(ext_info['sb'], ext_info['sa'])
			out_operation = ""
			if 'm' in ext_info:
				output += " [" + ext_info['m'] + "]"
				out_operation = ext_info['m']
			out_is_implemented = True
			if (v[1] == vm_opcode.op_NI) or (v[1] == vm_opcode.op_NIO):
				output += " *** Not Implemented ***"
				out_is_implemented = False
			output_list.append((out_opcode, out_name, out_description, out_stack_effects, out_operation, out_is_implemented, out_is_operand))
	print output
	return output_list

def generate_file_output(infos):
	output = "<html><head><title>Opcode Listing</title></head><body><h1>Opcode Listing</h1><table border=\'1\'><tr><td>Opcode</td><td>Name</td><td>Description</td><td>Stack</td><td>Operation</td><td>Notes</td></tr>"
	for info in infos:
		output += "<tr>"
		if info[6]:
			output += "<td>{0:02X} XX</td>".format(info[0])
		else:
			output += "<td>{0:02X}</td>".format(info[0])
		output += "<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>".format(info[1], info[2], info[3], info[4])
		if info[5]:
			output += "<td></td>"
		else:
			output += "<td>Not Implemented</td>"
		output += "</tr>"
	output += "</table></body></html>"
	return output

ol = parse_opcodes()
fo = generate_file_output(ol)
f = open("index.html","w")
f.write(fo)
f.close()