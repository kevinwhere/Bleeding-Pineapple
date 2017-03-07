from __future__ import division
import random
import math
import tests

def modeAudsley(tasks,scheme):

	## to know how many priority levels we need to decide
	num_modes=0
	for itask in tasks:
		num_modes+=len(itask)		
		for imode in itask:
			## put an attribute for each mode used as an indicator for whether or not its priority level is assigned
			imode['ifassigned']=False
	
	### assign priority levels to modes, from the lowerest to the highest
	for plevel in range(num_modes):
	
		## check whether task i can be assigned with the priority level plevel
		canAssign=0
		for i in range(len(tasks)):
			primeTasks=tasks[:i]+tasks[i+1:]		

			for imode in tasks[i]:
				##ignore modes whose priority levels have been decided
				if imode['ifassigned']==True:
					continue


				## checking if this mode can be assigned to this priority level by QT test
				if tests.modeQT(imode,primeTasks):							
					continue
				else:					
					imode['ifassigned']=True
					canAssign=1
					break
				
			## greedily assign the first mode feasible to this priority level
			if canAssign==1:
				break
		## if none of the modes can be assigned at this priority level, return unscheduable
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

					if tests.QT(imode,primeTasks) == False:
						canAssign=0
						break
				elif scheme == 'VRBL2-FPT':
					if tests.VRBL2(imode,primeTasks) == False:
						canAssign=0
						break
				elif scheme == 'DT-FPT':
					if tests.DTest(i,tasks,imode,priortyassigned) == False:
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

	


		