from __future__ import division
import math
import sys




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
	
