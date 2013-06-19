# vm.py - Virtual Machine Implementation
# (c) 2013, Bryan Stockus. All Rights Reserved.

import vm_values
import vm_frame
import vm_blocks
import vm_domain
import vm_trace

consts = [	3,
			5,
			6,
			vm_values.TokenValue("sys","obj"),
			True,
			float(33.076)
		]

codes = [	20, 3,
			58,
			61,
			2,
			2,
			2,
			2,
			20, 0,
			56, 0,
			20, 1,
			56, 1,
			20, 2,
			56, 2,
			20, 4,
			56, 3,
			20, 5,
			56, 4,
			10		# HALT
		]

token_types = 	{
					vm_values.TokenValue("sys","obj") : vm_blocks.Type(5,5)
				}

proc = vm_blocks.Proc(0, 5, consts, codes)
domain = vm_domain.Domain(token_types)
domain.spawn_thread(proc)
domain.run()

vm_trace.print_info('Domain', "Tokens Map = {0}".format(domain.tokens_map))
vm_trace.print_info('Domain', "Pool = {0}".format(domain.pool.blocks))