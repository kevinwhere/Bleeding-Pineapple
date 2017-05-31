def calU(sysl,k,tasks):
	sysCLU=0
	for itask in tasks:
		if len(itask)==sysl:			
			sysCLU+=itask[k-1]['utilization']
	return sysCLU
def EDF_VD2(tasks,numCL):
	
	UHinL=0
	UHinH=0
	ULinL=0
	for itask in tasks:
		if len(itask) == 2: 
			UHinL+=itask[0]['utilization']
			UHinH+=itask[1]['utilization']
		else:
			ULinL+=itask[0]['utilization']
	x=UHinL/(1-ULinL)	
	if UHinH+ULinL<=1:
		return True

	if x*ULinL+UHinH>1:
		return False
	else:
		return True

def EDF_VD(tasks,numCL):
	
	U=0	
	for l in range(1,numCL+1):
		U+=calU(l,l,tasks)
	#print U
	if not (U>1):
		return True
	

	for k in range(1,numCL):		
		Uk=0
		for l in range(1,k+1):
			Uk+=calU(l,l,tasks)

		if Uk<1:
			Ulk=0
			for l in range(k+1,numCL+1):
				Ulk+=calU(l,k,tasks)

			Ull=0
			for l in range(1,k+1):
				Ull+=calU(l,l,tasks)
			
			Ullk=0

			for l in range(k+1,numCL+1):
				Ullk+=calU(l,l,tasks)

			if Ulk/(1-Ull)>(1-Ullk)/Ull:
				continue
			else:
				return True
		else:
			continue
	return False

