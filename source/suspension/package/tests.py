from __future__ import division
import math

def SC_EDF(tasks):
	U=0
	for itask in tasks:
		U+=(itask['execution']+itask['sslength'])/itask['period']
	
	return EDFB(U)
def dbfEDA(t,task):
	D=(task['period']-task['sslength'])/2
	if t<D:
		return 0
	else:
		return task['Cseg'][0]+task['Cseg'][1]+(t-D)*(task['Cseg'][0]+task['Cseg'][1])/task['period']
def dbfNC1(task,t):
	return int((t+task['sslength'])/task['period'])*task['Cseg'][1]+int((t-(task['period']-task['sslength']))/task['period'])*task['Cseg'][0]
def dbfNC2(task,t):
	return int((t+(task['sslength']))/task['period'])*task['Cseg'][0]+int((t)/task['period'])*task['Cseg'][1]
def dbfNC(t,task):
	return max(dbfNC1(task,t),dbfNC2(task,t))
	

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
def lm_cmp(x, y):
	dx=(x['period']-x['sslength'])/2
	dy=(y['period']-y['sslength'])/2
	return int(dx - dy)
def NC(tasks):
	
	for i in xrange(len(tasks)):
		task=tasks[i]
		D=(task['period']-task['sslength'])

		dbf=0
		
		for jtask in tasks:
			dbf+=dbfNC(D,jtask)
		if dbf>D:
			return False

		D=(task['period'])
		
		dbf=0
		HEPTasks=tasks[:i+1]
		for jtask in tasks:
			dbf+=dbfNC(D,jtask)
		if dbf>D:
			return False
	return True
def SEIFDA(task,HindexTasks,k,scheme):
	if scheme=='minD':
		if task['Cseg'][0]<task['Cseg'][1]:
			d1=task['Cseg'][0]
		else:
			d1=(task['period']-task['sslength'])-task['Cseg'][1]
	elif scheme=='maxD':
		d1=(task['period']-task['sslength'])/2
	elif scheme=='PBminD':
		if task['Cseg'][0]+task['Cseg'][1] ==0:
			print "0"
			d1=0
		else:
			if task['Cseg'][0]<task['Cseg'][1]:
				d1=(task['period']-task['sslength'])*task['Cseg'][0]/(task['Cseg'][0]+task['Cseg'][1])
			else:
				d1=task['period']-task['sslength']-(task['period']-task['sslength'])*task['Cseg'][1]/(task['Cseg'][0]+task['Cseg'][1])
	
	while 1:

		if task['Cseg'][0]<task['Cseg'][1]:
			d=d1
			c=task['Cseg'][0]
		else:
			d=(task['period']-task['sslength'])-d1
			c=task['Cseg'][1]
		if d>(task['period']-task['sslength'])/2 or d<c:
			return d1
		t=[]
		for a in range(1,k+1):
			for itask in HindexTasks:
				t.append(itask['d1']+(a-1)*itask['period'])
				t.append((a-1)*itask['period'])
				t.append(itask['period']-(itask['d1']+itask['sslength'])+(a-1)*itask['period'])
				t.append(itask['period']-itask['sslength']+(a-1)*itask['period'])

			t.append(d1+(a-1)*task['period'])
			t.append((a-1)*task['period'])
			t.append(task['period']-(d1+task['sslength'])+(a-1)*task['period'])
			t.append(task['period']-task['sslength']+(a-1)*task['period'])
		flag=False
		#print len(t)
		for it in t:
			dbf=0
			for itask in HindexTasks:
				d=itask['d1']
				dbf+=max(dbf1FPTAS(itask,it,d,k),dbf2FPTAS(itask,it,d,k))
			dbf+=max(dbf1FPTAS(task,it,d1,k),dbf2FPTAS(task,it,d1,k))
			if dbf >it:
				flag=True
				break
		#print d1
		if flag==True:
			if scheme=='minD' or scheme=='PBminD':
				if task['Cseg'][0]<task['Cseg'][1]:
					d1=d1+1
				else:
					d1=d1-1
			else:
				if task['Cseg'][0]<task['Cseg'][1]:
					d1=d1-1
				else:
					d1=d1+1

			continue
		else:
			return d1
			
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
def EDA(tasks):
	sortedTasks=sorted(tasks,cmp=lm_cmp)
	for i in xrange(len(sortedTasks)):
		task=sortedTasks[i]
		D=(task['period']-task['sslength'])/2
		dbf=0
		HEPTasks=sortedTasks[:i+1]
		for jtask in HEPTasks:
			dbf+=dbfEDA(D,jtask)
		if dbf>D:
			return False
	return True





	