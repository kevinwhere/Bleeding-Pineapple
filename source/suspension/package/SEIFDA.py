from __future__ import division
import math
from functions import *
def dbf1(task,t,d):
	return int((t+task['period']-d)/task['period'])*task['Cseg'][0]+int(t/task['period'])*task['Cseg'][1]
def dbf2(task,t,d):
	return int((t+d+task['sslength'])/task['period'])*task['Cseg'][1]+int((t+task['sslength'])/task['period'])*task['Cseg'][0]
def dbf1FPTAS(task,t,d,k):

	if t>=(k-1)*task['period']+d:
		return t*(task['Cseg'][0]+task['Cseg'][1])/task['period']-d*task['Cseg'][0]/task['period']+task['Cseg'][0]
	else:
		return dbf1(task,t,d)
def dbf2FPTAS(task,t,d,k):

	if t>=(k-1)*task['period']+task['period']-task['sslength']-d:
		return (t+task['sslength'])*(task['Cseg'][0]+task['Cseg'][1])/task['period']+d*task['Cseg'][1]/task['period']
	else:
		return dbf2(task,t,d)

def SEIFDA(task,HindexTasks,k,scheme):
	d1=0
	while 1:			
		
		setDeadline(task,scheme,d1,ifsame)	

		t=[]
		for a in range(1,k+1):
			for itask in HindexTasks+[task]:
				t.append((a-1)*itask['period'])
				for p in range(len(itask['paths'])):
					t.append(itask['paths'][p]['deadline'][0]+(a-1)*itask['period'])			
					t.append(itask['period']-(itask['paths'][p]['deadline'][1]+itask['paths'][p]['Sseg'][0])+(a-1)*itask['period'])
					t.append(itask['period']-itask['paths'][p]['Sseg'][0]+(a-1)*itask['period'])
			
		flag=False
		#print len(t)
		for it in t:
			dbf=0
			for itask in HindexTasks+[task]:			
				dbf+=dbfpath(itask,it,k)			
			if dbf >it:
				flag=True
				break
		#print d1
		if flag==True:
			if scheme=='minD' or scheme=='PBminD':				
				d1=d1+1			
			else:				
				d1=d1-1
		else:
			return True	

		if TerminationCheck(task,scheme,d1,ifsame):
			return False
			
def greedy(tasks,scheme):
	sortedTasks=sorted(tasks,cmp=lm_cmp)
	
	ischme=scheme.split('-')[1]
	k=int(scheme.split('-')[2])
	#print k

	for i in xrange(len(sortedTasks)):
		task=sortedTasks[i]
		HindexTasks=sortedTasks[:i]
		
		d1=SEIFDA(task,HindexTasks,k,ischme)
		if task['Cseg'][0]>=task['Cseg'][1]:
			d=(task['period']-task['sslength'])-d1
			c=task['Cseg'][1]
		else:
			d=d1
			c=task['Cseg'][0]
		if d>(task['period']-task['sslength'])/2 or d<c:

			return False
		else:
			task['d1']=d1

		
		
	# 	D=(task['period']-task['sslength'])/2
	# 	dbf=0
	# 	HEPTasks=sortedTasks[:i+1]
	# 	for jtask in HEPTasks:
	# 		dbf+=dbfEDA(D,jtask)
	# 	if dbf>D:
	# 		return False
	t=[]
	for a in range(1,k+1):
		for itask in tasks:
			t.append(itask['d1']+(a-1)*itask['period'])
			t.append((a-1)*itask['period'])
			t.append(itask['period']-(itask['d1']+itask['sslength'])+(a-1)*itask['period'])
			t.append(itask['period']-itask['sslength']+(a-1)*itask['period'])

	
	#print len(t)
	## validation (necessary condition)
	for it in t:
		dbf=0
		for itask in tasks:
			d=itask['d1']
			dbf+=max(dbf1FPTAS(itask,it,d,k),dbf2FPTAS(itask,it,d,k))
		if dbf>it:
			print dbf,d,'false'
		
	return True






	