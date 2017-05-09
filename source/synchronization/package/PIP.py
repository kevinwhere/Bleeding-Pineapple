import heapq
from functions import * 
def Ilp(R,LPTasks,task,k):
	W=0
	for itask in LPTasks:
		x=0
		for q in range(len(task['resGraph'])):
			if itask['resGraph'][q]['totacc']!=0 and itask['resGraph'][q]['PIPPrio']<k:
				x+=itask['resGraph'][q]['totacc']

		W+=Workload_w_C(itask['period'],x,itask['period'],R)
	return W
def Idsr(R,HPTasks,task):
	W=0
	for itask in HPTasks:
		x=0
		for q in range(len(task['resGraph'])):
			if task['resGraph'][q]['totacc']!=0 and itask['resGraph'][q]['totacc']!=0:
				x+=itask['resGraph'][q]['totacc']		
		W+=Workload_w_C(itask['period'],x,itask['period'],R)
	return W
def Insr(R,HPTasks,task):
	W=0
	for itask in HPTasks:
			W+=Workload_w_C(itask['period'],itask['execution'],itask['period'],R)
	return W
def Iosr(R,HPTasks,task):
	W=0
	for itask in HPTasks:
		x=0
		for q in range(len(task['resGraph'])):
			if task['resGraph'][q]['totacc']==0 and itask['resGraph'][q]['totacc']!=0:
				x+=itask['resGraph'][q]['totacc']
		W+=Workload_w_C(itask['period'],x,itask['period'],R)
	return W
def PIPPrio(sortedTasks,numQ):
	for q in range(numQ):		
		for i in range(len(sortedTasks)):
			if sortedTasks[i]['resGraph'][q]['totacc']!=0:
				for itask in sortedTasks:
					itask['resGraph'][q]['PIPPrio']=i
				break
def PIPRTA(task,m,HPTasks,LPTasks,D,k):
	C=task['accExecution']+task['execution']
	R=C
	B=DB(LPTasks,task)
	while True:		
		
		W=C+B+Idsr(R,HPTasks,task)+Insr(R,HPTasks,task)/m+Iosr(R,HPTasks,task)/m+Ilp(R,LPTasks,task,k)/m
		if R>D:
			return R
		if R < W:
			R=W		
		else: 
			return R	
def DB(LPTasks,task):
	B=0
	for q in range(len(task['resGraph'])):
		if task['resGraph'][q]['totacc']!=0:	
			CI=[]
			for itask in LPTasks:
				if itask['resGraph'][q]['totacc']!=0:
					CI.append(itask['resGraph'][q]['maxacc'])
									
							
			decWCtasks=heapq.nlargest(1,CI)			
			B+=task['numCritical']*sum(decWCtasks)
	return B			
def PIP(tasks,m,scheme,numQ):
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	
	PIPPrio(sortedTasks,numQ)
	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		D=task['period']
		WCRT=PIPRTA(task,m,HPTasks,LPTasks,D,i)

		if WCRT > D:
			return False
		else:
			sortedTasks[i]['WCRT']=WCRT
	return True