from __future__ import division
import random
import math
import json
import sys, getopt
maxmaxP=[]
rfile=""
ifFPT=0
selectUT=0 ## UT:0 BUT:1 MixUT:2

def parameterRead():
	global rfile,selectUT,ifFPT
	try:
		opts, args = getopt.getopt(sys.argv[1:],"ho:s:x:")
	except getopt.GetoptError:
		print 'test.py -i <seed> -u <totalutilzation> -if <scalefactor> -x <FPT>'
		sys.exit(2)
	print opts, args
	
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <randoseed> -u <totalutilzation> -f <scalefactor> -x <FPT>'
			sys.exit()		
		elif opt in ("-o", "--output"):
			rfile = arg
		elif opt in ("-s", "--select"):
			selectUT = arg
		elif opt in ("-x", "--FPT"):
			ifFPT = int(arg)
		else:
			assert False, "unhandled option"
def U_cmp(x):
	return x['execution']/x['period']
def dp_recursive(t,dpTB,dirtTB,incM,idptask):
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
			choice.append(dp_recursive(t-int(imode['period']),dpTB,dirtTB,incM,idptask)+imode['execution'])
		else:
			choice.append(0)

		dirtTB[t]=0
		dpTB[t]=max(choice)
	return dpTB[t]
def countInt(idptask,primeTasks,Tn):
	print "he",primeTasks[idptask]
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

	 	countI=dp_recursive(int(Tn),dpTB,dirtTB,incM,idptask) 

	return  countI	
#3d list
#1:task,2:gamma,3:t
dpTasks=[] 
dirtyBit=[]
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
def DTest(k,tasks,Un,Tn,priortyassigned):

	summaxC=0
	
	Cn=Un*Tn
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
	 	print "Tn, tST,sum, dpsumC,summaxC,Cn",Tn,tST,nextt,dpsumC,summaxC,Cn
	 	

	 	if nextt >tST:
	 		if nextt>Tn:					 			
	 			return False
	 		else: 
	 			tST=nextt	
	 			
	 	else:
	 		print "schedulable!",tST
	 		return True
def VRBL2(Tasks,Un,Tn):
	I=0	
	Cn=Un*Tn
	for itask in Tasks:
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
		Cmax=max(itask,key=lambda item:item['execution'])['execution']
		I+=Tn*Umax+Cmax*(1-Umax)
	if I+Cn> Tn:
		return False
	return True

def UTest(Tasks,Un,Tn):
	
	sumC=0
	if ifFPT:
		for itask in Tasks:
			sumC+=max(itask,key=lambda x: x['execution'])['execution']
		
		if sumC+Tn*Un > Tn:
			print "sumC Fail"
			return False	

		if selectUT == 'FPTQB':
			if BBQB(Tasks,Un,Tn) == False:
				return False
			else:
				return True
		elif selectUT == 'DTP':
			assert "sss"
		elif selectUT == 'FPTVRBL2':
			if VRBL2(Tasks,Un,Tn) == False:
				return False
			else:
				return True		
		else :
			return False


	else:
		if selectUT == 'RMQB':
			if QB(Tasks,Un) == False:
				return False
			else:
				return True	
		
		elif selectUT == 'RMQBP':
			#beta=betaCal(Tasks,Tn)
			if BBQB(Tasks,Un,Tn) == False:
				return False
			else:
				return True

	


def BBQB(Tasks,Un,Tn):


	taskB=[]
	for itask in Tasks:
		Cmax= max(itask,key=lambda item:item['execution'])['execution']
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
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






def BQB(sumU,sqtU,Un,beta):
	print "BQB: sumU, Un, beta, sqrU:",sumU,Un,beta, sqtU
	if Un> 1-(1+beta)*sumU+beta*0.5*(sumU**2)+beta*0.5*sqtU:
		return False
	return True
def QB(Tasks,Un):
	sumU=0
	sqtU=0	
	for itask in Tasks:
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
		sumU+=Umax
		sqtU+=(Umax**2)
	print "QB: sumU, Un,sqtU:",sumU,Un, sqtU
	if Un> 1-2*sumU+0.5*(sumU**2)+0.5*sqtU:
		return False
	return True
def betaCal(Tasks,Tn):		
	beta=[]
	#print PSet
	##-1 exclude the under-test task
	for itask in Tasks:
		Cmax= max(itask,key=lambda item:item['execution'])['execution']
		Umax=  max(itask,key=U_cmp)['execution']/max(itask,key=U_cmp)['period']
		beta.append(Cmax/(Umax*Tn))
	return max(beta)
def QBLT(tasks):
	sumU=0
	
	minU=1
	taskC=[]
	index=0
	
	for i in xrange(len(tasks)):		
		Umax=max(tasks[i],key=U_cmp)['execution']/max(tasks[i],key=U_cmp)['period']
		
		sumU+=Umax
		if Umax < minU:
			minU=Umax
			index=i
	print sumU
	for i in xrange(len(tasks)):
		if i != index:			
			taskC.append(tasks[i])
	
	return QB(taskC,minU) 

parameterRead()
fi = open(rfile, "r")
#fi = open("golden.txt", "r")
tasks= json.load(fi)
fi.close()
##dp
table_init(tasks)
		
if ifFPT:
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
			print "all :",tasks
			print "task:",itask
			print "prime:",primeTasks
			print ""
			if len(primeTasks) ==0:
				priortyassigned[i]=1
				canLevel=1
				print "assign success at",i
				break

			## check feasiability of all modes
			for imode in itask:
				Tn=imode['period']
				Un=imode['execution']/imode['period']
				if selectUT == 'DTP':
					if DTest(i,tasks,Un,Tn,priortyassigned) == False:
						canAssign=0
						break
				else:
					if UTest(primeTasks,Un,Tn) == False:
						canAssign=0
						break
			if canAssign == 1:
				priortyassigned[i]=1
				canLevel=1
				print "assign success at",i
				break

		if canLevel == 0:
			print "fail assign at",plevel 
			break


else:

	if selectUT == 'RMQBL':
		if QBLT(tasks) == False:
			print "fail"
		sys.exit()

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
	
			print "all :",tasks
			print "test Mode:",imode
			print "task:",itask
			print "prime:",primeTasks
			print ""
			if len(primeTasks) ==0:
				continue
			if UTest(primeTasks,Un,Tn) == False:
				print "fail"
				sys.exit()
	



	
