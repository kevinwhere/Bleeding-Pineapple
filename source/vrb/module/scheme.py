from __future__ import division
import random
import math
import json
import sys, getopt
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
def maxU_cmp(x):
	return x['execution']/x['period']

def BBQB(Tasks,Un,Tn):
	taskB=[]
	for itask in Tasks:
		Cmax= max(itask,key=lambda item:item['execution'])['execution']
		Umax=  max(itask,key=maxU_cmp)['execution']/max(itask,key=maxU_cmp)['period']
		pair={}
		pair['beta']=float(Cmax/(Umax*Tn))
		pair['utilization']=Umax
		pair['execution']=Cmax
		taskB.append(pair)
	sortB=sorted(taskB, key=lambda item:item['beta'],reverse =True) 
	print sortB
	sumPart=0
	for i in range(len(sortB)):
		sumPart+=(1+sortB[i]['beta'])*sortB[i]['utilization']

	timePart=0
	for i in range(len(sortB)):
		sumC=0
		for j in range(i,len(sortB)):
			sumC+=sortB[j]['beta']*sortB[j]['utilization']

		timePart+=(sortB[i]['utilization']*sumC)
	print "Un:",Un,"XBUT",1-sumPart+timePart
	if Un>1-sumPart+timePart:
		return False
	return True	



def MixQB(tasks,sumU,Un):
	Stasks=[]
	Vtasks=[]
	for itask in tasks:
		if len(itask) == 1: 
			Stasks.append(itask)
		else:
			Vtasks.append(itask)
	vsumU=0
	vsqtU=0		
	
	for itask in Vtasks:
		Umax=  max(itask,key=maxU_cmp)['execution']/max(itask,key=maxU_cmp)['period']
		vsumU+=Umax
		vsqtU=vsqtU+(Umax**2)
	hyperf=1

	for itask in Stasks:
		U=itask['execution']/itask['period']
		hyperf=hyperf*(1+U)
	
	if Un > ((2/hyperf)-1)-(1+(1/hyperf))*vsumU+0.5*(vsumU**2)+0.5*vsqtU:
		return False
	return True


def BQB(sumU,sqtU,Un,beta):
	print "BQB: sumU, Un, beta, sqrU:",sumU,Un,beta, sqtU
	if Un> 1-(1+beta)*sumU+beta*0.5*(sumU**2)+beta*0.5*sqtU:
		return False
	return True

def UNFITTED(sumU,sqtU):
	return 1-(2)*sumU+0.5*(sumU**2)+0.5*sqtU
def betaCal(Tasks,Tn):		
	beta=[]
	#print PSet
	##-1 exclude the under-test task
	for itask in Tasks:
		Cmax= max(itask,key=lambda item:item['execution'])['execution']
		Umax=  max(itask,key=maxU_cmp)['execution']/max(itask,key=maxU_cmp)['period']
		beta.append(Cmax/(Umax*Tn))
	return max(beta)

def BF(processor,Tasks):
	for iTask in Tasks:
		
		selectP=-1
		for j in xrange(mProc):
			if QB(processor[j]['sum'],processor[j]['sqt'],iTask) == True:
				# select highest capcity
				if  selectP ==-1:
					selectP=j
					continue
				else:
					if UNFITTED(processor[j]['sum'],processor[j]['sqt']) < UNFITTED(processor[selectP]['sum'],processor[selectP]['sqt']):
						selectP=j
				
		if 	selectP!=-1:
			processor[selectP]['sum']=processor[selectP]['sum']+iTask ## 
			processor[selectP]['sqt']=processor[selectP]['sqt']+(iTask**2)
		else:
				return False

	return True
