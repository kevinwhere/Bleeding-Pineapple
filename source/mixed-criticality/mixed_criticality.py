from __future__ import division
import random
import math
import sys, getopt
import json
import numpy as np
import mctg,mctest

from package import mctg, EDFVD, MCNC

totBucket=100
tasksinBkt=10
UStep=5
UStart=0


prefix="tmp/"
prefixdata="plot/data"


schemes=['EDFVD']
types=['S','M','L']
periodlogs=['2']
numQ=['4']
maxUsdQ=['1']
processors=['1']
numCL=['2']
for ischeme in schemes:
	for iprocessor in processors:
		for itype in types:
				for inumCL in numCL:
							
						# Initialize X and Y axes 
						x = np.arange(0, int(100/UStep)+1) 
						y = np.zeros(int(100/UStep)+1)
									
						for u in x:
							
							print "Scheme:",ischeme,"n:",tasksinBkt,"U:",(u+UStart)*UStep, " procs:",iprocessor,itype,inumCL
							
							
							
							numfail=0
							for i in xrange(0,totBucket,1):
								
								percentageU=((u+UStart)*UStep/100)*int(iprocessor)
								
								#percentageU=(70/100)*int(iprocessor)
								if percentageU == 0:
									continue
	
								tasks=mctg.taskGeneration_p(tasksinBkt*int(iprocessor),percentageU,seed=i,systype=itype,numMode=int(inumCL))
								#print tasks
								#print c.microseconds, "ms",
								# fi = open('taskset', "r")
								# tasks= json.load(fi)
								# fi.close()
								# for itask in tasks:
								# 	itask['execution']=itask['execution']*int(issprop)/10
								## sort by increasing periods
								#sortedTasks=sorted(tasks, key=lambda item:item['period']) 
								#print sortedTasks
								# u=0
								# for i in sortedTasks:
								# 	u+=i['execution']/i['period']
								# 	print i
								# print u
								
								if ischeme == 'EDF-VD':
									if EDFVD.EDF_VD(tasks,int(inumCL))== False:
										#print "Fail"
										numfail+=1
								elif ischeme== 'EDF-VD2':
									if EDFVD.EDF_VD2(tasks,int(inumCL))== False:
										#print "Fail"
										numfail+=1								
								elif ischeme == 'DBF':
									if MCNC.DBF_MC(tasks,int(inumCL))== False:
										#print "Fail"
										numfail+=1
								else:
									sys.exit()
								#print c.microseconds, "ms"
	
					
							acceptanceRatio=1-(numfail/totBucket)
							print "acceptanceRatio:",acceptanceRatio
							y[u]=acceptanceRatio
							
						# for u in range(0,UStart,UStep):
						# 	y[u]=1
						# for u in range(UEnd+1,totBucket+1,UStep):
						# 	y[u]=0
						
						plotfile=prefixdata+"/CL/"+inumCL+"/"+itype+"/"+ischeme
						np.save(plotfile,np.array([x,y]))
		
			
		
			