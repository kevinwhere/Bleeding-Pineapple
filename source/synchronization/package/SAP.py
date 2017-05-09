
def compare_SAP(x,y):
	minxp=100000
	for itask in x:
		if itask['period']<minxp:
			pminxtask=itask
			minxp=itask['period']
	xcost=0
	
	for i in range(len(pminxtask['resGraph'])):
		xLocal=0
		xGlobal=0
		maxA=0
		for itask in x:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']>maxA:
					maxA=itask['resGraph'][i]['maxacc']
		xGlobal=maxA/minxp

		xLocal=0
		for itask in x:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']/itask['period']>xLocal:
					xLocal=itask['resGraph'][i]['maxacc']/itask['period']
		xcost+=xGlobal-xLocal


	minyp=100000
	for itask in y:
		if itask['period']<minyp:
			pminytask=itask
			minyp=itask['period']


	ycost=0
	
	for i in range(len(pminytask['resGraph'])):
		yLocal=0
		yGlobal=0
		maxA=0
		for itask in y:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']>maxA:
					maxA=itask['resGraph'][i]['maxacc']
		yGlobal=maxA/minyp

		yLocal=0
		for itask in x:
			if itask['resGraph'][i]['totacc']!=0:
				if itask['resGraph'][i]['maxacc']/itask['period']>yLocal:
					yLocal=itask['resGraph'][i]['maxacc']/itask['period']
		ycost+=yGlobal-yLocal

	if xcost>ycost:
		return 1
	else:
		return -1
def numeric_compare(x,y):
	xsumU=0
	ysumU=0
	for itask in x:
		xsumU+=(itask['execution']+itask['accExecution'])/itask['period']
	for itask in y:
		ysumU+=(itask['execution']+itask['accExecution'])/itask['period']
	#print xsumU,ysumU
	if xsumU>ysumU:
		return -1
	else:
		return 1