def RM_QB(Tasks):
	## sort by increasing period
	RMTasks=sorted(Tasks, key=lambda item:item['period']) 

	min_delta=100
	for itask in RMTasks:
		if itask['deadline']/itask['period']<min_delta:
			min_delta=itask['deadline']/itask['period']
	max_a=0
	for i in xrange(len(RMTasks)-1):
		if RMTasks[i]['period']/RMTasks[i+1]['period'] > max_a:
			max_a=RMTasks[i]['period']/RMTasks[i+1]['period']
	minQB=100
	for h in xrange(1,len(RMTasks)):
		s=(1-max_a**h)/(1-max_a)
		r=(h-2)*(1/s)
		if r>=1 or min_delta<= (max_a-max_a**h)/(2*(1-r)):
			continue
		Uah=0.5*(h+(max_a**(-h))*s*(min_delta-math.sqrt(max_a**(h+1)+2*r*(max_a**h)*min_delta+min_delta**2)))
		if Uah<minQB:
			minQB=Uah
	for h in xrange(1,len(RMTasks)):
		s=(1-max_a**h)/(1-max_a)
		r=(h-2)*(1/s)
		if min_delta<= 1-max_a**h or min_delta > (-r)*(max_a**h)+math.sqrt((r**2)*(max_a**(2*h))+1-max_a**(h+1)):
			continue
		Ubh=1-0.25*s*(max_a+2*r*(min_delta-1)+(max_a**(-h))*((min_delta-1)**2))
		if Ubh<minQB:
			minQB=Ubh
	U=0
	for itask in RMTasks:
		U+=itask['execution']/itask['period']
	if U > minQB: 
		return False
	else:
		return True

def RB_Bini(task,HPtasks):
	if len(HPtasks) ==0:
		return True
	sumU=0
	for iTask in HPtasks:
		sumU+=(iTask['execution']/iTask['period'])
	sumL=0
	for iTask in HPtasks:
		sumL+=(iTask['execution']*(1-iTask['execution']/iTask['period']))
	Ci=task['execution']
	RB= (Ci+sumL)/(1-sumU)
	#print "BiniRB:",RB
	if RB > task['deadline']:
		return False
	else:
		return True
def EQU_Baruah(task,LTasks,HTasks):

	
	#sorting by decreasing period 
	decTLtasks=sorted(LTasks, key=lambda item:item['period'],reverse=True) 
	
	sumC=task['execution']
	for itask in LTasks:
		sumC+=itask['execution']
	for itask in HTasks:
		sumC+=itask['execution']
	sumU=0
	for itask in decTLtasks:
		sumU+=itask['execution']/itask['period']

	sumL=0
	for i in xrange(len(decTLtasks)):
		sumPartC=0
		for j in xrange(i,len(decTLtasks)):
			sumPartC+=decTLtasks[j]['execution']			
		sumL+=(decTLtasks[i]['execution']/decTLtasks[i]['period'])*sumPartC
	R=(sumC-sumL)/(1-sumU) 	
	
	return R
def EQU_OUR(task,LTasks,HTasks):

	
	#sorting by decreasing period 
	decTLtasks=sorted(LTasks, key=lambda item:item['period'],reverse=True) 
	
	sumC=task['execution']
	for itask in LTasks:
		sumC+=itask['execution']
	for itask in HTasks:
		sumC+=itask['execution']
	sumU=0
	for itask in decTLtasks:
		sumU+=itask['execution']/itask['period']

	sumL=0
	for i in xrange(len(decTLtasks)):
		sumPartC=0
		for j in xrange(i,len(decTLtasks)):
			sumPartC+=decTLtasks[j]['execution']			
		sumL+=(decTLtasks[i]['execution']/decTLtasks[i]['period'])*sumPartC
	R=(sumC-sumL)/(1-sumU) 	
	
	return R
def RB_Baruah(task,HPtasks):

	if len(HPtasks) ==0:
		return True
	sumU=0
	R=task['period']
	C=task['execution']
	#sorting by increasing period 
	incTtasks=sorted(HPtasks, key=lambda item:item['period']) 

	
	#binary serach
	imin=0
	imax=len(incTtasks)-1
	while imax>imin:
		#p := (L + R)/2 bug implemation
		imid=int((imax - imin)/2) + imin
		#print "imid:",imid
		LTasks=incTtasks[:imid+1]
		HTasks=incTtasks[imid+1:]
		#print "All:",incTtasks
		#print "H:",HTasks
		#print "L:",LTasks

		R=EQU_Baruah(task,LTasks,HTasks)
		#print "R:",R
		if R > incTtasks[imid]['period'] :
			imin = imid + 1
		else:
			imax = imid
	#print imin,len(incTtasks)
	LTasks=incTtasks[:imin+1]
	HTasks=incTtasks[imin+1:]
	#print "HL",len(LTasks),len(HTasks)
	RB=EQU_Baruah(task,LTasks,HTasks)
	#print "BaruahRB:",RB
	#print "RB:",RB
	if RB > task['deadline']:
		return False
	else:
		return True

