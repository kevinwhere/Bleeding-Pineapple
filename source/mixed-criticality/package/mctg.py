from __future__ import division
import random
import math
import sys, getopt
import json
import numpy

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
   	
   

def StaffordRandFixedSum(n, u, nsets):

    #deal with n=1 case
    if n == 1:
        return numpy.tile(numpy.array([u]),[nsets,1])

    k = numpy.floor(u)
    s = u
    step = 1 if k < (k-n+1) else -1
    s1 = s - numpy.arange( k, (k-n+1)+step, step )
    step = 1 if (k+n) < (k-n+1) else -1
    s2 = numpy.arange( (k+n), (k+1)+step, step ) - s

    tiny = numpy.finfo(float).tiny
    huge = numpy.finfo(float).max

    w = numpy.zeros((n, n+1))
    w[0,1] = huge
    t = numpy.zeros((n-1,n))

    for i in numpy.arange(2, (n+1)):
        tmp1 = w[i-2, numpy.arange(1,(i+1))] * s1[numpy.arange(0,i)]/float(i)
        tmp2 = w[i-2, numpy.arange(0,i)] * s2[numpy.arange((n-i),n)]/float(i)
        w[i-1, numpy.arange(1,(i+1))] = tmp1 + tmp2;
        tmp3 = w[i-1, numpy.arange(1,(i+1))] + tiny;
        tmp4 = numpy.array( (s2[numpy.arange((n-i),n)] > s1[numpy.arange(0,i)]) )
        t[i-2, numpy.arange(0,i)] = (tmp2 / tmp3) * tmp4 + (1 - tmp1/tmp3) * (numpy.logical_not(tmp4))

    m = nsets
    x = numpy.zeros((n,m))
    rt = numpy.random.uniform(size=(n-1,m)) #rand simplex type
    rs = numpy.random.uniform(size=(n-1,m)) #rand position in simplex
    s = numpy.repeat(s, m);
    j = numpy.repeat(int(k+1), m);
    sm = numpy.repeat(0, m);
    pr = numpy.repeat(1, m);

    for i in numpy.arange(n-1,0,-1): #iterate through dimensions
        e = ( rt[(n-i)-1,...] <= t[i-1,j-1] ) #decide which direction to move in this dimension (1 or 0)
        sx = rs[(n-i)-1,...] ** (1/float(i)) #next simplex coord
        sm = sm + (1-sx) * pr * s/float(i+1)
        pr = sx * pr
        x[(n-i)-1,...] = sm + pr * e
        s = s - e
        j = j - e #change transition table column if required

    x[n-1,...] = sm + pr * s

    #iterated in fixed dimension order but needs to be randomised
    #permute x row order within each column
    for i in xrange(0,m):
        x[...,i] = x[numpy.random.permutation(n),i]

    return numpy.transpose(x);

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
	global USet,PSet

	j=0
	for i in USet:
		thN=j%numLog
		p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
		pair={}
		pair['utilization']=i
		pair['period']=p
		pair['execution']=i*p
		PSet.append(pair)
		j=j+1;

def SSS_generate(ssU,n,maxUsdRes,numCritical):
	global PSet
	
	ssUlist=[]
	
	while 1:
		restart=0
		SS=[]
		sumU=ssU
		#print sumU
		nextSumU=0
		for i in range(n-1):
			nextSumU=sumU*math.pow(random.random(), 1/(n-i))
			if (sumU-nextSumU)+	PSet[i]['ncriutilization'] >1:
				restart=1				
				break
			SS.append(sumU-nextSumU)
			sumU=nextSumU
			
		if restart ==1:
			continue
		if nextSumU+PSet[n-1]['ncriutilization'] >1:
			continue		
		SS.append(nextSumU)
		ssUlist=SS
		
		break

	for i in range(n):
		PSet[i]['accUtilization']=ssUlist[i]		
		PSet[i]['accExecution']=PSet[i]['period']*PSet[i]['accUtilization']
		PSet[i]['maxUsdRes']=maxUsdRes
		PSet[i]['numCritical']=numCritical
		PSet[i]['utilization']=PSet[i]['accUtilization']+PSet[i]['ncriutilization']

	
	

def AAA_generate(totRes,maxUsdRes,numCritical):
	global PSet
	n=maxUsdRes
	for itask in PSet:

		SS=[]

		sumU=itask['accUtilization']
		
		#print sumU
		nextSumU=0
		for i in range(n-1):
			nextSumU=sumU*math.pow(random.random(), 1/(n-i))
			
			SS.append(sumU-nextSumU)
			sumU=nextSumU
		SS.append(sumU)
		resAcc=[]
		for i in range(totRes):
			q={}
			q['totacc']=0
			resAcc.append(q)
		
		X=random.sample(xrange(totRes), maxUsdRes)
		itask['resEdge']=X
		j=0
		for iSS in SS:

			resAcc[X[j]]['totacc']=iSS*itask['period']
			resAcc[X[j]]['maxacc']=random.uniform(iSS*itask['period']/numCritical, iSS*itask['period'])
			j+=1
		
		itask['resGraph']=resAcc
		
		
def	VRBSet_generate(numMode,vRatio,scalefac):

	numV=int(len(PSet)*vRatio)
	
	i=0
	for iStask in PSet:		
		if i< numV:		
			modes=[]
			
			numcl=random.randrange(1,numMode+1)			
			for j in range(numcl):
				
				p=iStask['period']
				c=iStask['period']*iStask['utilization']				

				#tune C for non- MaxU 				
				pair={}
				pair['period']=p ## 
				pair['execution']=c*scalefac**(j)
				if j==0:
					pair['C']=c
				else:
					pair['C']=c*scalefac**(j)-c*scalefac**(j-1)
				pair['CL']=j+1
				pair['utilization']=pair['execution']/p
				modes.append(pair)
				

			VRBSet.append(modes)
			i+=1
		else:			
			modes=[]
			p=iStask['period']
			c=iStask['period']*iStask['utilization']			
			pair={}
			pair['period']=p## 
			pair['execution']=c
			pair['C']=c
			pair['CL']=1
			pair['utilization']=pair['execution']/p
			modes.append(pair)
			VRBSet.append(modes)	
def init():
	global USet,PSet,VRBSet
	USet=[]
	PSet=[]
	VRBSet=[]
def taskGeneration_p(numTasks,uTotal,Pmin=1,numLog=2,Ratio=3,seed=1,numMode=5,vRatio=1,systype='S'):
	random.seed(seed)
	numpy.random.seed(seed)
	init()
	#parameterRead()
	
	if systype=='S':
		gscaleFac=1.81
	elif systype=='M':
		gscaleFac=2.83
	elif systype=='L':
		gscaleFac=5.83
	else:
		gscaleFac=1.1
	uC=uTotal*Ratio/(1+Ratio)
	accessU=uTotal/(1+Ratio)

	#print "N:",numTasks,"U:",uTotal,"SSRatio:",vRatio, "SSType=",sstype,"Seed: ",seed,
	#UUniFast_Discard(numTasks,uC)
	X=StaffordRandFixedSum(numTasks, uC, 1)
	global USet,VRBSet
	USet=X[0]
	CSet_generate(Pmin,numLog)
	VRBSet_generate(numMode,vRatio,gscaleFac)
	#USSS_generate(accessU,numTasks,maxUsdQ,numCritical)
	#UAAA_generate(totRes,maxUsdQ,numCritical)

	return VRBSet
	
