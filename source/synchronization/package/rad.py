from __future__ import division
import random
import math
import json
import sys, getopt
import heapq
maxmaxP=[]
rfile=""

selectUT=""
mProc=1
Cn=1
def parameterRead():
	global rfile,selectUT,selectUT,mProc
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:s:m:")
	except getopt.GetoptError:
		print 'test.py -i <seed> -u <totalutilzation> -if <scalefactor>'
		sys.exit(2)
	print opts, args
	
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <randoseed> -u <totalutilzation> -f <scalefactor>'
			sys.exit()		
		elif opt in ("-i", "--input"):
			rfile = arg
		elif opt in ("-s", "--select"):
			selectUT = arg
		elif opt in ("-m", "--proc"):
			mProc = int(arg)
		else:
			assert False, "unhandled option"

def lm_cmp(x, y):
	dx=x['period']-x['accExecution']
	dy=y['period']-y['accExecution']
	return int(dx - dy)

def AccRBF(t,tasks,tight=False):
	sumW=0
	for itask in tasks:
		if tight == False:
			sumW+=itask['accExecution']+itask['accExecution']*math.ceil((t)/itask['period'])
		else:
			sumW+=itask['accExecution']*math.ceil((t+itask['WCRT']-itask['accExecution'])/itask['period'])
	return sumW
def getSumA(remoteHPTasks,t,rho,scheme):
	sumA=0
	for itask in remoteHPTasks:
		if scheme == 'MIRROR-MC':

			sumA+=itask['accExecution']*math.ceil(t/itask['period'])
		else:
			sumA+=itask['accExecution']*(rho-1+math.ceil((t+rho*(itask['WCRT']-itask['accExecution']))/itask['period']))
		
	return sumA
def getSumC(HPTasks,t,rho):
	sumA=0
	for itask in HPTasks:
		sumA+=itask['execution']*(rho-1+math.ceil((t+rho*(itask['WCRT']-itask['execution']))/itask['period']))
		
	
	return sumA
def getSSA(task,remoteHPTasks,D,scheme=''):

	R=0
	A=task['accExecution']
	while True:		
		W=getSumA(remoteHPTasks,R,task['rho'],scheme)
		if R>D:
			return R
		if R < W+A:
			R=W+A			
		else: 
			return R
def getSSC(task,HPTasks,D,rho_C):

	R=0
	C=task['execution']
	while True:		
		W=getSumC(HPTasks,R,rho_C)
		if R>D:
			return R
		if R < W+C:
			R=W+C			
		else: 
			return R
def getBlocking2(task,remoteHPTasks):

	return task['accExecution']+AccRBF(task['period'],remoteHPTasks,tight=True)
def getWinGlobal(t,x,task):
		
	n=int((t-x+task['period'])/task['period'])
	
	return n*x+min(x,t-x+task['period']-task['period']*n)
def locRBF(t,tasks):
	sumW=0
	for itask in tasks:		
		sumW+=itask['execution']*math.ceil((t+itask['WCRT']-itask['execution'])/itask['period'])
	return sumW

def accRBF(t,tasks,q):
	sumW=0
	for itask in tasks:	
		if itask['resGraph'][q]['totacc']!=0:
			sumW+=itask['resGraph'][q]['totacc']*math.ceil((t+itask['WCRT']-itask['resGraph'][q]['totacc'])/itask['period'])
	return sumW

def SUMRTA(C,rho,HPTasks,D):
	R=0
	while True:		

		W=(rho+1)*locRBF(R,HPTasks,tight=True)

		if R>D:
			return R
		if R < W+C:
			R=W+C		
		else: 
			return R
def FILLRTA(C,B,HPTasks,D,ifss):
	R=0
	
	while True:		
		W=locRBF(R,HPTasks,ifss,tight=True)
		if R>D:
			return R
		if R < W+C+B:
			R=W+C+B			
		else: 
			return R
def getWinGlobalWCRT(t,x,task):	
	
	return x*math.ceil((t+task['WCRT']-x)/task['period'])

def getWCRTsigma(t,x,task,sigma):	
	
	return x*(sigma-1+math.ceil((t+sigma*(task['WCRT']-x))/task['period']))
def IW(localHPTasks,R,num,Q,q):
	W=0

	for itask in localHPTasks:
		if Q=='':
			W+=Jitter(itask,R,itask['execution'],num)
		else:
			W+=Jitter(itask,R,itask['resGraph'][q],num)
	return W

def myRTA(C,localHPTasks,D,num,Q='',q=0):
	
	R=C
	while True:			

		W=IW(localHPTasks,R,num,Q,q)
		if R>D:
			return R
		if R < W+C:
			R=W+C	
		else: 
			return R
def Jitter(task,t,x,num):
	return x*(num-1+math.ceil((t+num*(task['WCRT']-x))/task['period']))
def Ssatr(task, HPTasks,Q='',q=0):

	if Q == '':
		D=task['period']
		C=task['execution']

		numC=0
		for q in range(len(task['resGraph'])):
			numC+=task['numCritical']
		numC+=1
		
	else:
		D=task['period']
		C=task['resGraph'][q]['totacc']+task['resGraph'][q]['blocking']
		num=task['numCritical']

	return myRTA(C,HPTasks,D,num,Q,q)


		
def Itot(R,task,HPTasks,LPTasks,Thetas,effProc,iproc,procs,MaxWCRTThetas):
	W=0

	for i in range(len(Thetas)):		
		if effProc[i] == True:
			
				A=0
				
				if i==iproc:
					
					for itask in procs[i]:
						x=itask['execution']
						A+=getWinGlobalWCRT(R,x,itask)
					for itask in LPTasks:
						x=0
						for q in Thetas[i]:
							iq=q['which']
							if itask['resGraph'][iq]['totacc']!=0:
								x+= itask['resGraph'][iq]['totacc']
						A+=getWinGlobal(R,x,itask)
	
				for itask in HPTasks:
					x=0
					for q in Thetas[i]:
						iq=q['which']
						if itask['resGraph'][iq]['totacc']!=0:
							x+= itask['resGraph'][iq]['totacc']
					A+=getWinGlobalWCRT(R,x,itask)				
		
				W+=A

	W+=task['execution']
	W+=task['accExecution']
	return W
