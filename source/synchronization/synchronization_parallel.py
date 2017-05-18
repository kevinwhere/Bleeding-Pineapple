from __future__ import division
from joblib import Parallel, delayed
import multiprocessing

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
#schemes=['FRDEDF=PBminD=2-PCP-FF-SLM']
#'PCP-ROP-FF-RM'
#'PIP','MrsP','MPCP','PCP-ROP-FF-RM','PCP-FRDFP-FF-SLM','NPP-FRDFP-FF-SLM','FRDEDF=PBminD=2-NPP-FF-SLM','FRDEDF=PBminD=2-PCP-FF-SLM','NPDBF'
schemes=['FRDEDF=PBminD=2-PCP-FF-SLM']
ratio=['10']
periodlogs=['1']
maxUsdQ=['1']
processors=['4']
numQ=['4']


def acceptance_ratio(u=1,numLog=2,Ratio=1,sstype='R',totRes=4,maxUsdQ=1,ischeme='D',iprocessor=4):	

	print "Scheme:",ischeme,"n:",tasksinBkt,"U:",(u+UStart)*UStep,"type:", isstype, "ratio:",iratio," procs:",iprocessor," maxUsdQ:", maxUsdQ," numQ:", inumQ

	numfail=0
	for i in xrange(0,totBucket,1):
		
		percentageU=((u+UStart)*UStep/100)*int(iprocessor)
		
		
		tasks=tg.taskGeneration_p(tasksinBkt*int(iprocessor),percentageU,seed=i,numLog=int(numLog),Ratio=int(Ratio),sstype=sstype,totRes=int(totRes),maxUsdQ=maxUsdQ)
		
		
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
			print ischeme.split("-")[0]
			sys.exit()
	return numfail

for ischeme in schemes:
	for iprocessor in processors:
		for isstype in sstype:
			for iplog in periodlogs:
				for inumQ in numQ:
					for iratio in ratio:
						t1 = datetime.now()	
						# Initialize X and Y axes 
						x = np.arange(1, int(100/UStep)+1) 
						#y = np.zeros(int(100/UStep)+1)					
						
						
						y = Parallel(n_jobs= multiprocessing.cpu_count())(delayed(acceptance_ratio)(u,numLog=int(iplog),Ratio=int(iratio),sstype=isstype,totRes=int(inumQ),maxUsdQ=int(maxUsdQ[0]),ischeme=ischeme,iprocessor=(iprocessor)) for u in x)	

						y=[1.0]+[(totBucket-d)/100 for d in y]
						print "acceptanceRatio:",y											
						t2 = datetime.now()	
						delta=t2-t1
						print delta
						plotfile=prefixdata+"/"+isstype+"/"+iratio+"/"+ischeme+"-m"+iprocessor+"-Q"+inumQ+"-max"+maxUsdQ[0]+"-n"+str(tasksinBkt)
						np.save(plotfile,np.array([x,y]))
		
			
		
			