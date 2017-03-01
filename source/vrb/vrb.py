from __future__ import division
import random
import math
import sys, getopt
import json
import numpy as np
import tg,scheme
from datetime import datetime, timedelta

totBucket=100
tasksinBkt=10


UStep=5
UStart=0

prefix="tmp/"
prefixdata="plot/data"


###### schemes=['DT-FPT','VRBL2-FPT','QT-FPT','OUR-LP','Guan']

schemes=['DP-OPA']
######  modes=['2','4','8']
modes=['5','8','10']
######periodlogs=['1','2','3']
props=['2','5','10']
######periodlogs=['1','2','3']
periodlogs=['2']

for ischeme in schemes:	
	for imode in modes:
			for iplog in periodlogs:				
						
				
				# Initialize X and Y axes 
				x = np.arange(0, int(100/UStep)+1) 
				y = np.zeros(int(100/UStep)+1)
				for u in x:
					print "Scheme:",ischeme,"N:",totBucket,"U:",(u+UStart)*UStep, "Procs:",imode,"logP:",iplog
				
					numfail=0
					for i in xrange(0,totBucket,1):

						percentageU=((u+UStart)*UStep/100)
						if percentageU == 0:
							continue		
						#a = datetime.now()

						tasks=tg.taskGeneration_p(tasksinBkt,percentageU,seed=i,numLog=int(iplog),numMode=int(imode))
						#print tasks
						#b = datetime.now()

						#t1=b-a
						#print "TG time (ms):", t1.microseconds,
						# fi = open('taskset', "r")
						# tasks= json.load(fi)
						# fi.close()
						# for itask in tasks:
						# 	itask['execution']=itask['execution']*int(issprop)/10
						## sort by increasing deadlines
						#sortedTasks=sorted(tasks, key=lambda item:item['deadline']) 
						#print sortedTasks
						# u=0
						# for i in sortedTasks:
						# 	u+=i['execution']/i['period']
						# 	print i
						# print u
						#print sortedTasks
						#if scheme.RB(sortedTasks,ischeme) == False:
						#c = datetime.now()

						if ischeme == 'QT-OPA':
							if scheme.modeAudsley(tasks,ischeme) == False:
								numfail+=1
						if ischeme == 'DP-OPA':
							if scheme.modeAudsley(tasks,ischeme) == False:
								numfail+=1
						elif ischeme == 'QT-RM':
							if scheme.RMQT(tasks,ischeme) == False:
								numfail+=1
						elif ischeme == 'QT-FPT':
							if scheme.Audsley(tasks,ischeme) == False:
								numfail+=1
						elif ischeme == 'VRBL2-FPT':
							if scheme.Audsley(tasks,ischeme) == False:
								numfail+=1
						elif ischeme == 'DT-FPT':
							if scheme.Audsley(tasks,ischeme) == False:
								numfail+=1
						elif ischeme == 'OUR':
							if scheme.GDM(tasks,ischeme,int(imode)) == False:
								numfail+=1
						elif ischeme == 'OURx':
							if scheme.GDM(tasks,ischeme,int(imode)) == False:
								numfail+=1
						elif ischeme == 'LOAD':
							if scheme.GDM(tasks,ischeme,int(imode)) == False:
								numfail+=1
						elif ischeme == 'Guan':
							if scheme.GDM(tasks,ischeme,int(imode)) == False:
								numfail+=1
						elif ischeme == 'BAK':
							if scheme.GDM(tasks,ischeme,int(imode)) == False:
								numfail+=1
						else:
							if scheme.Audsley(tasks,ischeme,int(imode)) == False:
								numfail+=1

						#d = datetime.now()

						#t2=d-c
						#print "analysis time (ms):", t2.microseconds

					
					acceptanceRatio=1-(numfail/totBucket)
					print "acceptanceRatio:",acceptanceRatio
					y[u]=acceptanceRatio
			
				
				
				plotfile=prefixdata+"/m/"+imode+"/"+ischeme
				np.save(plotfile,np.array([x,y]))
		
			
		
			