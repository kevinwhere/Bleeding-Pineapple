def calU(sysl,k,tasks):
	sysCLU=0
	for itask in tasks:
		if len(itask)==sysl:			
			sysCLU+=itask[k-1]['utilization']
	return sysCLU
def DBF_MC(tasks,numCL):

	for k in range(1,numCL+1):
		U=0
		#only those tasks with criticality level larger than or equal to k
		for l in range(k,numCL+1):
			U+=calU(l,k,tasks)

		if U>1:
			return False
	return True