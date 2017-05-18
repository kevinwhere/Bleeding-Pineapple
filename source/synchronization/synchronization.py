from __future__ import division
import random
import math
import sys, getopt
import json
import numpy as np
from package import tg,PIP,MPCP,MrsP,ROP,NPDBF
from datetime import datetime
totBucket=100
tasksinBkt=10
UStep=5
UStart=0


prefix="tmp/"
prefixdata="plot/data"

sstype= ['R']
#schemes=['PCP-FRDEDF=PBminD=2-FF-SLM']
#'PCP-ROP-FF-RM'
#'PIP','MrsP','MPCP','PCP-ROP-FF-RM','PCP-FRDFP-FF-SLM','NPP-FRDFP-FF-SLM','NPP-FRDEDF=PBminD=2-FF-SLM','PCP-FRDEDF=PBminD=2-FF-SLM','NPDBF'
schemes=['FRDEDF=PBminD=2-PCP-FF-SLM']
ratio=['10']
periodlogs=['1']
maxUsdQ=['1']
processors=['4']
numQ=['4']

for ischeme in schemes:
	for iprocessor in processors:
		for isstype in sstype:
			for iplog in periodlogs:
				for inumQ in numQ:
					for iratio in ratio:	
						# Initialize X and Y axes 
						x = np.arange(0, int(100/UStep)+1) 
						y = np.zeros(int(100/UStep)+1)
						
						t1 = datetime.now()
						for u in x:
							
							print "Scheme:",ischeme,"n:",tasksinBkt,"U:",(u+UStart)*UStep,"type:", isstype, "ratio:",iratio," procs:",iprocessor," maxUsdQ:", maxUsdQ[0]," numQ:", inumQ
							
							
							
							numfail=0
							for i in xrange(0,totBucket,1):
								
								percentageU=((u+UStart)*UStep/100)*int(iprocessor)
								#percentageU=(70/100)*int(iprocessor)
								if percentageU == 0:
									continue
	
								tasks=tg.taskGeneration_p(tasksinBkt*int(iprocessor),percentageU,seed=i,numLog=int(iplog),Ratio=int(iratio),sstype=isstype,totRes=int(inumQ),maxUsdQ=int(maxUsdQ[0]))
								
								
								if ischeme == 'NPDBF':
									if NPDBF.NPDBF(tasks,int(iprocessor),ischeme,int(inumQ))== False:
										#print "Fail"
										numfail+=1
								elif  ischeme == 'PIP':
									if PIP.PIP(tasks,int(iprocessor),ischeme,int(inumQ))== False:
										#print "Fail"
										numfail+=1
								elif  ischeme == 'MPCP':
									if MPCP.MPCP(tasks,int(iprocessor),ischeme,int(inumQ))== False:
										#print "Fail"
										numfail+=1		
								elif  ischeme == 'MrsP':
									if MrsP.MrsP(tasks,int(iprocessor),ischeme,int(inumQ))== False:
										#print "Fail"
										numfail+=1	
								elif  ischeme.split("-")[0] == 'ROP' or ischeme.split("-")[0] == 'FRDFP' or ischeme.split("-")[0].split("=")[0] == 'FRDEDF':
									if ROP.ReasonableAllocation(tasks,int(iprocessor),ischeme,int(inumQ)) == False:
											#print "Fail"
											numfail+=1								
								else:
									sys.exit()
	
					
							acceptanceRatio=1-(numfail/totBucket)
							print "acceptanceRatio:",acceptanceRatio
							y[u]=acceptanceRatio							
						t2 = datetime.now()
						delta = t2 - t1
						print delta
						plotfile=prefixdata+"/"+isstype+"/"+iratio+"/"+ischeme+"-m"+iprocessor+"-Q"+inumQ+"-max"+maxUsdQ[0]+"-n"+str(tasksinBkt)
						np.save(plotfile,np.array([x,y]))
		
			
		
			