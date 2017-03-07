from __future__ import division
import math
import sys
maxmaxP=[]
rfile=""

selectUT=""
mProc=1
Cn=1


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


####################################################################################

## Response Time Analysis is not working for the case without critical instant

####################################################################################
# def dpDBF(t,itask,DBFTable):

# 	if DBFTable[t] == -1:
# 		maxDBF=0
# 		for imode in itask:
# 			if imode['ifassigned'] == False and t>imode['period']:
# 				current_dbf = imode['execution']+dpDBF(int(math.ceil(t-imode['period'])),itask,DBFTable)
# 				if current_dbf > maxDBF:
# 					maxDBF=current_dbf
# 		DBFTable[t]=maxDBF
		
# 		return DBFTable[t]
# 	else:
# 		return DBFTable[t]
# def WCRTvrb(mode,tasks):
# 	T=mode['period']
# 	C=mode['execution']
	
# 	pronedTasks=[]
# 	for itask in tasks:

# 		CMax=0
# 		for imode in itask:
# 			if imode['ifassigned'] == False:
# 				if imode['execution'] > CMax:
# 					CMax = imode['execution']
# 		C+=CMax
# 		if CMax!=0:
# 			pronedTasks.append(itask)
# 	R=C
# 	dpDBFTables = []
# 	for itask in pronedTasks:
# 		dpDBFTables.append([-1 for i in range(int(T+1))])
	
# 	while True:
		
# 		if R>T:
# 			return R
# 		W=0
# 		#print dpDBFTables
# 		for i in range(len(pronedTasks)):
# 			W+=dpDBF(int(math.ceil(R)),pronedTasks[i],dpDBFTables[i])
		

# 		if R < W+C:
# 			R=W+C			
# 		else: 
# 			return R
# def vrbDP(mode,tasks):

# 	WCRT=WCRTvrb(mode,tasks)
# 	if WCRT > mode['period']:
# 		return False
# 	else:
# 		return True
	
