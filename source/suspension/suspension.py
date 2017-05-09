from __future__ import division
import random
import sys
import numpy as np
from package import tgPath,SCEDF,EDA,NC,SEIFDA,Audsley,PATH

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
#schemes=['SCEDF','PASS-OPA','SEIFDA-minD-2','SEIFDA-PBminD-2','PATH-minD-2-D=D','PATH-PBminD-2-D=D','PATH-minD-2-DnD','PATH-PBminD-2-DnD']
schemes=['PATH-minD-2-D=D']
periodlogs=['2']
for ischeme in schemes:
	for isstype in sstype:
		for issofftype in ssofftypes:		
			for issprop in sspropotions:
					for iplog in periodlogs:
						
						# Initialize X and Y axes 
						x = np.arange(0, int(100/UStep)+1) 
						y = np.zeros(int(100/UStep)+1)
						ifskip=False
						for u in xrange(0,len(y),1):
							print "Scheme:",ischeme,"N:",totBucket,"U:",u*UStep, "SSType:",isstype,"OffType:",issofftype,"prop: ", issprop
							if u ==0:
								y[u]=1
								continue
							if u*UStep ==100:
								y[u]=0
								continue
							numfail=0

							if ifskip == True:
								print "acceptanceRatio:",0
								y[u]=0
								continue

							for i in xrange(0,totBucket,1):
								
								percentageU=u*UStep/100					
								prop=int(issprop)/10
								tasks=tgPath.taskGeneration_p(tasksinBkt,percentageU,sstype=isstype,vRatio=prop,seed=i,numLog=int(iplog),offtype=issofftype)
								
								## sort by increasing periods
								#sortedTasks=sorted(tasks, key=lambda item:item['period']) 
							
								if ischeme == 'SCEDF':
									if SCEDF.SC_EDF(tasks) == False:
										numfail+=1	
								elif ischeme == 'PASS-OPA':
									if Audsley.Audsley(tasks) == False:
										numfail+=1								
								elif ischeme == 'MIP':
									if mipx.mip(tasks) == False:
										numfail+=1								
								elif ischeme.split('-')[0] == 'SEIFDA':
									if SEIFDA.greedy(tasks,ischeme) == False:
										numfail+=1
								elif ischeme.split('-')[0] == 'PATH':
									if PATH.PATH(tasks,ischeme) == False:
										numfail+=1
								elif ischeme == 'EDA':
									if EDA.EDA(tasks) == False:										
										numfail+=1		
								elif ischeme == 'NC':
									if NC.NC(tasks) == False:										
										numfail+=1	
								else:
									assert ischeme, "not vaild ischeme"
					
							acceptanceRatio=1-(numfail/totBucket)
							print "acceptanceRatio:",acceptanceRatio
							y[u]=acceptanceRatio
							if acceptanceRatio == 0:
								ifskip=True
					
						# for u in range(0,UStart,UStep):
						# 	y[u]=1
						# for u in range(UEnd+1,totBucket+1,UStep):
						# 	y[u]=0
						
						plotfile=prefixdata+"/"+isstype+"/"+issofftype+"/"+ischeme					
						
						np.save(plotfile,np.array([x,y]))
		
			
		
			