def elvItot(R,task,HPTasks,LPTasks,Thetas,effProc,iproc,procs,MaxWCRTThetas):
	W=0

	

	for i in range(len(Thetas)):		
		if effProc[i] == True:
			A=0
			if iproc == i:
				
				for iq in Thetas[i]:					
					j=iq['which']	
					if task['resGraph'][j]['totacc']!=0:			
					
						CI=[]
						for itask in LPTasks:
							if itask['resGraph'][j]['totacc'] !=0:
								x=int(itask['resGraph'][j]['totacc']/itask['resGraph'][j]['maxacc'])
								for k in range(x):					
									CI.append(itask['resGraph'][j]['maxacc'])
								CI.append(itask['resGraph'][j]['totacc']-x*itask['resGraph'][j]['maxacc'])
								for k in range(x):					
									CI.append(itask['resGraph'][j]['maxacc'])
								CI.append(itask['resGraph'][j]['totacc']-x*itask['resGraph'][j]['maxacc'])
					
						decWCtasks=heapq.nlargest(task['numCritical'],CI)				
						A+=sum(decWCtasks)
			for itask in procs[i]:
				x=itask['execution']
				A+=getWinGlobalWCRT(R,x,itask)				
			
			for itask in HPTasks:
				x=0
				for q in Thetas[i]:
					iq=q['which']
					if itask['resGraph'][iq]['totacc']!=0:
						x+= itask['resGraph'][iq]['totacc']
				A+=getWinGlobalWCRT(R,x,itask)				
		
			W+=A

	W+=task['execution']
	W+=task['accExecution']
	return W
def IcoreWCRT(R,task,HPTasks,LPTasks,Theta,iproc,procs,iflocal,numss,scheme):
	A=0
	

	
	if iflocal== True:
		for itask in LPTasks:
			x=0
			for q in Theta:
				iq=q['which']
				if itask['resGraph'][iq]['totacc']!=0:
					x+= itask['resGraph'][iq]['totacc']	
			A+=getWinGlobal(R,x,itask)	
		
		for itask in HPTasks:
			x=0
			for q in Theta:
				iq=q['which']
				if itask['resGraph'][iq]['totacc']!=0:
					x+= itask['resGraph'][iq]['totacc']
				
			if itask in procs[iproc]:
				x+=itask['execution']
			

			A+=getWCRTsigma(R,x,itask,numss)	


	else:
		n=0
		for q in Theta:
			iq=q['which']
			if task['resGraph'][iq]['totacc']!=0:
				n+=task['numCritical']
		for itask in HPTasks:
			x=0
			for q in Theta:
				iq=q['which']
				if itask['resGraph'][iq]['totacc']!=0:
					x+= itask['resGraph'][iq]['totacc']
			
			A+=getWCRTsigma(R,x,itask,n)

	return A
def maxCoreWCRT(task,HPTasks,LPTasks,Theta,iproc,procs,iflocal,numss,scheme):
	D=task['period']
	B=0
	if iflocal != True:
		
		n=0
		CI=[]
		for iq in Theta:
			i=iq['which']
			if task['resGraph'][i]['totacc'] !=0:
				n+=task['numCritical']		
			for itask in LPTasks:
				if itask['resGraph'][i]['totacc'] !=0:
					if scheme == 'DPCP' or scheme == 'elvDPCP':											
							if itask['resGraph'][i]['PCPPrio']<=task['resGraph'][i]['basePrio']:
								#tot=10  max=3 -> 3 3 3 1
								x=int(itask['resGraph'][i]['totacc']/itask['resGraph'][i]['maxacc'])
										
								for j in range(x):					
									CI.append(itask['resGraph'][i]['maxacc'])
								CI.append(itask['resGraph'][i]['totacc']-x*itask['resGraph'][i]['maxacc'])
								for j in range(x):					
									CI.append(itask['resGraph'][i]['maxacc'])
								CI.append(itask['resGraph'][i]['totacc']-x*itask['resGraph'][i]['maxacc'])
					elif scheme =='DNP':
						x=int(itask['resGraph'][i]['totacc']/itask['resGraph'][i]['maxacc'])
										
						for j in range(x):					
							CI.append(itask['resGraph'][i]['maxacc'])
						CI.append(itask['resGraph'][i]['totacc']-x*itask['resGraph'][i]['maxacc'])
						for j in range(x):					
							CI.append(itask['resGraph'][i]['maxacc'])
						CI.append(itask['resGraph'][i]['totacc']-x*itask['resGraph'][i]['maxacc'])

		decWCtasks=heapq.nlargest(n,CI)
		B+=sum(decWCtasks)
	
	C=0
	for q in Theta:
		iq=q['which']
		if task['resGraph'][iq]['totacc']!=0:
			C+=task['resGraph'][iq]['totacc']
	if iflocal == True:
		C+=task['execution']
	R=B+C
	while True:	
		I=IcoreWCRT(R,task,HPTasks,LPTasks,Theta,iproc,procs,iflocal,numss,scheme)

		if R>D:
			return R
		if R < I+B+C:
			R=I+B+C	
		else: 
			return R