def RB_HP(task,HPtasks):

	prod=1
	for itask in HPtasks:
		prod*=(1+(itask['execution']/min(itask['period'],itask['deadline'])))	
	#prod*=(1+task['execution']/task['deadline'])
	
	#RB=task['execution']/((2/prod)-1)

	if (1+task['execution']/min(task['deadline'],task['period']))*prod>2:
		return False
	else:
		return True	
def RB_OURX(task,HPtasks,M):
	if len(HPtasks) ==0:
		return True
	if boundedTest(task,HPtasks,M) == False:
		return False
	#sorting by decreasing execution
	CI=[]
	for itask in HPtasks:
		#WC=(1+math.ceil((itask['deadline']-itask['execution'])/itask['period']))*itask['execution']
		WC=math.floor(itask['deadline']/itask['period'])*itask['execution']+min(itask['deadline']%itask['period'],itask['execution'])
		CI.append(WC)
	decWCtasks=sorted(CI,reverse=True) 
	#carry-in jobs
	sumCI=0
	##at most M-1 task can be carried in
	##sum the largest M-1
	for i in range(min(M-1,len(decWCtasks))):
		sumCI+=decWCtasks[i]
	sumU=0
	for iTask in HPtasks:
		sumU+=(iTask['execution']/iTask['period'])
	sumC=0
	for iTask in HPtasks:
		sumC+=iTask['execution']*(1-iTask['execution']/iTask['period'])

	sumL=0
	#for iTask in HPtasks:
	#	sumL+=iTask['execution']*(iTask['execution']/iTask['period'])
	Ci=task['execution']
	RB=(Ci+(sumCI+sumC)/M)/(1-sumU/M) 	
	#print "OURRB:",RB
	if RB > task['deadline']:
		return False
	else:
		return True
def boundedTest(task,HPtasks,M):
	sumU=0
	for iTask in HPtasks:
		sumU+=iTask['execution']/iTask['period']
	Ui=task['execution']/task['period']
	if M*Ui+sumU<M:
		return True
	else:
		return False

def RB_OUR(task,HPtasks,M):
	if len(HPtasks) ==0:
		return True

	if boundedTest(task,HPtasks,M) == False:
		return False
	#sorting by decreasing period 
	decTtasks=sorted(HPtasks, key=lambda item:item['period'],reverse=True) 
	
	#sorting by decreasing execution
	CI=[]
	for itask in HPtasks:
		WC=(1+math.ceil((itask['deadline']-itask['execution'])/itask['period']))*itask['execution']
		CI.append(WC)
	decWCtasks=sorted(CI,reverse=True) 
	#carry-in jobs
	sumCI=0
	##at most M-1 task can be carried in
	##sum the largest M-1
	for i in range(min(M-1,len(decWCtasks))):
		sumCI+=decWCtasks[i]
	#carry-in jobs
	

	sumU=0
	for iTask in decTtasks:
		sumU+=(iTask['execution']/iTask['period'])

	sumC=0
	for iTask in decTtasks:
		sumC+=iTask['execution']*(1-iTask['execution']/iTask['period'])
	sumL=0
	for i in xrange(len(decTtasks)):
		sumPartC=0

		for j in xrange(i,len(decTtasks)):
			sumPartC+=decTtasks[j]['execution']
			
		sumL+=(decTtasks[i]['execution']/decTtasks[i]['period'])*sumPartC
	
	Ci=task['execution']
	RB=(Ci+(sumCI+sumC-sumL/M)/M)/(1-sumU/M) 	
	#print "OURRB:",RB
	if RB > task['deadline']:
		return False
	else:
		return True
def diffWcW(t,itask):


	W=itask['execution']*int(t/itask['period'])+min(t%itask['period'],itask['execution'])
	##imprecise Guan's method
	#Wc=itask['execution']*int(max(0,t-itask['execution'])/itask['period'])+itask['execution']+min(max(0,t-itask['execution'])%itask['period'],itask['execution'])
	Wc=itask['execution']*int((t+itask['deadline'])/itask['period'])+min((t+itask['deadline'])%itask['period'],itask['execution'])
	return Wc-W
