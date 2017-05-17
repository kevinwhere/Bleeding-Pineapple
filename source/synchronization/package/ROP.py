import sys
from functions import *
def dbfGMF(task,t,k):
	C1=task['C'][0]
	C2=task['C'][1]
	S=task['S']
	T=task['period']
	D1=task['D'][0]
	D2=task['D'][1]

	if t>k*task['period']:
		dbf1=dbf_constrained_apprx(C1,D1,T,t)+dbf_constrained_apprx(C2,D2,T,t-D1-S)
		dbf2=dbf_constrained_apprx(C2,D2,T,t)+dbf_constrained_apprx(C1,D1,T,t-D2)
	else:
		dbf1=dbf_constrained(C1,D1,T,t)+dbf_constrained(C2,D2,T,t-D1-S)
		dbf2=dbf_constrained(C2,D2,T,t)+dbf_constrained(C1,D1,T,t-D2)

	return max(dbf1,dbf2)
def TerminationCheck(task,scheme,d1):
	if scheme== 'minD' or scheme == 'maxD':		
		if d1>(task['period']-task['S'])/2:		
			return True
	elif scheme=='PBminD':		
		if task['C'][0]<=task['C'][1]:
			ddd=d1+(task['period']-task['S'])*task['C'][0]/(task['C'][0]+task['C'][1])
		else:
			ddd=d1+(task['period']-task['S'])*task['C'][1]/(task['C'][0]+task['C'][1])
			
		if ddd>(task['period']-task['S'])/2:	
			return True
def setDeadline(task,scheme,d):	
	C1=task['C'][0]
	C2=task['C'][1]
	if scheme == 'minD':		
		if C1<C2:
			task['D'][0]=d
			task['D'][1]=task['period']-d-task['S']
		else:
			task['D'][0]=task['period']-d-task['S']
			task['D'][1]=d

	elif scheme == 'PBminD':	
		if C1<C2:
			task['D'][0]=d+(task['period']-task['S'])*C1/(C1+C2)
			task['D'][1]=task['period']-task['S']-task['D'][0]
		else:
			task['D'][1]=d+(task['period']-task['S'])*C2/(C1+C2)
			task['D'][0]=task['period']-task['S']-task['D'][1]
	else:
		sys.exit()
def FirstFit_SyncProc(task,procs,HPTasks,LPTasks,Thetas,scheme):
	for i in range(len(procs)):
		if scheme.split("-")[1] == "FRDFP" or scheme.split("-")[1] == "FRDEDF":
			if FRDFP(task,procs[i],True,Thetas[i],HPTasks+LPTasks):			
				procs[i].append(task)	
				return True
			else:
				continue
		elif scheme.split("-")[1] == "ROP":			
			if ROP(task,procs[i],HPTasks,LPTasks,Thetas,scheme,True,Thetas[i]):			
				procs[i].append(task)	
				return True
			else:
				continue
	return False
def FRDEDF(task,HPTasks,scheme):
	d1=0

	k=int(scheme.split("-")[0].split("=")[2])
	search_scheme=scheme.split("-")[0].split("=")[1]
	task['D']=[0 for i in task['C']]
	while 1:	
		
		setDeadline(task,search_scheme,d1)	

		t=[]
		for a in range(1,k+1):
			for itask in HPTasks+[task]:
				t.append(itask['D'][0]+(a-1)*itask['period'])	
				t.append((a-1)*itask['period'])						
				t.append(itask['period']-(itask['D'][1]+itask['S'])+(a-1)*itask['period'])
				t.append(itask['period']-itask['S']+(a-1)*itask['period'])
			
		flag=False		
		for it in t:
			dbf=0
			for itask in HPTasks+[task]:			
				dbf+=dbfGMF(itask,it,k)		
			if dbf >it:
				flag=True
				break
		#print d1
		if flag==True:
			if search_scheme=='minD' or search_scheme=='PBminD':				
				d1=d1+1			
			else:				
				d1=d1-1
		else:
			return True	
			
		if TerminationCheck(task,search_scheme,d1):
			return False
def GMFWorkload(itask,R):
	W1=Workload(itask['period'],itask['C'][0],R)+Workload(itask['period'],itask['C'][1],max(0,R-itask['D'][0]-itask['S']))
	W2=Workload(itask['period'],itask['C'][1],R)+Workload(itask['period'],itask['C'][0],max(0,R-itask['D'][1]))
	return max(W1,W2)
def FRDFP_RTA(C,D,HPTasks):
	R=C
	while True:		
		I=0
		for itask in HPTasks:
			I=I+GMFWorkload(itask,R)
		if R>D:
			return R
		if R < I+C:
			R=I+C	
		else: 
			return R
