import math
from SAP import * 

def IMrsP(R,HPTasks):
	W=0
	for itask in HPTasks:

		CC=itask['execution']+itask['accExecution']
		for q in itask['resEdge']:			
			CC+=itask['resGraph'][q]['e']*itask['numCritical']

		W+=math.ceil((R)/itask['period'])*CC
	return W
def MrsPRTA(task,LPTasks,HPTasks,m):

	C=task['execution']+task['accExecution']
	D=task['period']
	for q in task['resEdge']:
		C+=task['resGraph'][q]['e']

	B=0
	for lptask in LPTasks:
		for iRes in lptask['resEdge']:
			flag=False
			for ihptask in HPTasks+[task]:
				if ihptask['resGraph'][iRes]['totacc']!=0:
					flag=True
					break

			if lptask['resGraph'][iRes]['e']>B and flag==True:
				B=lptask['resGraph'][iRes]['e']
	
	
	
	R=C+B

	while True:		
		
		I=IMrsP(R,HPTasks)
		if R>D:
			return R
		if R < I+B+C:
			R=I+B+C	
		else: 
			return R

def MrsP(tasks,M,scheme,numQ):
	
	MacroTasks=[]
	Res=[]
	for i in range(numQ):
		Q={}
		Q['which']=i
		Q['taskEdge']=[]
		Q['visited']=False
		Q['tobevisited']=False
		Res.append(Q)
	
	for itask in tasks:
		itask['visited']=False
		for q in itask['resEdge']:			
			Res[q]['taskEdge'].append(itask)
		
	
	for iRes in Res:
		if iRes['visited']== False:			
			visitingReq=[]
			visitingReq.append(iRes)
			iRes['tobevisited']=True
			iMacro=[]
			while len(visitingReq)!=0:
				

				if visitingReq[0]['visited']!=True:
					for itask in visitingReq[0]['taskEdge']:
						if itask['visited'] == False:
							itask['visited']=True
							iMacro.append(itask)
					Res[visitingReq[0]['which']]['visited']=True
					
					visitingReq.pop(0)
					
					
					for itask in iMacro:
						for q in itask['resEdge']:							
							if Res[q]['visited'] == False and Res[q]['tobevisited'] == False:
								Res[q]['tobevisited'] = True
								visitingReq.append(Res[q])

			if len(iMacro) !=0:
				MacroTasks.append(iMacro)
	procs=[]
	for i in range(int(M)):
		proc=[]
		procs.append(proc)


	# sortedTasks=sorted(tasks, key=lambda item:item['period'])

	# for i in range(len(sortedTasks)):
	# 	task=sortedTasks[i]
	# 	LPTasks=sortedTasks[i+1:]
	# 	for q in task['resEdge']:
	# 		B=0
	# 		for lptask in LPTasks:
	# 			if	lptask['resGraph'][q]['maxacc']>B:
	# 				B=lptask['resGraph'][q]['maxacc']
	# 		task['resGraph'][q]['wblk']=B
	# for iMacro in MacroTasks:
	# 	print len(iMacro)

	for itask in tasks:
		if itask['visited']== False:
			MacroTasks.append([itask])

	
	sortedMacroTasks=sorted(MacroTasks, cmp=numeric_compare)


	leftTasks=[]
	for itaskinMacroTasks in sortedMacroTasks:
		#print len(itaskinMacroTasks)
		macroU=0
		for itask in itaskinMacroTasks:
			macroU+=itask['utilization']
		
		minU=1
		
		for iproc in procs:
			sumU=0
			for itaskinProc in iproc:
				sumU+=itaskinProc['utilization']
			if sumU <minU:
				minU=sumU
				minProc=iproc
		#print minU,macroU
		if minU+macroU>1:
			leftTasks.append(itaskinMacroTasks)
		else:
			for itask in itaskinMacroTasks:
				minProc.append(itask)
	#print "after"
	#print "left:",len(leftTasks)
	for itaskinProc in procs:	
		sumU=0
		for itask in itaskinProc:
			sumU+=itask['utilization']
		#print len(itaskinProc),sumU	
	#print 

	sortedleftMacroTasks=sorted(leftTasks, cmp=compare_SAP)

	for iMacro in sortedleftMacroTasks:


		sortediMacro=sorted(iMacro, key=lambda item:item['utilization'],reverse=True)
		while len(sortediMacro)!=0:
			minU=1
			
			for iproc in procs:
				sumU=0
				for itaskinProc in iproc:
					sumU+=itaskinProc['utilization']
				if sumU <minU:
					minU=sumU
					minProc=iproc

			if sortediMacro[0]['utilization']+minU>1:
				return False
			


			while not (sortediMacro[0]['utilization']+minU>1):

				minProc.append(sortediMacro[0])
				minU+=sortediMacro[0]['utilization']
				sortediMacro.pop(0)
				if len(sortediMacro)==0:
					break

	sortedTasks=sorted(tasks, key=lambda item:item['period'])
	for i in range(len(sortedTasks)):
		sortedTasks[i]['basePrio']=i
	#calculate global priority ceiling 
	for iproc in procs:		
		for iq in range(numQ):
			gs=9999
			for itask in iproc:
				if itask['resGraph'][iq]['totacc']!=0:
					if itask['basePrio'] <= gs:
						gs=itask['basePrio']
			for itask in iproc:
				if itask['resGraph'][iq]['totacc']!=0:
					itask['resGraph'][iq]['gs']=gs
	 
	#calculate wprime
	for iproc in procs:	
		for q in range(numQ):
			for itask in iproc:
				if itask['resGraph'][q]['totacc']!=0:
					itask['resGraph'][q]['e']=itask['resGraph'][q]['maxacc']

	for iproc in procs:	
		for q in range(numQ):
			maxB=0
			for itask in iproc:
				if itask['resGraph'][q]['totacc']!=0:
					if itask['resGraph'][q]['maxacc']>maxB:
						maxB=itask['resGraph'][q]['maxacc']

			for jproc in procs:				
				if jproc != iproc:
					for jtask in jproc:
						if jtask['resGraph'][q]['totacc']!=0:
							jtask['resGraph'][q]['e']+=maxB*jtask['numCritical']





	for m in range(len(procs)):
		sortedTasks=sorted(procs[m], key=lambda item:item['period'])
		for i in range(len(sortedTasks)):
			task=sortedTasks[i]
			HPTasks=sortedTasks[:i]
			LPTasks=sortedTasks[i+1:]
			# MPCP_B=0
			# for iRes in task['resEdge']:
			# 	iB=task['numCritical']*calB_MPCP(task['basePrio'],iRes,m,procs,task['period'])
			# 	task['resGraph'][iRes]['MPCP_B']=iB
			# 	MPCP_B+=iB
			# task['MPCP_B']=MPCP_B


			WCRT=MrsPRTA(task,LPTasks,HPTasks,m)
	 		if WCRT > task['period']:
	 			return False
	return True