### Guan's Method
def highPTaskDemandMP(t,HPtasks,M):
	sumNC=0
	for itask in HPtasks:
		sumNC+=itask['execution']*int(t/itask['period'])+min(t%itask['period'],itask['execution'])
	diff=[]
	for itask in HPtasks:
		diff.append(diffWcW(t,itask))
	
	#sorting by decreasing value
	decDiff=sorted(diff,reverse=True) 

	sumMaxDiff=0

	for i in range(min(M-1,len(decDiff))):
		sumMaxDiff+=decDiff[i]
	

	return (sumNC+sumMaxDiff)/M
def VRBL2(mode,Tasks):
	I=0	
	Tn=mode['period']
	for itask in Tasks:
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
		Cmax=max(itask,key=lambda item:item['execution'])['execution']
		I+=Tn*Umax+Cmax*(1-Umax)
	if I+mode['execution']> mode['period']:
		return False
	return True
def Term(task,HPtasks,M):

	V=0
	for itask in HPtasks:
		V+=min(itask['execution']/itask['period'],1-itask['execution']/itask['period'])
	#print "Term False"
	return M-V-M*(task['execution']/task['period'])>0

def RB_GUAN(task,HPtasks,M):

	if len(HPtasks) ==0:
		return True
	
	#print task,HPtasks
	H=1
	Tn=task['period']
	Cn=task['execution']
	maxR=0
	##check busy interval
	while 1:

		R=0
		while True:	

			dm=highPTaskDemandMP(R,HPtasks,M)
			if R> (H-1)*Tn+task['deadline']:
				return False
			if R < dm+H*Cn:

				R=dm+H*Cn
				#print "R:",R
			
			else: 
				break
		RT=R-(H-1)*Tn
		if  RT > maxR:
			maxR=RT


		L=H*Tn
		
		#if cm+H*Cn>(H-1)*Tn+task['deadline']:
		#	return False
		if L>=R:
			break
		else:
			H+=1
		#print "L:",L,"  H:",H	
		
	
	if maxR > task['deadline']:
		return False
	else:
		return True
def DBF(ktask,t):
	
	dbf=ktask['execution']*(math.floor((t-ktask['deadline'])/ktask['period'])+1)
	return max(0,dbf)
def F(Ltasks,t):
	f=0

	for itask in Ltasks:
		#print len(Ltasks)
		#print "DBF:", DBF(itask,t)
		f+=DBF(itask,t)

	return f
def DBF_star(itask,t,n,e):
	u=itask['execution']/itask['period']
	k=int(max(0,math.ceil(n*u/e-itask['deadline']/itask['period'])))
		
	if t<k*itask['period']+itask['deadline']:
		return DBF(itask,t)/t
	else:
		return (itask['execution']+(t-itask['deadline'])*itask['execution']/itask['period'])/t



def LOAD_PTAS(tasks,M):
	e=0.1
	sumU=0
	for itask in tasks:
		sumU+=itask['execution']/itask['period']
	sumLambda=0
	for itask in tasks:
		sumLambda+=itask['execution']/min(itask['period'],itask['deadline'])
	
	n=len(tasks)
	fmax=sumU+e
	times=[]
	if fmax>sumLambda:
		return sumLambda
	for itask in tasks:
		u=itask['execution']/itask['period']
		k=int(max(0,math.ceil(n*u/e-itask['deadline']/itask['period'])))
		for j in xrange(k+1):
			t=itask['period']*j+itask['deadline']
			f=0
			for itask in tasks:
				
				f+=DBF_star(itask,t,n,e)

			if f>fmax:
				fmax=f
				if fmax >=sumLambda:
					return sumLambda
	

	return fmax
