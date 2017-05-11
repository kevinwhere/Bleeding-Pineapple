from __future__ import division
import random
import math
import sys, getopt
import json


USet=[]
PSet=[]


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
		pair['period']=p
		pair['execution']=i*p
		pair['deadline']=p
		pair['utilization']=i
		PSet.append(pair)
		j=j+1;

def seg_UUniFast(n,total):
	seg=[]
	sumU=total
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))		
		seg.append(sumU-nextSumU)
		sumU=nextSumU
	seg.append(sumU)

	return seg
def SSS_seg_gen(vRatio,minCtune,maxCtune,maxnumsegs,minSratio,numpaths,scalef):
	global PSet
	numV=int(len(PSet)*vRatio)
	i=0
	
	for itask in PSet:
		if i< numV:
			UB=itask['period']-itask['execution']
			s=random.uniform(minCtune*UB,maxCtune*UB)

			itask["sslength"]=s

			itask["minSr"]=minSratio
			itask["paths"]=[]
			itask["Cseg"]=[]
			itask["Sseg"]=[]
			#the path with the maximum C
			#the path with the maximum S
			iMaxE=random.randrange(numpaths)
			iMaxS=random.randrange(numpaths)
			maxSumC=0
			maxSumS=0
			#generate each path
			for j in range(numpaths):
				

				path={}

				if j!=iMaxE:
					path["Cseg"]=seg_UUniFast(maxnumsegs,itask['execution']*random.uniform(scalef,1))
				else:
					path["Cseg"]=seg_UUniFast(maxnumsegs,itask['execution'])	

				if j!=iMaxS:
					path["Sseg"]=seg_UUniFast(maxnumsegs-1,itask['sslength']*random.uniform(scalef,1))
				else:
					path["Sseg"]=seg_UUniFast(maxnumsegs-1,itask['sslength'])

				deadlineD=[]
				for k in range(len(path['Cseg'])):
					deadlineD.append(-1)
				path['deadline']=deadlineD
				##integeraize
				sumC=0
				sumS=0
				for k in range(len(path['Cseg'])):				
					path['Cseg'][k]=max(1,int(path['Cseg'][k]))
					sumC+=path['Cseg'][k]
				for k in range(len(path['Sseg'])):
					path['Sseg'][k]=max(1,int(path['Sseg'][k]))
					sumS+=path['Sseg'][k]

				itask["paths"].append(path)	
				if sumC>maxSumC:
					maxSumC=sumC
				if sumS>maxSumS:
					maxSumS=sumS
			#numsegs=random.randrange(2,maxnumsegs)
			
			for j in range(maxnumsegs):
				maxCseg=0				
				for k in range(numpaths):								
					if itask["paths"][k]["Cseg"][j]>maxCseg:
						maxCseg=itask["paths"][k]["Cseg"][j]
				itask["Cseg"].append(maxCseg)
				
			
			for j in range(maxnumsegs-1):
				maxSseg=0				
				for k in range(numpaths):							
					if itask["paths"][k]["Sseg"][j]>maxSseg:
						maxSseg=itask["paths"][k]["Sseg"][j]

				itask["Sseg"].append(maxSseg)



			itask['period']=math.ceil(itask['period'])
			itask['execution']=maxSumC
			itask['sslength']=maxSumS

			#print itask
			#itask["Cseg"]=seg_UUniFast(numsegs,itask['execution'])
			#itask["Sseg"]=seg_UUniFast(numsegs-1,itask['sslength'])\

			
			#itask["Sseg"].append(itask['period']-itask['deadline'])
		else:
			s=0
			itask["sslength"]=s
		
		i+=1
def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration_p(numTasks,uTotal,Pmin=100,numLog=1,vRatio=1,sstype="M",seed=1,offtype="R",minSratio=1,numpaths=2,scalef=0.8):
	random.seed(seed)
	init()
	minCtune=0.1
	maxCtune=0.6
	numsegs=2
	#parameterRead()
	if sstype == 'M':
		minCtune=0.1
		maxCtune=0.3
	elif sstype == 'S':
		minCtune=0.01
		maxCtune=0.1
	elif sstype == 'L':
		minCtune=0.3
		maxCtune=0.6
	else:
		assert "error"
		sys.exit()

	if offtype == 'R':
		numsegs=2		
	elif offtype == 'M':
		numsegs=5		
	elif offtype == 'F':
		numsegs=10	
	else:
		assert "error"
		sys.exit()

	#print "N:",numTasks,"U:",uTotal,"SSRatio:",vRatio, "SSType=",sstype,"Seed: ",seed,
	UUniFast(numTasks,uTotal)

	CSet_generate(Pmin,numLog)

	SSS_seg_gen(vRatio,minCtune,maxCtune,numsegs,minSratio,numpaths,scalef)

	return PSet
	

