from functions import *


def dbfEDA(t,task):
	D=(task['period']-task['sslength'])/2
	if t<D:
		return 0
	else:
		return task['Cseg'][0]+task['Cseg'][1]+(t-D)*(task['Cseg'][0]+task['Cseg'][1])/task['period']

	
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