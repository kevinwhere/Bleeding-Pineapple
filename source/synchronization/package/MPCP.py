import math
from SAP import * 

def compare_SAP(x,y):
	minxp=100000
	for itask in x:
		if itask['period']<minxp:
			pminxtask=itask
			minxp=itask['period']
	xcost=0
	
	for i in range(len(pminxtask['resGraph'])):
		xLocal=0
		xGlobal=0
		maxA=0
		for itask in x:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']>maxA:
					maxA=itask['resGraph'][i]['maxacc']
		xGlobal=maxA/minxp

		xLocal=0
		for itask in x:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']/itask['period']>xLocal:
					xLocal=itask['resGraph'][i]['maxacc']/itask['period']
		xcost+=xGlobal-xLocal


	minyp=100000
	for itask in y:
		if itask['period']<minyp:
			pminytask=itask
			minyp=itask['period']


	ycost=0
	
	for i in range(len(pminytask['resGraph'])):
		yLocal=0
		yGlobal=0
		maxA=0
		for itask in y:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']>maxA:
					maxA=itask['resGraph'][i]['maxacc']
		yGlobal=maxA/minyp

		yLocal=0
		for itask in x:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']/itask['period']>yLocal:
					yLocal=itask['resGraph'][i]['maxacc']/itask['period']
		ycost+=yGlobal-yLocal

	if xcost>ycost:
		return 1
	else:
		return -1 
def calB_MPCP(basePriok,q,m,procs,D):
	B=0
	for i in range(len(procs)):
		if i == m:
			continue
		for itask in procs[i]:
			if itask['basePrio']>basePriok:
				if itask['resGraph'][q]['totacc']!=0:
					if itask['resGraph'][q]['wpmax']>B:
						B=itask['resGraph'][q]['wpmax']
	R=B
	while True:	
		W=0
		for i in range(len(procs)):
			if i == m:
				continue
			for itask in procs[i]:
				if itask['basePrio']<basePriok:
					if itask['resGraph'][q]['totacc']!=0:
						W+=(math.ceil(R/itask['period'])+1)*itask['resGraph'][q]['wptot']
		if R>D:
			return R
		if R < W+B:
			R=W+B		
		else: 
			return R

def IMPCP(R,HPTasks):
	W=0
	for itask in HPTasks:
		W+=math.ceil((R+itask['MPCP_B'])/itask['period'])*(itask['execution']+itask['accExecution'])

	return W
def MPCPRTA(task,LPTasks,HPTasks,m):

	C=task['execution']+task['accExecution']+task['MPCP_B']
	D=task['period']

	B=0
	for itask in LPTasks:
		for iRes in itask['resEdge']:
			if itask['resGraph'][iRes]['maxacc']>B:
				B=itask['resGraph'][iRes]['maxacc']
	n=0
	for iRes in task['resEdge']:
		n+=task['numCritical']
	
	B=B*(n+1)
	R=C+B

	while True:		
		
		I=IMPCP(R,HPTasks)
		if R>D:
			return R
		if R < I+B+C:
			R=I+B+C	
		else: 
			return R
def MPCP(tasks,M,scheme,numQ):
	
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
	# for iproc in procs:
	# 	sumU=0
	# 	for itaskinProc in iproc:
	# 		sumU+=itaskinProc['utilization']
	# 	print sumU
	# print 
	sortedTasks=sorted(tasks, key=lambda item:item['period'])
	for i in range(len(sortedTasks)):
		sortedTasks[i]['basePrio']=i
	#calculate global priority ceiling 
	for iproc in procs:
		#print len(iproc)
		for iq in range(numQ):
			gs=9999
			for itask in iproc:
				if itask['resGraph'][iq]['totacc']!=0:
					if itask['basePrio'] <= gs:
						gs=itask['basePrio']
			for itask in iproc:
				if itask['resGraph'][iq]['totacc']!=0:
					itask['resGraph'][iq]['gs']=gs
	#print 
	#calculate wprime
	for iproc in procs:			
		for itask in iproc:
			for itaskRes in itask['resEdge']:
				wp=0
				for lctask in iproc:
					maxwp=0
					for iRes in lctask['resEdge']:
						if lctask['resGraph'][iRes]['gs']>itask['resGraph'][itaskRes]['gs']:
							if lctask['resGraph'][iRes]['maxacc']>maxwp:
								maxwp=lctask['resGraph'][iRes]['maxacc']
					wp+=maxwp
				
				itask['resGraph'][itaskRes]['wpmax']=itask['resGraph'][itaskRes]['maxacc']+wp
				itask['resGraph'][itaskRes]['wptot']=itask['resGraph'][itaskRes]['totacc']+wp*itask['numCritical']
				#print itask['resGraph'][itaskRes]['wptot']
				#print itask['resGraph'][itaskRes]['wprime'],itask['resGraph'][itaskRes]['maxacc']
	
	for m in range(len(procs)):
		sortedTasks=sorted(procs[m], key=lambda item:item['period'])
		for i in range(len(sortedTasks)):
			task=sortedTasks[i]
			HPTasks=sortedTasks[:i]
			LPTasks=sortedTasks[i+1:]
			MPCP_B=0
			for iRes in task['resEdge']:
				iB=task['numCritical']*calB_MPCP(task['basePrio'],iRes,m,procs,task['period'])
				task['resGraph'][iRes]['MPCP_B']=iB
				MPCP_B+=iB
			task['MPCP_B']=MPCP_B


			WCRT=MPCPRTA(task,LPTasks,HPTasks,m)
	 		if WCRT > task['period']:
	 			return False
	return True	