def getMaxWCRTThetas(task,HPTasks,LPTasks,Thetas,effProc,iproc,procs,scheme):
	
	maxWCRTThetas=[]
	for i in range(len(Thetas)):
		maxWCRTThetas.append(99999999999)
	for i in range(len(Thetas)):
		if effProc[i] == True:
			n=0

			if i == iproc:
				iflocal=True
				for j in range(len(Thetas)):
					if j!=i:
						for iq in Thetas[j]:

							q=iq['which']
							if task['resGraph'][q]['totacc']!=0:
								n+=task['numCritical']
				n+=1
			else:
				iflocal=False
			maxWCRTThetas[i]=maxCoreWCRT(task,HPTasks,LPTasks,Thetas[i],iproc,procs,iflocal,n,scheme)

			
	return maxWCRTThetas

def IcoreTask(R,HPTasks,sigma):
	W=0
	for itask in HPTasks:
		x=itask['execution']
		W+=getWCRTsigma(R,x,itask,sigma)
	return W
def qWorkload(R,HPTasks,q,sigma):
	W=0
	for itask in HPTasks:
		x=itask['resGraph'][q]['totacc']
		W+=getWCRTsigma(R,x,itask,sigma)
	return W
def iTDMARTA(task,HPtasks,D,sigma):
	C=task['execution']
	R=C
	while True:	
		I=IcoreTask(R,HPtasks,sigma)

		if R>D:
			return R
		if R < I+C:
			R=I+C	
		else: 
			return R
def qTDMARTA(task,HPtasks,LPTasks,D,q,serverR):

	C=task['resGraph'][q]['totacc']
	B=0
	CI=[]
	for itask in LPTasks:
		if itask['resGraph'][q]['totacc'] !=0:
			x=int(itask['resGraph'][q]['totacc']/itask['resGraph'][q]['maxacc'])
			for j in range(x):					
				CI.append(itask['resGraph'][q]['maxacc'])
			CI.append(itask['resGraph'][q]['totacc']-x*itask['resGraph'][q]['maxacc'])
			for j in range(x):					
				CI.append(itask['resGraph'][q]['maxacc'])
			CI.append(itask['resGraph'][q]['totacc']-x*itask['resGraph'][q]['maxacc'])
	
	decWCtasks=heapq.nlargest(task['numCritical'],CI)				
	B+=sum(decWCtasks)
	R=C

	while True:	
		I=qWorkload(R,HPtasks,q,task['numCritical'])

		if R>D:
			return R
		if R < (I+C+B)/serverR:

			R=(I+C+B)/serverR

		else: 
			return R
def TDMARTA(task,localHPTasks,HPTasks,LPTasks,D,mTDMA,numQ,LOADA):
	
	
	
	n=0
	for q in task['resGraph']:
		if q['totacc']!=0:
			n+=task['numCritical']
	if n==0:
		print "d"
	X=iTDMARTA(task,localHPTasks,D,n+1)
	for q in range(len(task['resGraph'])):
		if task['resGraph'][q]['totacc']!=0:
			serverR=mTDMA/numQ

			# iLOAD=0
			# for itask in HPTasks+LPTasks:
			# 	iLOAD+=itask['resGraph'][q]['totacc']/itask['period']
			# iLOAD+=task['resGraph'][q]['totacc']/task['period']
		
			# serverR=mTDMA*iLOAD/LOADA
			X+=qTDMARTA(task,HPTasks,LPTasks,D,q,serverR)
	return X
def dualRTA(task,HPTasks,LPTasks,D,Thetas,iproc,procs,scheme):
	R=0
	# Q=[]
		
		
	# for i in range(len(task['resGraph'])):
	# 	Q.append(0)
	# for iTheta in Thetas:
	# 	flag1=False
	# 	for iq in iTheta:
	# 		flag2=False						
	# 		if task['resGraph'][iq['which']]['totacc']!=0:
	# 				flag2=True
	# 				break			
	# 	if flag2 == True:
	# 		for iq in iTheta:
	# 			Q[iq['which']]=1
	effProc=[]
	
	
	for i in range(len(Thetas)):
		effProc.append(0)

	for i in range(len(Thetas)):
				
		if i == iproc:
			effProc[i]=1
			continue
		flag=False
		for iq in Thetas[i]:
			if task['resGraph'][iq['which']]['totacc']!=0 :				
				flag=True
				break

		if flag == True:
			effProc[i]=1

	B=0	

	for iThe in range(len(Thetas)):
		if effProc[iThe] == False:
			continue
		if iThe == iproc:
			continue	
		
		
		for iq in Thetas[iThe]:
			
			i=iq['which']				
			if task['resGraph'][i]['totacc'] !=0:					
				CI=[]
				for itask in LPTasks:
					if itask['resGraph'][i]['totacc'] !=0:
						x=int(itask['resGraph'][i]['totacc']/itask['resGraph'][i]['maxacc'])
						for j in range(x):					
							CI.append(itask['resGraph'][i]['maxacc'])
						CI.append(itask['resGraph'][i]['totacc']-x*itask['resGraph'][i]['maxacc'])
						for j in range(x):					
							CI.append(itask['resGraph'][i]['maxacc'])
						CI.append(itask['resGraph'][i]['totacc']-x*itask['resGraph'][i]['maxacc'])
				
				decWCtasks=heapq.nlargest(task['numCritical'],CI)				
				B+=sum(decWCtasks)
	
	C=task['execution']+task['accExecution']
	#MaxWCRTThetas=[]

	MaxWCRTThetas=getMaxWCRTThetas(task,HPTasks,LPTasks,Thetas,effProc,iproc,procs)
	R=C+B
	

	
	while True:			


		if scheme == 'FED':
			I=Itot(R,task,HPTasks,LPTasks,Thetas,effProc,iproc,procs,MaxWCRTThetas)
		elif scheme == 'elvFED':
			I=elvItot(R,task,HPTasks,LPTasks,Thetas,effProc,iproc,procs,MaxWCRTThetas)
		else:
			sys.exit()
		if R>D:
			return R
		if R < I+B:
			R=I+B		
		else: 
			return R