def FRDFP_RTA_mix(C,D,HPTasks,Theta,PrimeTasks):
	if len(Theta) == 0:
		print "ddd"
	R=C

	while True:		
		I=0
		for itask in HPTasks:
			I=I+GMFWorkload(itask,R)
		for itask in PrimeTasks:
			Ci=0
			for iq in Theta:				
				Ci=Ci+itask['resGraph'][iq]['totacc']			
			I=I+Workload(itask['period'],Ci,R)
		if R>D:
			return R
		if R < I+C:
			R=I+C	
		else: 
			return R
def FRDFP(task,HPTasks,ifmix,Theta=[],PrimeTasks=[]):
	WCRT=[]
	## get upper bounds on WCRT of each segment 
	for iC in task['C']:
		if ifmix == False:
			WCRT.append(FRDFP_RTA(iC,task['period'],HPTasks))
		else:
			WCRT.append(FRDFP_RTA_mix(iC,task['period'],HPTasks,Theta,PrimeTasks))

	if task['S']+sum(WCRT)>task['period']:
		#print task['S'], WCRT,task['period']
		return False
	else:
		## set subjobs' deadlines
		## the second takes all 
		WCRT[1]=task['period']-task['S']-WCRT[0]
		task['D']=WCRT
		return True
def IROP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmix=False,The=[]):

	W=0
	

	for itask in localHPTasks:
		x=itask['execution']
		W+=Workload_w_C(itask['period'],x,itask['period'],R)

	if ifmix == True:
		for q in The:
			for itask in LPTasks:
				x=0
				if itask['resGraph'][q]['totacc'] != 0:
					x=itask['resGraph'][q]['totacc']
				W+=Workload_w_C(itask['period'],x,itask['period'],R)
					

	for iThe in Thetas:
		
		if not any(j in task['resEdge'] for j in iThe):
			continue		
		A=0
		for q in iThe:
			for itask in HPTasks:
				x=0						
				if itask['resGraph'][q]['totacc']!=0:
					x=itask['resGraph'][q]['totacc']
				A+=Workload_w_C(itask['period'],x,itask['period'],R)
					
		bmax=getBk(task,LPTasks,iThe,scheme)

		n=0
		for q in iThe:				
			if q in task['resEdge']:
				n+=task['numCritical']
			A+=n*bmax

		for q in iThe:					
			for itask in HPTasks:
				x=0							
				if itask['resGraph'][q]['totacc']!=0:
					x=itask['resGraph'][q]['totacc']
				A+=Workload_w_C(itask['period'],x,itask['period'],R)
		
		W+=A
	return W
def RTAROP(task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmix,The):	
	
	C=task['execution']+task['accExecution']
	D=task['period']
	R=C


	while True:		
					
		I=IROP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmix,The)

		if R>D:
			return R
		if R < I+C:
			R=I+C	
		else: 
			return R
def ROP(task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmax=False,The=[]):
	
	WCRT = RTAROP(task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmax,The)
	
	if WCRT > task['period']:
		return False
	else:
		task['WCRT']=WCRT
		return True
def FirstFit(task,procs,HPTasks,LPTasks,Thetas,scheme):

	for i in range(len(procs)):
		canFit=False

		if scheme.split("-")[0] == 'FRDFP':
			canFit=FRDFP(task,procs[i],False)
		elif scheme.split("-")[0].split("=")[0] == 'FRDEDF':			
			canFit=FRDEDF(task,procs[i],scheme)		
		elif scheme.split("-")[0] == 'ROP':			
			canFit=ROP(task,procs[i],HPTasks,LPTasks,Thetas,scheme)
		else:
			sys.exit()

		if canFit:			
			procs[i].append(task)			
			return True
		else:
			continue
	return False

def getBk(task,LPTasks,iTheta,scheme):
	Bk=0

	for itask in LPTasks:
		for iq in iTheta:
			if iq in itask['resEdge']:						
				if scheme.split("-")[1] == 'NPP':
					Bk=max(Bk,itask['resGraph'][iq]['maxacc'])
				elif scheme.split("-")[1] == 'PCP':					
					if itask['resGraph'][iq]['PCPPrio']<=task['resGraph'][iq]['basePrio']:
						Bk=max(Bk,itask['resGraph'][iq]['maxacc'])
				else:
					print "Oops:getBk"
					sys.exit()
	return Bk
