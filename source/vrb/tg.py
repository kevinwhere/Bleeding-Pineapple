from __future__ import division
import random
import math
import sys, getopt
import json


USet=[]
PSet=[]
VRBSet=[]

def parameterRead():
	global gscaleFac, uTotal, numTasks, numMode, xMode, numLog, ofile,vRatio
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:u:n:f:m:x:p:o:v:")
	except getopt.GetoptError:
		print 'test.py -i <seed> -u <totalutilzation> -if <scalefactor>'
		sys.exit(2)
	print opts, args
	
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <randoseed> -u <totalutilzation> -f <scalefactor>'
			sys.exit()
		elif opt in ("-u"):
			uTotal = float(float(arg)/100)
		elif opt in ("-i"):
			random.seed(int(arg))
		elif opt in ("-n", "--num"):
			numTasks = int(arg)
		elif opt in ("-f", "--scalefacor"):
			gscaleFac = float(arg)
		elif opt in ("-m", "--mode"):
			numMode = int(arg)
		elif opt in ("-x", "--xmode"):
			xMode = int(arg)
		elif opt in ("-p", "--numLog"):
			numLog = float(arg)
		elif opt in ("-v", "--v"):
			vRatio = float(arg)
		elif opt in ("-o", "--output"):
			ofile = arg
		else:
			assert False, "unhandled option"
   	
   

def UUniFast(n,U_avg):
	global USet
	sumU=U_avg
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))		
		USet.append(sumU-nextSumU)
		sumU=nextSumU
	USet.append(sumU)

def UUniFast_Discard(n,U_avg):	
	while 1:
		sumU=U_avg
		for i in range(n-1):
			nextSumU=sumU*math.pow(random.random(), 1/(n-i))		
			USet.append(sumU-nextSumU)
			sumU=nextSumU
		USet.append(sumU)

		if max(USet) < 1:			
			break
		del USet[:]

def UniDist(n,U_min,U_max):
	for i in range(n-1):
		uBkt=random.uniform(U_min, U_max)
		taskSet.append(uBkt)
def	CSet_generate(Pmin,numLog):
	j=0
	for i in USet:
		thN=j%numLog
		p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
		pair={}
		pair['period']=p
		pair['utilization']=i
		PSet.append(pair)
		j=j+1;
maxCtune=1
minCtune=0.75
def	VRBSet_generate(numMode,vRatio,scalefac):
	numV=int(len(PSet)*vRatio)
	i=0
	for iStask in PSet:		
		if i< numV:

			iMaxU=random.randrange(numMode)
			modes=[]
			for j in range(numMode):
				p=iStask['period']*math.pow(scalefac, j)
				c=iStask['period']*iStask['utilization']*math.pow(scalefac, j)			
				#tune C for non- MaxU 
				if j != iMaxU:		
					c=c*random.uniform(minCtune,maxCtune);
				s=math.ceil(p)/p
				pair={}
				pair['period']=math.ceil(p) ## 
				pair['execution']=c*s
				modes.append(pair)
			VRBSet.append(modes)
			i+=1
		else:
			modes=[]
			p=iStask['period']
			c=iStask['period']*iStask['utilization']
			s=math.ceil(p)/p
			pair={}
			pair['period']=math.ceil(p) ## 
			pair['execution']=c*s
			modes.append(pair)
			VRBSet.append(modes)	

def init():
	global USet,PSet,VRBSet
	USet=[]
	PSet=[]
	VRBSet=[]


def taskGeneration_p(numTasks,uTotal,Pmin=1,numMode=5,vRatio=0.5,gscaleFac=1.5,numLog=2,seed=1):
	random.seed(seed)
	init()
	

	#print "N:",numTasks,"U:",uTotal,"SSRatio:",vRatio, "SSType=",sstype,"Seed: ",seed,
	UUniFast(numTasks,uTotal)

	CSet_generate(Pmin,numLog)

	VRBSet_generate(numMode,vRatio,gscaleFac)
	return VRBSet
	
