from __future__ import division
import random
import math
import json
import sys, getopt
maxmaxP=[]
rfile=""
sys.setrecursionlimit(5000)

def parameterRead():
	global rfile
	try:
		opts, args = getopt.getopt(sys.argv[1:],"ho:")
	except getopt.GetoptError:
		print 'test.py -i <seed> -u <totalutilzation> -if <scalefactor>'
		sys.exit(2)
	print opts, args
	
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <randoseed> -u <totalutilzation> -f <scalefactor>'
			sys.exit()		
		elif opt in ("-o", "--output"):
			rfile = arg
		else:
			assert False, "unhandled option"
			
def maxU_cmp(x):
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
			choice.append(dp_recursive(int(t-imode['period']),dpTB,dirtTB,incM,idptask)+imode['execution'])
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

def DTest(tasks,Un,Cn,Tn):

	summaxC=0
	sumU=0
	for itask in tasks:
		if len(itask) != 0:
			sumU+= max(itask,key=maxU_cmp)['execution']/max(itask,key=maxU_cmp)['period']
	for itask in tasks:
		if len(itask) != 0:
			summaxC+= max(itask,key=lambda item:item['execution'])['execution']
	tST=0

	while 1: 	
		dpsumC=0
	
	 	for idptask in range(len(tasks)):	 		
	 		dpsumC+=countInt(idptask,tasks,tST)
	 	
	 	nextt=dpsumC+summaxC+Cn
	 	print "Tn, tST,sum, dpsumC,summaxC,Cn",Tn,tST,nextt,dpsumC,summaxC,Cn
	 	if nextt >tST:
	 		if nextt>Tn:					 			
	 			return False
	 		else: 
	 			tST=int(math.ceil(nextt))			
	 			
	 	else:
	 		print "schedulable!",tST
	 		return True
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
parameterRead()
fi = open(rfile, "r")
#fi = open("golden.txt", "r")
tasks= json.load(fi)

fi.close()
table_init(tasks)


for i in range(len(tasks)):
	itask=tasks[i]
	for imode in itask:
		Tn=imode["period"]
		Un=imode["execution"]/imode["period"]
		Cn=imode["execution"]
		primeTasks=[]
		for j in range(len(tasks)):
			if j != i:
				jtask=[]
				for jmode in tasks[j]:
					if jmode["period"] <= Tn:
						jtask.append(jmode)	
			else:
				jtask=[]
			
			primeTasks.append(jtask)
		print "all :",tasks
		print "test Mode:",imode
		print "task:",itask
		print "prime:",primeTasks
		print ""
		
		if DTest(primeTasks,Un,Cn,Tn) == False:
			print "fail"
			sys.exit()


	