def RTA_FRD(B,C,D,HPtasks,q):
	Ck=B+C	
	R=Ck
	while True:
		I=0
		for itask in HPtasks:
			Ci=0			
			for iq in q:
				if iq in itask['resEdge']:
					Ci=Ci+itask['resGraph'][iq]['totacc']
			I=I+Workload(itask['period'],Ci,R)
		if R>D:
			return R
		if R < I+Ck:
			R=I+Ck	
		else: 
			return R
def calMaxSusp(tasks,Thetas,scheme):

	sortedTasks=sorted(tasks, key=lambda item:item['period'])	
	for m in range(len(Thetas)):
		for i in range(len(sortedTasks)):	
			if any(j in sortedTasks[i]['resEdge'] for j in Thetas[m]):		
				HPTasks=sortedTasks[:i]
				LPTasks=sortedTasks[i+1:]
				
				Ck=sortedTasks[i]['execution']
				Dk=sortedTasks[i]['period']
				Bk=getBk(sortedTasks[i],LPTasks,Thetas[m],scheme)
				Sk=RTA_FRD(Bk,Ck,Dk,HPTasks,Thetas[m])
				sortedTasks[i]['S']=Sk
				if Sk>Dk:
					return False
	return True
def slack_cmp(x):	
	return x['period']-x['S']
def RAM(tasks,M,Thetas,scheme,numQ):

	procs=[]
	other=[]
	## sort tasks in order of decreasing priorities
	## Deadline-Monotonic, Slack-Laxiety-Monotonic 
	for i in range(int(M)):
		proc=[]
		procs.append(proc)
	if scheme.split("-")[3] == "DM" or scheme.split("-")[3] == "RM":
		sortedTasks=sorted(tasks, key=lambda item:item['period'])	
	elif scheme.split("-")[3] == "SLM":
		sortedTasks=sorted(tasks, key=slack_cmp)		
	else:
		print "Oops!"
		sys.exit()

	syncprocs=[]
	for i in range(len(Thetas)):					
		syncprocs.append([])
	

	for i in range(len(sortedTasks)):
		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		if scheme.split("-")[2] == "FF":
			# if FirstFitDPCP(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:
			# 	return False
			## Try application processor first
			if FirstFit(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:
				## Try schronization processor 			
				if FirstFit_SyncProc(sortedTasks[i],syncprocs,HPTasks,LPTasks,Thetas,scheme)== False:
					return False
		else :
			return False
		# if FirstFit(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:

		
		# 	return False

		

	return True
# set up priority ceiling table
def setPCP(tasks,numQ):
	sortedTasks=sorted(tasks, key=lambda item:item['period'])
	for q in range(numQ):
		highestP=-1
		for j in range(len(sortedTasks)):
			if sortedTasks[j]['resGraph'][q]['totacc']!=0:
				highestP=j
				break
		for j in range(len(sortedTasks)):
			sortedTasks[j]['resGraph'][q]['basePrio']=j
			if sortedTasks[j]['resGraph'][q]['totacc']!=0:
				sortedTasks[j]['resGraph'][q]['PCPPrio']=highestP
def WFD(LOADA,Thetas):

	#numNC=0
	## sort resources in order of non-increasing utilizations
	sortedLOADA=sorted(LOADA, key=lambda item:item['utilization'],reverse=True)
	table={}
	for i in sortedLOADA:
		table[i['which']]=i['utilization']
	for i in sortedLOADA:
		minSumProc=[]
		minSumU=9999
		for j in range(len(Thetas)):		
			u=0
			for iq in Thetas[j]:
				u+=table[iq]
			if u < minSumU:
				minSumU=u
				minSumProc=Thetas[j]		

	
		minSumProc.append(i['which'])

## ROP
def ReasonableAllocation(tasks,M,scheme,numQ):
	
	LOADA=[]
	
	## calculate the total utilization on each shared resource 
	for i in range(numQ):
		t=0
		for itask in tasks:
			t+=itask['resGraph'][i]['totacc']/itask['period']
		AJ={}
		AJ['which']=i
		AJ['utilization']=t
		LOADA.append(AJ)
	
	
	for m in range(1,min(M,numQ)):
		
		Thetas=[[]for j in range(m)]

		# Worst-Fit Decreasing
		WFD(LOADA,Thetas)
		
		# Set priority ceiling if PCP is used
		if scheme.split("-")[1] == "PCP" or scheme.split("-")[1] == "DPCP":
			setPCP(tasks,numQ)
		# Set max suspension time if period enforcement is used
		if scheme.split("-")[0] == "FRDFP" or scheme.split("-")[0].split("=")[0] == "FRDEDF":
			if calMaxSusp(tasks,Thetas,scheme) == False:
				continue
		# task allocation
		if RAM(tasks,M-m,Thetas,scheme,numQ) == True:			
			return True

		
	return False