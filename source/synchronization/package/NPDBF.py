import heapq
def NPDBF(tasks,M,scheme,numQ):	
	
	sortedTasks=sorted(tasks, key=lambda item:item['period'])	

	for i in range(len(sortedTasks)):

		HPTasks=sortedTasks[:i]
		LPTasks=sortedTasks[i+1:]

		task=sortedTasks[i]
		
		for j in range(len(task['resGraph'])):

			if task['resGraph'][j]['totacc']==0:
				continue
			else:
				
				HPC=0
				for itask in HPTasks:
					if itask['resGraph'][j]['totacc'] !=0:
						#demand before deadline
						HPC+=itask['resGraph'][j]['totacc']*int(task['period']/itask['period'])
				B=0
				CI=[]
				for itask in LPTasks:
					if itask['resGraph'][j]['totacc'] !=0:
							CI.append(itask['resGraph'][j]['maxacc'])
						# pick the maximum one
				decWCtasks=heapq.nlargest(1,CI)				
				B=sum(decWCtasks)
				if (HPC+B+task['resGraph'][j]['totacc'])/task['period']>1:
					return False