def LOADx(task,M):

	e=0.1
	lcm=task['period']
	for itask in HPtasks:
		lcm*=itask['period']
	c=task['execution']
	for itask in HPtasks:
		c+=itask['execution']

	sumU=task['execution']/task['period']
	for itask in HPtasks:
		sumU+=itask['execution']/itask['period']
	maxpd=task['period']-task['deadline']
	for itask in HPtasks:
		if maxpd<itask['period']-itask['deadline']:
			maxpd=itask['period']-itask['deadline']
	sumLambda=task['execution']/min(task['period'],task['deadline'])
	for itask in HPtasks:
		sumLambda+=itask['execution']/min(itask['period'],itask['deadline'])
	limit=min(lcm,c/e,maxpd*sumU/e)
	#print limit
	#limit=lcm
	#fmax=0
	tlist=[]
	fmax=sumU
	for itask in HPtasks:
		j=0
		t=itask['period']*j+itask['deadline']
		while t<limit:
			t=itask['period']*j+itask['deadline']
			f=F(HPtasks,t)
			f+=DBF(task,t)
			f=f/itime
			if f>fmax:
				fmax=f
				limit=min(limit,sumU*maxpd/(fmax-sumU+e))
				if fmax>sumLambda-e:
					return fmax

	return fmax

def RB_LOAD(task,HPtasks,M):
	if len(HPtasks) == 0:
		return True
	L=[]
	for iTask in HPtasks:
		L.append(iTask)
	L.append(task)
	deltamax=0
	for itask in L:
		d=itask['execution']/min(itask['period'],itask['deadline'])
		if d>deltamax:
			deltamax=d
	fmax=LOAD_PTAS(L,M)
	mu=M-(M-1)*(task['execution']/min(task['period'],task['deadline']))
	
	#print "f",2*fmax+(math.ceil(mu)-1)*deltamax," 1:",2*fmax, " 2: ",(math.ceil(mu)-1)*deltamax, " mu: ",mu

	if 2*fmax+(math.ceil(mu)-1)*deltamax<mu:
		return True
	elif fmax<=(M-(M-1)*deltamax)/(1+2):
		return True
	else:
		return False 


def RB_BAK(task,HPtasks,M):

	if len(HPtasks) == 0:
		return True
	u=M*(1-task['execution']/min(task['period'],task['deadline']))
	#print u
	for itask in HPtasks:
		
		ui=M-(itask['execution']/itask['period'])*(M-1)
		beta=0
		for itask in HPtasks:
			if (M-ui)/(M-1) >= itask['execution']/itask['period']:
				temp=(itask['execution']/itask['period'])*(1+(itask['period']-itask['execution'])/itask['deadline'])
				beta+=min(1,temp)
			else:
				temp=(itask['execution']/itask['period'])*(1+(itask['period']-itask['execution'])/itask['deadline'])+(itask['deadline']/task['deadline'])*((itask['execution']/itask['period'])-(M-ui)/(M-1))
				beta+=min(1,temp)
		#print beta
		if beta <= u:
			return True

	return False



def GDM(Tasks,scheme,M):

	## sort by increasing period
	DMTasks=sorted(Tasks, key=lambda item:item['deadline']) 
	#print sortedTasksLM

	for i in xrange(len(DMTasks)):
		
		#reverse test
		#i=len(DMTasks)-j-1
		

		HPTasks=DMTasks[:i]
		#print HPTasks	
		if 	scheme == 'OUR-LP':
			if RB_OUR(DMTasks[i],DMTasks[:i],M)==False:
				return False
		elif 	scheme == 'OUR':
			if RB_OURX(DMTasks[i],DMTasks[:i],M)==False:
				return False
		elif 	scheme == 'Guan':
			if RB_GUAN(DMTasks[i],DMTasks[:i],M)==False:
				return False
		elif 	scheme == 'BAK':
			if RB_BAK(DMTasks[i],DMTasks[:i],M)==False:
				return False	
		elif 	scheme == 'LOAD':
			if RB_LOAD(DMTasks[i],DMTasks[:i],M)==False:
				return False		
		else:
			print "undefined scheme"
			sys.exit(2)
	return True

def RB(Tasks,scheme,M):
	#print sortedTasksLM
	for j in xrange(len(Tasks)):
		
		HPTasks=Tasks[:i]
		#print HPTasks	
		if 	scheme == 'Bini':
			if RB_Bini(Tasks[i],Tasks[:i])==False:
				return False
		elif scheme == 'OUR':
			if RB_OUR(Tasks[i],Tasks[:i],M)==False:
				return False
		elif scheme == 'HP':
			if RB_HP(Tasks[i],Tasks[:i])==False:
				return False
		elif scheme == 'Baruah':
			if RB_Baruah(Tasks[i],Tasks[:i])==False:
				return False
		elif scheme == 'RTA':
			if RTA(Tasks[i],Tasks[:i])==False:
				return False
		else:
			print "undefined scheme"
			sys.exit(2)
	return True
		