def DKRTA(C,HPTasks,D):
	
	return C+locRBF(D,HPTasks,tight=True)
def TDMAFFtest(task,localHPTasks,HPTasks,LPTasks,mTDMA,numQ,LOADA):
	D=task['period']

	
	WCRT=TDMARTA(task,localHPTasks,HPTasks,LPTasks,D,mTDMA,numQ,LOADA)
	#WCRT=min(FILLRTA(C,B,localHPTasks,D,''),SUMRTA(C,rho,localHPTasks,D)+B,DKRTA(C,localHPTasks,D)+B)
	
	if  WCRT> task['period']:

		return False
	else:
		task['WCRT']=WCRT
		return True	
def RAStest(task,remoteHPTasks,LPTasks,Thetas,i,procs,scheme):
	D=task['period']
	

	
	WCRT=dualRTA(task,remoteHPTasks,LPTasks,D,Thetas,i,procs,scheme)
	
	#WCRT=min(FILLRTA(C,B,localHPTasks,D,''),SUMRTA(C,rho,localHPTasks,D)+B,DKRTA(C,localHPTasks,D)+B)
	
	if  WCRT> task['period']:

		return False
	else:
		task['WCRT']=WCRT
		return True

def SORAStest(task,localHPTasks,remoteHPTasks):
	D=task['period']
	B=getBlocking2(task,remoteHPTasks)
	task['blocking']=B
	C=task['execution']
	rho=task['rho']
	
	if B+C>D:
		return False
	WCRT=FILLRTA(C,B,localHPTasks,D,'SO')
	if  WCRT > task['period']:
		return False
	else:
		task['WCRT']=WCRT
		return True
def diffRAS(task,localHPTasks,remoteHPTasks):
	D=task['period']
	Sr=getSSA(task,remoteHPTasks,D)
	Sc=getSSC(task,localHPTasks,D,task['rho']-1)
	WCRT=dualRTA(task,localHPTasks,remoteHPTasks,D,'',Sr=Sr,Sc=Sc)
	
	return task['period']-WCRT
def WorstFit(task,procs,scheme,remoteHPTasks):

	maxCProc=[]
	maxRemain=-1
	for iproc in procs:		
		rc=diffRAS(task,iproc,remoteHPTasks)		
		if rc > maxRemain:
			maxCProc=iproc
			maxRemain=rc

	if maxRemain <0:
		return False
	else:
		task['WCRT']=task['period']-maxRemain
		maxCProc.append(task)
		return True
def BestFit(task,procs,scheme,remoteHPTasks):

	CProc=[]
	minRemain=10000000000000
	for iproc in procs:
		
		rc=diffRAS(task,iproc,remoteHPTasks)
		
		if rc < 0:
			continue
		else:
			if rc < minRemain:
				minRemain=rc
				CProc=iproc
	if minRemain == 10000000000000:
		return False
	else:
		task['WCRT']=task['period']-minRemain
		CProc.append(task)
		return True	

def getA(t,HPTasks):
	W=0
	for itask in HPTasks:		
		W+=math.ceil((t+itask['WCRT']-itask['accExecution'])/itask['period'])*itask['accExecution']

	return W
def getJitter(task,HPTasks,D):
	R=task['accExecution']

	while True:		
		A=getA(R,HPTasks)		
		C=math.ceil(R/task['period'])*task['accExecution']
		if R>D:
			return R
		if R < A+C:
			R=A+C			
		else: 
			return R
def getJW(t,HPTasks):
	W=0
	for itask in HPTasks:
		W+=math.ceil((t+itask['Mjitter'])/itask['period'])*itask['execution']
	return W
def getW(t,HPTasks):
	W=0
	for itask in HPTasks:
		W+=math.ceil((t)/itask['period'])*(itask['execution']+itask['accExecution'])
	return W
def MCRTC(C,HPTasks,D):
	R=C
	while True:
		W=getJW(R,HPTasks)
		if R>D:
			return R
		if R < W+C:
			R=W+C			
		else: 
			return R
def TDMAFirstFit(task,procs,HPTasks,LPTasks,mProc,mTDMA,numQ,LOADA):

	for i in range(mProc):	

		if TDMAFFtest(task,procs[i],HPTasks,LPTasks,mTDMA,numQ,LOADA)== True:
				procs[i].append(task)
				return True

	return False
# def FirstFit(task,procs,remoteHPTasks,LPTasks,Thetas,scheme):

# 	for i in range(len(procs)):	
# 		if scheme.split("-")[1] == "FRDFP":			
# 			if FRDFP(task,remoteHPTasks,scheme)== True:
# 				procs[i].append(task)
# 				return True
# 		elif scheme.split("-")[1] == "FRD":
# 			if FRDtest(task,remoteHPTasks,LPTasks,Thetas,i,procs,scheme)== True:
# 				procs[i].append(task)
# 				return True

# 	return False
def WFD(LOADA,Thetas):

	#numNC=0
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
def TDMAFFDM(tasks,mProc,mTDMA,numQ,LOADA):

	procs=[]
	other=[]
	for i in range(int(mProc)):
		proc=[]
		procs.append(proc)
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	

	for i in range(len(sortedTasks)):

		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		
		if TDMAFirstFit(sortedTasks[i],procs,HPTasks,LPTasks,mProc,mTDMA,numQ,LOADA)== False:
			
			return False

		

	return True
def slack_cmp(x):	
	return x['period']-x['S']
