from __future__ import division
import random
import math
import sys, getopt
import json


USet=[]
PSet=[]
VRBSet=[]

   	
   

def UUniFast(n,U_avg):
	global USet
	sumU=U_avg
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))		
		USet.append(sumU-nextSumU)
		sumU=nextSumU
	USet.append(sumU)

def	SetGenerate(Pmin,numLog):
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


def	VRBSetGenerate(numMode,vRatio,scalefac):
	## a proportion of tasks is convented to multi-mode tasks	
	numV=int(len(PSet)*vRatio)
	i=0
	for iStask in PSet:
		if i< numV:
			## one of the modes is chosen as the baseline (the one with the maximum utilization) to adjust the other modes 
			iMaxU=random.randrange(numMode)
			modes=[]
			for j in range(numMode):
				## scale the period and the execution according to the scalefactor 
				p=iStask['period']*math.pow(scalefac, j)
				c=iStask['period']*iStask['utilization']*math.pow(scalefac, j)			
				#tune C for non- MaxU by multiplying them by uniform random values in the range [minCtune,maxCtune]
				if j != iMaxU:		
					c=c*random.uniform(minCtune,maxCtune);

				## discrete time model
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
			## discrete time model
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


def TaskGeneration(numTasks,uTotal,Pmin=1,numMode=5,vRatio=0.5,gscaleFac=1.5,numLog=2,seed=1):
	## Initialize internal state of the random number generator
	random.seed(seed)
	init()	

	## the UUniFast method is adopted to generate a set of utilization values with the given goal
	UUniFast(numTasks,uTotal)
	## generate the task periods according to the log distribution
	SetGenerate(Pmin,numLog)
	## converted sporadic tasks to multi-mode tasks
	VRBSetGenerate(numMode,vRatio,gscaleFac)
	return VRBSet
	