def highPTaskDemand(R,tasks):
	sumDM=0
	for itask in tasks:
		sumDM+=itask['execution']*math.ceil(R/itask['period'])
	return sumDM

def RTA(task,HPtasks):
	if len(HPtasks) ==0:
		return True
	#print task,HPtasks
	H=1
	Tn=task['period']
	Cn=task['execution']
	##check busy interval
	while 1:
		L=H*Tn
		if L> H*Cn+highPTaskDemand(L,HPtasks):
			break
		else:
			H+=1
	
	maxR=0
	for i in xrange(1,H+1):
		R=0
		while True:		
			dm=highPTaskDemand(R,HPtasks)
			if R != dm+i*Cn:

				R=dm+i*Cn
				#print "R:",R
			
			else: 
				break
		RT=R-(i-1)*Tn
		if  RT > maxR:
			maxR=RT
	#print "RTARB:",maxR
	if maxR > task['deadline']:
		return False
	else:
		return True
	
	
			
			


def maxU_cmp(x):
	return x['execution']/x['period']

# ## sort by increasing periods
# sortedTasks=sorted(tasks, key=lambda item:item['period']) 
# print sortedTasks

# sumE=0
# sumEB=0
# for i in xrange(len(sortedTasks)):
# 	result=0
# 	HPTasks=sortedTasks[:i]
# 	#print HPTasks
# 	Ci=sortedTasks[i]['execution']

# 	RT=RTA(Ci,HPTasks)
# 	UB=0
# 	if selectUT == 'BINI':
# 		UB=Bini(Ci,HPTasks)
# 	elif selectUT == 'QB':
# 		decPHPTasks=sorted(HPTasks, key=lambda item:item['period'],reverse=True) 
# 		print decPHPTasks
# 		UB=QB(Ci,decPHPTasks)
# 	else:
# 		 assert selectUT, "selectUT is undefined"
# 	UB=Bini(Ci,HPTasks)
# 	decPHPTasks=sorted(HPTasks, key=lambda item:item['period'],reverse=True) 
	
# 	QUB=QB(Ci,decPHPTasks)

# 	print RT, UB, QUB
# 	sumE+=(UB-RT)/RT
# 	sumEB+=(QUB-RT)/RT
# if selectUT == 'BINI':
# 	print "Err",sumE/len(sortedTasks)
# if selectUT == 'QB':
# 	print "Err",sumEB/len(sortedTasks)
def U_cmp(x):
	return x['execution']/x['period']

def modeQT(mode,tasks):

	HPtasks=[]

	for itask in tasks:
		modesTask=[]
		ifmode=0
		for imode in itask:	
			if imode == mode:
				ifmode=1
				break
		if ifmode==1:
			continue
		for imode in itask:			
			if imode['ifassigned']==True:
				continue			
			modesTask.append(imode)
		if len(modesTask)!=0:
			HPtasks.append(modesTask)

	if len(HPtasks)==0:
		return True
	
	taskB=[]

	

	for itask in HPtasks:
		Cmax= max(itask,key=lambda item:item['execution'])['execution']
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
		pair={}
		pair['beta']=float(Cmax/(Umax))
		pair['utilization']=Umax
		pair['execution']=Cmax
		taskB.append(pair)
	sumC=0
	for itask in taskB:
		sumC+=itask['execution']
	if sumC+mode['execution']>mode['period']:
		return False

	#sorting by decreasing period (beta)
	sortB=sorted(taskB, key=lambda item:item['beta'],reverse =True) 
	#print sortB

	
	timePart=0
	for i in range(len(sortB)):
		t_star=mode['period']
		for j in range(i,len(sortB)):
			t_star-=sortB[j]['execution']

		timePart+=(sortB[i]['utilization']*t_star)
	
	if mode['execution']+sumC+timePart>mode['period']:
		return False
	return True	
def RMQT(tasks,scheme):

	for i in range(len(tasks)):
		itask=tasks[i]
		for imode in itask:
			Tn=imode['period']
			Un=imode['execution']/imode['period']
			primeTasks=[]	
			
			for j in range(len(tasks)):
				if j != i:
					jtask=[]
					for jmode in tasks[j]:							
						if jmode['period'] <= Tn:
							jtask.append(jmode)
					if len(jtask)!=0 :
						primeTasks.append(jtask)	
			
			if len(primeTasks) ==0:
				continue
			if QT(imode,primeTasks) == False:				
				return False
	return True