def RAM(tasks,M,Thetas,scheme,numQ):

	procs=[]
	other=[]
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
			if FirstFit(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:				
				if FirstFit_SyncProc(sortedTasks[i],syncprocs,HPTasks,LPTasks,Thetas,scheme)== False:
					return False
		else :
			return False
		# if FirstFit(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:

		
		# 	return False

		

	return True
def RTA(task,HPTasks):
	R=task['execution']+task['accExecution']
	AC=task['execution']+task['accExecution']
	D=task['period']
	while True:
		W=getW(R,HPTasks)
		if R>D:
			return R
		if R < W+AC:
			R=W+AC			
		else: 
			return R
def NBFirstFit(task,procs):

	for i in range(len(procs)):	
		WCRT=RTA(task,procs[i])
		if WCRT>task['period']:
			continue
		else:
			procs[i].append(task)
			return True
	return False

def NBFFDMFP(tasks,M,scheme,numQ):
	procs=[]
	other=[]
	for i in range(int(M)):
		proc=[]
		procs.append(proc)
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	

	for i in range(len(sortedTasks)):
		if NBFirstFit(sortedTasks[i],procs)== False:				
				return False


	return True
def NPDBF(tasks,M,scheme,numQ):	
	
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	

	for i in range(len(sortedTasks)):

		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]

		task=sortedTasks[i]
		
		for j in range(len(task['resGraph'])):

			if task['resGraph'][j]['totacc']==0:
				continue
			else:
				
				HPC=0
				for itask in HPTasks:
					if itask['resGraph'][j]['totacc'] !=0:
						#demand before deadline
						HPC+=itask['resGraph'][j]['totacc']*int(task['period']/itask['period'])
				B=0
				CI=[]
				for itask in LPTasks:
					if itask['resGraph'][j]['totacc'] !=0:
							CI.append(itask['resGraph'][j]['maxacc'])
						# pick the maximum one
				decWCtasks=heapq.nlargest(1,CI)				
				B=sum(decWCtasks)
				if (HPC+B+task['resGraph'][j]['totacc'])/task['period']>1:
					return False
def Idsr(R,HPTasks,task):
	W=0
	for itask in HPTasks:
		x=0
		for q in range(len(task['resGraph'])):
			if task['resGraph'][q]['totacc']!=0 and itask['resGraph'][q]['totacc']!=0:
				x+=itask['resGraph'][q]['totacc']
		W+=getWinGlobal(R,x,itask)
	return W
def Insr(R,HPTasks,task):
	W=0
	for itask in HPTasks:
			W+=getWinGlobal(R,itask['execution'],itask)
	return W
def Iosr(R,HPTasks,task):
	W=0
	for itask in HPTasks:
		x=0
		for q in range(len(task['resGraph'])):
			if task['resGraph'][q]['totacc']==0 and itask['resGraph'][q]['totacc']!=0:
				x+=itask['resGraph'][q]['totacc']
		W+=getWinGlobal(R,x,itask)
	return W
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
def Ilp(R,LPTasks,task,k):
	W=0
	for itask in LPTasks:

		x=0
		for q in range(len(task['resGraph'])):
			if itask['resGraph'][q]['totacc']!=0 and itask['resGraph'][q]['PIPPrio']<k:
				x+=itask['resGraph'][q]['totacc']

		W+=getWinGlobal(R,x,itask)
	return W		
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
def DPCPW(R,Gamma,task):
	W=0
	for itask in Gamma:
		if itask['period']< task['period']:
			x=itask['execution']
			W+=getWinGlobal(R,x,itask)
	return W

def PIPPrio(sortedTasks,numQ):
	for q in range(numQ):		
		for i in range(len(sortedTasks)):
			if sortedTasks[i]['resGraph'][q]['totacc']!=0:
				for itask in sortedTasks:
					itask['resGraph'][q]['PIPPrio']=i
				break

def elvIDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc,procs,MaxWCRTThetas):

	W=0
	k=0
	for iThe in range(len(Thetas)):
		if effProc[iThe]== False:
			continue	
		A=0
		for itask in procs[iThe]:
			if itask in HPTasks:			
				x=itask['execution']
				A+=getWinGlobalWCRT(R,x,itask)
		for q in Thetas[iThe]:				
			iq=q['which']			
			for itask in HPTasks:							
				if itask['resGraph'][iq]['totacc']!=0:
					x=itask['resGraph'][iq]['totacc']
					A+=getWinGlobalWCRT(R,x,itask)
		bmax=0
		for q in Thetas[iThe]:
			iq=q['which']			
			for itask in LPTasks:	
				if itask['resGraph'][iq]['totacc']!=0:			
						if itask['resGraph'][iq]['PCPPrio']<=task['resGraph'][iq]['basePrio']:
							if itask['resGraph'][iq]['maxacc']>bmax:
								bmax=itask['resGraph'][iq]['maxacc']

		n=0
		for q in Thetas[iThe]:
			iq=q['which']
			if task['resGraph'][iq]['totacc']!=0:
				n+=task['numCritical']

		A+=n*bmax

		if iThe==iproc:
			A+=task['execution']
		
		for q in Thetas[iThe]:
			iq=q['which']
			if task['resGraph'][iq]['totacc']!=0:
				A+=task['resGraph'][iq]['totacc']

		
		W+=min(A,MaxWCRTThetas[iThe])
		

	return W
def IDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmix=False,The=[]):

	W=0
	scheme1=scheme.split("-")[0]

	for itask in localHPTasks:
		x=itask['execution']
		W+=getWinGlobalWCRT(R,x,itask)
	
	if ifmix == True:
		for q in The:
			for itask in LPTasks:
				if itask['resGraph'][q]['totacc'] != 0:
					x=itask['resGraph'][q]['totacc']
					W+=getWinGlobal(R,x,itask)

	for iThe in Thetas:
		
		if not any(j in task['resEdge'] for j in iThe):
			continue		
		A=0
		for q in iThe:
			for itask in HPTasks:							
				if itask['resGraph'][q]['totacc']!=0:
					x=itask['resGraph'][q]['totacc']
					A+=getWinGlobalWCRT(R,x,itask)
		bmax=getBk(task,LPTasks,iThe,scheme)

		n=0
		for q in iThe:				
			if q in task['resEdge']:
				n+=task['numCritical']
			A+=n*bmax

		for q in iThe:					
			for itask in HPTasks:							
				if itask['resGraph'][q]['totacc']!=0:
					x=itask['resGraph'][q]['totacc']
					A+=getWinGlobalWCRT(R,x,itask)
		
		W+=A
	return W
