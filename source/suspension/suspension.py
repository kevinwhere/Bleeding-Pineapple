from __future__ import division
import random
import sys
import numpy as np
from package import tg,tests

totBucket=100
tasksinBkt=10

UStart=1
UEnd=99
UStep=5

prefix="tmp/"
prefixdata="plot/data"

sstype= ['L','M','S']
sspropotions=['10']
ssofftypes = ['R'] ## R: 2 computation segments
schemes=['SEIFDA-minD-2','SEIFDA-minD-3','SEIFDA-minD-4','SEIFDA-minD-5','SEIFDA-maxD-2','SEIFDA-maxD-3','SEIFDA-maxD-4','SEIFDA-maxD-5','SEIFDA-PBminD-2','SEIFDA-PBminD-3','SEIFDA-PBminD-4','SEIFDA-PBminD-5']

periodlogs=['2']
for ischeme in schemes:
	for isstype in sstype:
		for issofftype in ssofftypes:		
			for issprop in sspropotions:
					for iplog in periodlogs:
						
						# Initialize X and Y axes 
						x = np.arange(0, int(100/UStep)+1) 
						y = np.zeros(int(100/UStep)+1)
						for u in xrange(0,len(y),1):
							print "Scheme:",ischeme,"N:",totBucket,"U:",u*UStep, "SSType:",isstype,"OffType:",issofftype,"prop: ", issprop
							if u ==0:
								y[u]=1
								continue
							if u*UStep ==100:
								y[u]=0
								continue
							numfail=0

							for i in xrange(0,totBucket,1):
								
								percentageU=u*UStep/100					
								prop=int(issprop)/10
								tasks=tg.taskGeneration_p(tasksinBkt,percentageU,sstype=isstype,vRatio=prop,seed=i,numLog=int(iplog),offtype=issofftype)
								for itask in tasks:			
									print itask
								## sort by increasing periods
								sortedTasks=sorted(tasks, key=lambda item:item['period']) 
							
								if ischeme == 'SCEDF':
									if tests.SC_EDF(sortedTasks) == False:
										numfail+=1								
								elif ischeme == 'MIP':
									if mipx.mip(sortedTasks) == False:
										numfail+=1								
								elif ischeme.split('-')[0] == 'SEIFDA':
									if tests.greedy(sortedTasks,ischeme) == False:
										numfail+=1	
								elif ischeme == 'EDA':
									if tests.EDA(sortedTasks) == False:										
										numfail+=1		
								elif ischeme == 'NC':
									if tests.NC(sortedTasks) == False:										
										numfail+=1	
								else:
									assert ischeme, "not vaild ischeme"
					
							acceptanceRatio=1-(numfail/totBucket)
							print "acceptanceRatio:",acceptanceRatio
							y[u]=acceptanceRatio
					
						# for u in range(0,UStart,UStep):
						# 	y[u]=1
						# for u in range(UEnd+1,totBucket+1,UStep):
						# 	y[u]=0
						
						plotfile=prefixdata+"/"+isstype+"/"+issofftype+"/"+ischeme					
						
						np.save(plotfile,np.array([x,y]))
		
			
		
			