def QT(mode,HPTasks):
	Tn=mode['period']
	taskB=[]
	for itask in HPTasks:
		Cmax= max(itask,key=lambda item:item['execution'])['execution']
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
		pair={}
		pair['beta']=float(Cmax/(Umax*Tn))
		pair['utilization']=Umax
		pair['execution']=Cmax
		taskB.append(pair)
	#sorting by decreasing period (beta)
	sortB=sorted(taskB, key=lambda item:item['beta'],reverse =True) 
	#print sortB
	sumPart=0
	for i in range(len(sortB)):
		sumPart+=(1+sortB[i]['beta'])*sortB[i]['utilization']

	timePart=0
	for i in range(len(sortB)):
		sumC=0
		for j in range(i,len(sortB)):
			sumC+=sortB[j]['beta']*sortB[j]['utilization']

		timePart+=(sortB[i]['utilization']*sumC)
	#print "Un:",Un,"XBUT",1-sumPart+timePart
	if mode['execution']/mode['period']>1-sumPart+timePart:
		return False
	return True	
def DTest(k,tasks,mode,priortyassigned):

	summaxC=0
	Tn=mode['period']
	Cn=mode['execution']
	
	for i in range(len(tasks)):
		if i != k and priortyassigned[i] == 0:
			summaxC+= max(tasks[i],key=lambda item:item['execution'])['execution']
	tST=0
	if summaxC+Cn>Tn:
		return False

	while 1: 	
		dpsumC=0
		
	 	for i in range(len(tasks)):
	 		if i != k and priortyassigned[i] == 0:
	 			dpsumC+=countInt(i,tasks,int(math.ceil(tST)))
	 	
	 	nextt=dpsumC+summaxC+Cn
	 	#print "Tn, tST,sum, dpsumC,summaxC,Cn",Tn,tST,nextt,dpsumC,summaxC,Cn
	 	

	 	if nextt >tST:
	 		if nextt>Tn:					 			
	 			return False
	 		else: 
	 			tST=nextt	
	 			
	 	else:	 		
	 		return True
dpTasks=[] 
dirtyBit=[]
def dp_recursive(t,dpTB,dirtTB,incM,idptask,tasks):
	choice=[]

	if t ==0:
		dirtTB[0]=0
		dpTB[t]=0

	if dirtTB[t]==0:
		return dpTB[t]

	for i in range(incM):
		imode=tasks[idptask][i]
		if imode['period']<=t:
			## dp table look one time unit behind when float
			## safe
			choice.append(dp_recursive(t-int(imode['period']),dpTB,dirtTB,incM,idptask,tasks)+imode['execution'])
		else:
			choice.append(0)

		dirtTB[t]=0
		dpTB[t]=max(choice)
	return dpTB[t]
def countInt(idptask,primeTasks,Tn):
	#print "he",primeTasks[idptask]
	if len(primeTasks[idptask]) == 0:
	 	countI=0
	elif len(primeTasks[idptask]) == 1:
		if Tn==0:
			countI=0
		else:			
	 		countI=math.floor(Tn/primeTasks[idptask][0]["period"])*primeTasks[idptask][0]["execution"]
	else:
	 	
		incM=len(primeTasks[idptask]) ## table needed only for len >=2 
		idp=incM-2

		if len(dpTasks[idptask][idp]) <= (int(Tn)+1):
			dp=[-1 for i in range(int(Tn)+1-len(dpTasks[idptask][idp]))]
			dirt=[-1 for i in range(int(Tn)+1-len(dpTasks[idptask][idp]))]
			#print dpTasks[idptask][incM]
			#print dp
			dpTasks[idptask][idp]=dpTasks[idptask][idp]+dp
			dirtyBit[idptask][idp]=dirtyBit[idptask][idp]+dirt
		
	 	## dp table look one time unit behind when float
		## safe		
		dpTB=dpTasks[idptask][idp]
		dirtTB=dirtyBit[idptask][idp]	

	 	countI=dp_recursive(int(Tn),dpTB,dirtTB,incM,idptask,primeTasks) 

	return  countI