def RTAEDA(task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,scheme,procs):
	return False
def ROP(task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmax=False,The=[]):
	
	WCRT = RTAROP(task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmax,The)
	
	if WCRT > task['period']:
		return False
	else:
		task['WCRT']=WCRT
		return True
def RTAROP(task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmix,The):	
	
	C=task['execution']+task['accExecution']
	D=task['period']
	R=C


	while True:		
		#I=IDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc)	
		if scheme == 'DPCP' or scheme =='DNP' or scheme == 'DPCP+' or scheme =='DNP+' or scheme.split("-")[0] =='PCP':			
			I=IDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,scheme,ifmix,The)			
		elif scheme == 'elvDPCP' or scheme == 'elvDPCP+':			
			I=elvIDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc,procs,MaxWCRTThetas)			
		else:
			sys.exit()		

		if R>D:
			return R
		if R < I+C:
			R=I+C	
		else: 
			return R
def pIDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc):

	W=0
	k=0
	

	if i == iproc:
		#non-critical
		for itask in localHPTasks:
			x=itask['execution']
			W+=getWinGlobalWCRT(R,x,itask)
		for q in Thetas[iproc]:
			iq=q['which']
			for itask in HPTasks:			
				x=itask['resGraph'][iq]['totacc']
				W+=getWinGlobalWCRT(R,x,itask)
			for itask in LPTasks:			
				x=itask['resGraph'][iq]['totacc']
				W+=getWinGlobal(R,x,itask)
	else:		
		for q in Thetas[i]:				
			iq=q['which']			
			for itask in HPTasks:							
				if itask['resGraph'][iq]['totacc']!=0:
					x=itask['resGraph'][iq]['totacc']
					W+=getWinGlobalWCRT(R,x,itask)

	W+=task['execution']
	W+=task['accExecution']
	return W
def RTAStar(task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,scheme,procs):

	while True:		
		#I=IDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc)	
		if scheme == 'DPCP' or 'DNP':
			I=pIDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc)
		elif scheme == 'elvDPCP':
			I=elvIDPCP(R,task,localHPTasks,HPTasks,LPTasks,Thetas,iproc,effProc,procs)
		else:
			sys.exit()
		

		if R>D:
			return R
		if R < I+B:
			R=I+B		
		else: 
			return R
def FirstFitDPCP(task,procs,HPTasks,LPTasks,Thetas,scheme):

	for i in range(len(procs)):	
		if scheme == 'EDA':
			WCRT=RTAEDA(task,procs[i],HPTasks,LPTasks,Thetas,i,scheme,procs)
		else:
			WCRT=RTADPCP(task,procs[i],HPTasks,LPTasks,Thetas,i,scheme,procs)
		if WCRT>task['period']:
			continue
		else:
			procs[i].append(task)
			task['WCRT']=WCRT
			return True
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
	for iC in task['C']:
		if ifmix == False:
			WCRT.append(FRDFP_RTA(iC,task['period'],HPTasks))
		else:
			WCRT.append(FRDFP_RTA_mix(iC,task['period'],HPTasks,Theta,PrimeTasks))

	if task['S']+sum(WCRT)>task['period']:
		#print task['S'], WCRT,task['period']
		return False
	else:
		WCRT[1]=task['period']-task['S']-WCRT[0]
		task['D']=WCRT
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
def dbf_constrained(C,D,T,t):
	return max(0,C*int((t+(T-D))/T))
def dbf_constrained_apprx(C,D,T,t):
	if t<0:
		print "Oops dbf"
		sys.exit()
	return C*((t+(T-D))/T)
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
def FRDEDF(task,HPTasks,scheme):
	d1=0

	k=int(scheme.split("-")[1].split("=")[2])
	search_scheme=scheme.split("-")[1].split("=")[1]
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
	

def FirstFit(task,procs,HPTasks,LPTasks,Thetas,scheme):

	for i in range(len(procs)):
		canFit=False

		if scheme.split("-")[1] == 'FRDFP':
			canFit=FRDFP(task,procs[i],False)
		elif scheme.split("-")[1].split("=")[0] == 'FRDEDF':
			canFit=FRDEDF(task,procs[i],scheme)		
		elif scheme.split("-")[1] == 'ROP':
			canFit=ROP(task,procs[i],HPTasks,LPTasks,Thetas,scheme)
		else:
			sys.exit()

		if canFit:			
			procs[i].append(task)			
			return True
		else:
			continue
	return False

def setPCP(tasks,numQ):

	for q in range(numQ):
		highestP=-1
		for j in range(len(tasks)):
			if tasks[j]['resGraph'][q]['totacc']!=0:
				highestP=j
				break
		for j in range(len(tasks)):
			tasks[j]['resGraph'][q]['basePrio']=j
			if tasks[j]['resGraph'][q]['totacc']!=0:
				tasks[j]['resGraph'][q]['PCPPrio']=highestP
				
def DPCP(tasks,m,scheme,numQ):
	
	LOADA=[]
	
	for i in range(numQ):
		t=0
		for itask in tasks:

			t+=itask['resGraph'][i]['totacc']/itask['period']
		AJ={}
		AJ['which']=i
		AJ['utilization']=t
		LOADA.append(AJ)

	
	
	for i in range(1,m):
		
		Thetas=[[]for j in range(m)]	
		
		WFD(LOADA,Thetas,i,m-i)

		procs=[]
		
		
		if DPCPFFDM(tasks,m,Thetas,numQ) == True:			
			return True

		
	return False

	
	
