from __future__ import division
import math
dpTasks=[] 
dirtyBit=[]

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