def table_init(tasks):	
	for i in range(len(tasks)):
		incM=[]
		incMdirt=[]
		dpTasks.append(incM)
		dirtyBit.append(incMdirt)
		## table needed only for len >=2 
		for j in range(len(tasks[i])-1):
			dp=[]
			dirt=[]
			dpTasks[i].append(dp)
			dirtyBit[i].append(dirt)

def dpDBF(t,itask,DBFTable):

	if DBFTable[t] == -1:
		maxDBF=0
		for imode in itask:
			if imode['ifassigned'] == False and t>imode['period']:
				current_dbf = imode['execution']+dpDBF(int(math.ceil(t-imode['period'])),itask,DBFTable)
				if current_dbf > maxDBF:
					maxDBF=current_dbf
		DBFTable[t]=maxDBF
		
		return DBFTable[t]
	else:
		return DBFTable[t]
def WCRTvrb(mode,tasks):
	T=mode['period']
	C=mode['execution']
	
	pronedTasks=[]
	for itask in tasks:

		CMax=0
		for imode in itask:
			if imode['ifassigned'] == False:
				if imode['execution'] > CMax:
					CMax = imode['execution']
		C+=CMax
		if CMax!=0:
			pronedTasks.append(itask)
	R=C
	dpDBFTables = []
	for itask in pronedTasks:
		dpDBFTables.append([-1 for i in range(int(T+1))])
	
	while True:
		
		if R>T:
			return R
		W=0
		#print dpDBFTables
		for i in range(len(pronedTasks)):
			W+=dpDBF(int(math.ceil(R)),pronedTasks[i],dpDBFTables[i])
		

		if R < W+C:
			R=W+C			
		else: 
			return R
def vrbDP(mode,tasks):

	WCRT=WCRTvrb(mode,tasks)
	if WCRT > mode['period']:
		return False
	else:
		return True
	
def modeAudsley(tasks,scheme):

	#Optimal Priority Assignment
	num_modes=0
	for itask in tasks:
		num_modes+=len(itask)
		for imode in itask:
			imode['ifassigned']=False
	
	#priortyassigned=[0 for i in range(len(tasks))]
	for plevel in range(num_modes):
	
		## check whether task i can be assigned with the priority level plevel
		canAssign=0
		for i in range(len(tasks)):
			primeTasks=tasks[:i]+tasks[i+1:]		

			for imode in tasks[i]:
				##ignore lower priority tasks
				if imode['ifassigned']==True:
					continue

				if scheme == 'QT-OPA':
					if modeQT(imode,primeTasks):							
						continue
					else:					
						imode['ifassigned']=True
						canAssign=1
						break
				elif scheme == 'DP-OPA':
					if vrbDP(imode,primeTasks) == False:							
						continue
					else:
						imode['ifassigned']=True
						canAssign=1
						break
				else:
					sys.exit(1)
			if canAssign==1:
				break

		if canAssign==0:

			return False
	return True

def Audsley(tasks,scheme):
	if scheme == 'DT-FPT':
		table_init(tasks)
	

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
			canAssign=1

			## get higher prioirty tasks
			primeTasks=[]
			for j in range(len(tasks)):
				if priortyassigned[j]==0 and i != j:
					primeTasks.append(tasks[j])
			#print "all :",tasks
			#print "task:",itask
			#print "prime:",primeTasks
			#print ""
			if len(primeTasks) ==0:
				priortyassigned[i]=1
				canLevel=1
				#print "assign success at",i
				break

			## check feasiability of all modes
			for imode in itask:
				Tn=imode['period']
				Un=imode['execution']/imode['period']
				if scheme == 'QT-FPT':

					if QT(imode,primeTasks) == False:
						canAssign=0
						break
				elif scheme == 'VRBL2-FPT':
					if VRBL2(imode,primeTasks) == False:
						canAssign=0
						break
				elif scheme == 'DT-FPT':
					if DTest(i,tasks,imode,priortyassigned) == False:
						canAssign=0
						break				
				else:
					sys.exit(0)
					
			if canAssign == 1:
				priortyassigned[i]=1
				canLevel=1
				#print "assign success at",i
				break

		if canLevel == 0:
			return False
	return True

	


		