def DPCPFFDM(tasks,M,Thetas,numQ):

	procs=[]
	other=[]
	for i in range(int(M)):
		proc=[]
		procs.append(proc)
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	
	setPCP(sortedTasks,numQ)
	for i in range(len(sortedTasks)):		
		if FirstFitDPCP(sortedTasks[i],procs,HPTasks,LPTasks,Thetas)== False:

		
			return False

		

	return True
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
def TDMA(tasks,M,scheme,numQ):

	LOADC=0
	LOADA=0
	for itask in tasks:
		LOADC+=itask['ncriutilization']
	for i in range(numQ):
		
		for itask in tasks:

			LOADA+=itask['resGraph'][i]['totacc']/itask['period']
	
	for m in range(1,M-int(math.ceil(LOADC))+1):
		
		
		
		if TDMAFFDM(tasks,M-m,m,numQ,LOADA) == True:			
			return True

		
	return False
def IWCRTNP(R,tasks):
	W=0
	for itask in tasks:
		x=itask['execution']+itask['accExecution']
		W+=x*math.ceil((R+itask['period'])/itask['period'])
	return W
def WCRTNP(B,C,HPTasks,D):
	R=B+C
	while True:			

		I=IWCRTNP(R,HPTasks)

		if R>D:
			return R
		if R < I+B+C:
			R=I+B+C	
		else: 
			return R
def NPMPFFDMtest(task,HPTasks,B):

	
	C=task['accExecution']+task['execution']
	D=task['period']
	WCRT=WCRTNP(B,C,HPTasks,D)
	if WCRT>D:
		return False
	else:
		return True	

def NPMPFFDM(task,procs,HPTasks,B):

	for i in range(len(procs)):	

		if NPMPFFDMtest(task,procs[i],B)== True:
				procs[i].append(task)
				return True

	return False
def NPMPFF(tasks,M,scheme,numQ):
	procs=[]
	other=[]
	for i in range(int(M)):
		proc=[]
		procs.append(proc)
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	

	B=0
	for itask in sortedTasks:
		if itask['execution']+itask['accExecution']>B:
			B=itask['execution']+itask['accExecution']

	for i in range(len(sortedTasks)):

		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		
		if NPMPFFDM(sortedTasks[i],procs,HPTasks,B)== False:
			
			return False

		

	return True
	
def attract_compare(x, y):
	if x>y:
		return -1
	else:
		return 1
def bap_compare(x, y):
	xsumU=0
	ysumU=0
	if len(x)==1:
		xsumU=x[0]['w']
	else:		
		for itask in x:
			xsumU+=(itask['execution']+itask['accExecution'])/itask['period']


	if len(y)==1:
		ysumU=y[0]['w']
	else:	
		for itask in y:
			ysumU+=(itask['execution']+itask['accExecution'])/itask['period']
	#print xsumU,ysumU
	if xsumU>ysumU:
		return -1
	else:
		return 1
def numeric_compare(x, y):
	xsumU=0
	ysumU=0
	for itask in x:
		xsumU+=(itask['execution']+itask['accExecution'])/itask['period']
	for itask in y:
		ysumU+=(itask['execution']+itask['accExecution'])/itask['period']
	#print xsumU,ysumU
	if xsumU>ysumU:
		return -1
	else:
		return 1
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

def IMPCP(R,HPTasks):
	W=0
	for itask in HPTasks:
		W+=math.ceil((R+itask['MPCP_B'])/itask['period'])*(itask['execution']+itask['accExecution'])
	return W
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
def uniPCPRTA(B,task,HPTasks,D):
	C=task['accExecution']+task['execution']
	R=C
	
	while True:		
		
		I=0
		for itask in HPTasks:			
			I+=math.ceil(R/itask['period'])*(itask['execution']+itask['accExecution'])
		if R>D:
			return R
		if R < I+C+B:
			R=I+C+B		
		else: 
			return R
def ifSchedulable(tasks):
	sortedTasks=sorted(tasks, key=lambda item:item['period'])
	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		B=0
		for q in task['resEdge']:
			for lptask in LPTasks:
				if lptask['resGraph'][q]['totacc']!=0:
					if lptask['resGraph'][q]['maxacc']>B:
						B=lptask['resGraph'][q]['maxacc']
		D=task['period']
		WCRT=uniPCPRTA(B,task,HPTasks,D)
		if WCRT > D:
			return False
		else:
			return True

