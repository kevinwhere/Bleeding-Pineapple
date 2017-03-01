from __future__ import division
import random
import math
import sys, getopt
import json


uTotal=0
numTasks=0
xMode=0
U_mean=0.25

tel={}
taskSet=[]
USet=[]
CSet=[]
PSet=[]

ofile=""

#ufo = open("maxuset.txt", "wb")
#betafo = open("beta", "wb")
u_sum=0
Pmax=1000000
Pmin=1
numLog=2


gscaleFac=1.5
maxCtune=1
minCtune=0.75
numMode=5
VRBSet=[ ]
vRatio=0.5

def parameterRead():
	global gscaleFac, uTotal, numTasks, numMode, xMode, vRatio, ofile
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:u:n:f:m:x:p:o:")
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
		elif opt in ("-p", "--proportion"):
			vRatio = float(arg)
		elif opt in ("-o", "--output"):
			ofile = arg
		else:
			assert False, "unhandled option"
   	
   

def UUniFast(n,U_avg):
	sumU=U_avg
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))		
		USet.append(sumU-nextSumU)
		sumU=nextSumU
	USet.append(sumU)

def UUniFast_Discard(n,U_avg,U_max,U_min):	
	while 1:
		sumU=U_avg
		for i in range(n-1):
			nextSumU=sumU*math.pow(random.random(), 1/(n-i))		
			taskSet.append(sumU-nextSumU)
			sumU=nextSumU
		taskSet.append(sumU)

		if max(taskSet) < U_max and min(taskSet) > U_min:			
			break
		del taskSet[:]

def ExpDist(limit,U_mean):
	while 1:
		uBkt=random.expovariate(U_mean)
		print uBkt
		if sum(taskSet) + uBkt > limit:
			break
		taskSet.append(uBkt)
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

			
parameterRead()
fo = open(ofile, "wb")
UUniFast(numTasks,uTotal)
CSet_generate(Pmin,numLog)

VRBSet_generate(numMode,vRatio,gscaleFac)

#print VRBSet


print >>fo,json.dumps(VRBSet)

fo.close()