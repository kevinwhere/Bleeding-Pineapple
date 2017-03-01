from __future__ import division
import random
import math
import json

maxmaxP=[]
dpTasks=[]
fi = open("taskset.txt", "r")
#fi = open("golden.txt", "r")
tasks= json.load(fi)

maxmaxP=tasks[len(tasks)-1]
del tasks[len(tasks)-1]
# for itask in tasks:		
# 	maxP= max(itask,key=lambda item:item['period'])
# 	print maxP
# 	maxmaxP.append(maxP['period'])
Tn= int(max(maxmaxP,key=lambda item:item['period'])['period'])
print Tn
print tasks
for itask in tasks:
	dp=[float(0)]*(Tn+1)
	t=0
	tArray=[]
	while 1:
		perV=dp[t]
		#print "time point:",t
		for imode in itask:	
			if len(tArray)!=0:
				if t+int(imode['period']) > Tn and tArray[len(tArray)-1]>=Tn:
					continue

			if len(tArray)==0:
				tArray.append(int(imode['period']))
			else:
				if t+int(imode['period'])< tArray[0]:
					tArray.insert(0,t+int(imode['period']))
				elif t+int(imode['period'])> tArray[len(tArray)-1]:
						tArray.insert(len(tArray),t+int(imode['period']))				
				else:
					for j in range(1,len(tArray)):
						if t+int(imode['period'])> tArray[j-1] and t+int(imode['period'])< tArray[j]:				
							tArray.insert(j,t+int(imode['period']))	
			#print tArray

		nextT=tArray.pop(0)
		
		if nextT <= Tn:	
			while t<nextT:
				if t<=Tn:
					dp[t]=perV
				t+=1	
				
			for imode in itask:
				if imode['period'] <= t:
					if dp[t]<=dp[t-int(imode['period'])]+imode['execution']:
						dp[t]=dp[t-int(imode['period'])]+imode['execution']
		else:
			while t<nextT:
				if t<=Tn:
					dp[t]=perV
				t+=1
			break
		#print dp

	dpTasks.append(dp)

summaxC=0
for itask in tasks:
	summaxC+= max(itask,key=lambda item:item['execution'])['execution']
tST=0
print "sum",summaxC
while 1: 	
	dpsumC=0
 	for idp in dpTasks: 
 		dpsumC+=idp[int(tST)]
 	if dpsumC+summaxC+max(maxmaxP,key=lambda item:item['period'])['execution'] >tST:

 		next=dpsumC+summaxC+max(maxmaxP,key=lambda item:item['period'])['execution'] 
 		tST=math.ceil(next)
 		if tST>Tn:
 			print "fail!"
 			break
 		else: 					
 			print tST
 	else:
 		print "schedulable!",tST
 		#print dpTasks
 		break




	
fi.close()