def MPCP_BAP(tasks,M,scheme,numQ):
	
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
	
	
	sortedTasks=sorted(tasks, key=lambda item:item['period'])

	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		task['basePrio']=i
		att=[]
		for j in range(len(sortedTasks)):
			att.append(0)
		task['attract']=att
		for j in range(len(sortedTasks)):
			if i==j:
				continue 
			elif i<j:
				beta=0
				nc=0
				jtask=sortedTasks[j]
				for q in jtask['resEdge']:
					if task['resGraph'][q]['totacc']!=0:
						nc+=task['numCritical']
						if jtask['resGraph'][q]['maxacc']>beta:
							beta=jtask['resGraph'][q]['maxacc']
				task['attract'][j]=nc*beta*math.ceil(jtask['period']/task['period'])
			else:
				ni=0
				for q in task['resEdge']:
					ni+=task['numCritical']
				beta=0			
				for q in itask['resEdge']:
					if task['resGraph'][q]['totacc']!=0:
						ni+=task['numCritical']
						if itask['resGraph'][q]['maxacc']>beta:
							beta=itask['resGraph'][q]['maxacc']
				task['attract'][j]=ni*beta

	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		w=0

		for itask in HPTasks:
			beta=0
			nc=0
			for q in itask['resEdge']:
				if task['resGraph'][q]['totacc']!=0:
					nc+=task['numCritical']
					if itask['resGraph'][q]['maxacc']>beta:
						beta=itask['resGraph'][q]['maxacc']
			w+=nc*beta*math.ceil(task['period']/itask['period'])
			

		ni=0
		for q in task['resEdge']:
			ni+=task['numCritical']
		for itask in LPTasks:
			beta=0			
			for q in itask['resEdge']:
				if task['resGraph'][q]['totacc']!=0:
					ni+=task['numCritical']
					if itask['resGraph'][q]['maxacc']>beta:
						beta=itask['resGraph'][q]['maxacc']
			w+=ni*beta


		task['w']=task['utilization']+w
	
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
	

	# for iMacro in MacroTasks:
	# 	print len(iMacro)
	Macroprocs=[]
	for i in range(int(M)):
		proc=[]
		Macroprocs.append(proc)

	for itask in tasks:
		if itask['visited']== False:
			MacroTasks.append([itask])
	Mixedlist=[]
	for itaskinMacroTasks in MacroTasks:
		if len(itaskinMacroTasks)==1:
			itaskinMacroTasks[0]['ifBroken']=False
			Mixedlist.append(itaskinMacroTasks[0])
		else:
			if ifSchedulable(itaskinMacroTasks) == True:				
				Mixedlist.append(itaskinMacroTasks)
			else:				
				for itask in itaskinMacroTasks:
					itask['MacroTasks']=itaskinMacroTasks
					itask['ifBroken']=True
					Mixedlist.append(itaskinMacroTasks)
	
	sortedMixedlist=sorted(Mixedlist, cmp=bap_compare)

	for iMacrotask in sortedMixedlist:
		
		if len(iMacrotask) == 1 and iMacrotask[0]['ifBroken']==True:
			sorted(iMacrotask[0]['MacroTasks'], cmp=attract_compare)	
			print "d"
		else:

			ifFind=False		
			for iproc in Macroprocs:
				w=0	
				for jMarcotask in iproc:
					if len(jMarcotask)==1:
						w+=jMarcotask['w']
					else:
						u=0
						for itask in jMarcotask:
							u+=itask['utilization']
						w+=u
				ownw=0
				if len(iMacrotask) == 1:
					ownw=iMacrotask[0]['w']
				else:				
					for jtask in iMacrotask:
						ownw+=jtask['utilization']
				if ownw+w>1:
					continue
				else:
					iproc.append(iMacrotask)
					ifFind=True
					break
			if ifFind==False:
				return False

	procs=[]
	for i in range(int(M)):
		proc=[]
		procs.append(proc)

	for m in range(int(M)):
		for iMacrotask in Macroprocs[m]:						
			for itask in iMacrotask:
				procs[m].append(itask)

	#calculate global priority ceiling 
	for iproc in procs:
		u=0
		for itask in iproc:
			u+=itask['utilization']
		print u
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

		
def MSRPFFDM(tasks,M,scheme,numQ):
	procs=[]
	other=[]
	for i in range(int(M)):
		proc=[]
		procs.append(proc)
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	
	setPCP(sortedTasks,numQ)
	for i in range(len(sortedTasks)):

		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]
		if FirstFitDPCP(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:
			return False
		# if FirstFit(sortedTasks[i],procs,HPTasks,LPTasks,Thetas,scheme)== False:

		
		# 	return False

		

	return True
def Workload(T,C,t):
	return C*math.ceil(t/T)

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
def getBk(task,LPTasks,iTheta,scheme):
	Bk=0
	for itask in LPTasks:
		for iq in iTheta:
			if iq in itask['resEdge']:						
				if scheme.split("-")[0] == 'NPP':
					Bk=max(Bk,itask['resGraph'][iq]['maxacc'])
				elif scheme.split("-")[0] == 'PCP':
					if itask['resGraph'][iq]['PCPPrio']<=task['resGraph'][iq]['basePrio']:
						Bk=max(Bk,itask['resGraph'][iq]['maxacc'])
				else:
					sys.exit()
	return Bk
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


def ReasonableAllocation(tasks,M,scheme,numQ):

	
	LOADA=[]
	
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
		
		WFD(LOADA,Thetas)
		
		if scheme.split("-")[0] == "PCP" or scheme.split("-")[0] == "DPCP":
			setPCP(tasks,numQ)

		if scheme.split("-")[1] == "FRDFP" or scheme.split("-")[1].split("=")[0] == "FRDEDF":
			if calMaxSusp(tasks,Thetas,scheme) == False:
				continue

		if RAM(tasks,M-m,Thetas,scheme,numQ) == True:			
			return True

		
	return False

def Audsley(tasks):
	#Optimal Priority Assignment
	priortyassigned=[0 for i in range(len(tasks))]
	for plevel in range(len(tasks)): 
		canLevel=0
		## check whether task i can be assigned with the priority level plevel
		for i in range(len(tasks)):	
			##ignore lower priority tasks
			if priortyassigned[i]==1:
				continue	
			itask=tasks[i]
			
			## get higher prioirty tasks
			primeTasks=[]
			for j in range(len(tasks)):
				if priortyassigned[j]==0 and i != j:
					primeTasks.append(tasks[j])
			#print "all :",tasks
			#print "task:",itask
			#print "prime:",primeTasks
			#print ""

			
			Tn=itask['period']
			Cn=itask['execution']
			Sn=itask['sslength']	
			
			if sssDT(Cn,Sn,Tn,primeTasks) == True:
				priortyassigned[i]=1
				canLevel=1
				tasks[i]['priority']=len(tasks)-plevel
				break	
		if canLevel == 0:
			#print "fail assign at",plevel 
			return False 
	#print tasks
	return True

