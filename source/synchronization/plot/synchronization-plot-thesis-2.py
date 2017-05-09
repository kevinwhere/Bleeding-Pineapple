"""
Simple demo with multiple subplots.
"""
from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
import math
from matplotlib import rcParams
#import matplotlib.font_manager as font_manager

#view available fonts
# prop = font_manager.FontProperties(fname='/usr/share/fonts/TTF/OpenSans-Regular.ttf')
# rcParams['font.family'] = prop.get_name()
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Tahoma']
processors=['4']
Ratio=['20','10','5']
sstype=['R']
periodlogs=['2']
numtasks=['10']

#schemes=['BCL','FF','BAK','OUR-LB','OUR-RTA','Guan']
#schemes=['FF-DM','BF-DM','WF-DM']
#schemes=['MIRROR-RAS+','MIRROR-RAS=','MIRROR-RAS-']
#schemes=['MIRROR-FF','MIRROR-BF','MIRROR-WF']
#schemes=['MRTA','MIRROR']
#schemes=['PIP','MPCP','MrsP','DNP','DPCP','elvDPCP','DNP+','DPCP+','NPDBF']
schemes=['elvDPCP','DNP','DPCP','DNP+','DPCP+','NPDBF']
#schemes=['LOAD','BAK','OUR-LB','OUR-RTA']
figlabel=['a','b','c','d','e','f','g','h','i']
#prefix="data/arbitrary/"
prefix="data/"
numQ=['5']
maxUsdQ=['1']
#'D','o', 'v','+','*','x'
#marker = itertools.cycle(( 's','*','p','D','1','d', 'v','+','o','h','x')) 
#marker = itertools.cycle(( 's','*','o')) 
#marker = [ '*','o','x']
#marker = [ 'd','v','x','o','+','D','*','p','s']
marker = [ '*','o','+','D','p','s']
#'g','b','r','k','k','y'
#colors = itertools.cycle(('r','y','k')) 
colors = ['g','c','c','k','k','y']
#colors = ['b','r','m','k','k','c','g','g','y','y']

#fig=plt.figure()


## create a virtual outer subsplot for putting big x-ylabel 
#ax=fig.add_subplot(111)
#fig.subplots_adjust(top=0.9,left=0.1,right=0.95,hspace =0.3)


#ax.spines['top'].set_color('none')
#ax.spines['bottom'].set_color('none')
#ax.spines['left'].set_color('none')
#ax.spines['right'].set_color('none')
#ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

for i in range(1,7):
	

	if i == 1:
		isstype='R'
		iaccessU='20'
		iprocessor='4'
		inumQ='5'
		imaxUsdQ='1'
	elif i ==2:
		isstype='R'
		iaccessU='20'
		iprocessor='8'
		inumQ='8'
		imaxUsdQ='1'
	elif i ==3:
		isstype='R'
		iaccessU='5'
		iprocessor='8'
		inumQ='8'
		imaxUsdQ='1'
	elif i ==4:
		isstype='R'
		iaccessU='20'
		iprocessor='8'
		inumQ='8'
		imaxUsdQ='3'
	elif i ==5:
		isstype='M'
		iaccessU='20'
		iprocessor='8'
		inumQ='8'
		imaxUsdQ='1'
	elif i ==6:
		isstype='R'
		iaccessU='20'
		iprocessor='16'
		inumQ='16'
		imaxUsdQ='1'
	elif i ==7:
		isstype='R'
		iaccessU='20'
		iprocessor='4'
		inumQ='5'
		imaxUsdQ='1'
	elif i ==8:
		isstype='R'
		iaccessU='20'
		iprocessor='4'
		inumQ='5'
		imaxUsdQ='1'

	
	if isstype =='R':
	 	N='1'
	elif isstype == 'M':
		N='3'
	elif isstype == 'F':
		N='5'
	#ax=fig.add_subplot(1,6,i)
			
	
	fig = plt.figure()
	ax = fig.add_axes([0.1, 0.1, 0.85, 0.3])
	ax.set_xlabel(r'$U_{\Sigma}$/m (%)',labelpad=-2,fontsize=15)
	ax.set_ylabel('Acceptance Ratio',size=15)
	for j in range(len(schemes)):

		
		ifile=prefix+isstype+"/"+iaccessU+"/"+schemes[j]+"-m"+iprocessor+"-Q"+inumQ+"-max"+imaxUsdQ+"-n"+numtasks[0]+".npy"
		data=np.load(ifile)
		x=data[0,::1]*5
		y=data[1,::1]
		
		if schemes[j]=='MRTA':
			if isstype=='M':
				labelname='MIRROR-SPIN-FF'
			else:
				labelname='MIRROR-SPIN'
		elif schemes[j]=='NBFFDM':
			labelname='NPDBF-NC'
		elif schemes[j]=='NPDBF':
			labelname='NCDBF'
		elif schemes[j]=='DPCP':
			labelname='R-PCP'
		elif schemes[j]=='DNP':
			labelname='R-NPP'
		elif schemes[j]=='DNP+':
			labelname='R-DNP+'
		elif schemes[j]=='DPCP+':
			labelname='R-PCP+'
		elif schemes[j]=='elvDPCP':
			labelname='R-elvPCP'
		else:
			labelname=schemes[j]
		
		
		ax.plot(x, y,
 				'-', 
 			color=colors[j],
 			marker=marker[j], 					
 			markersize=8,
 			markevery=1,
 			fillstyle='none',
 			label=labelname, 					
 			linewidth=1.0, clip_on=False	
 			)
			
		
			
	ax.legend(bbox_to_anchor=(0.5, 1.2),
				loc=10,
				markerscale =1.2,
    			ncol=int(len(schemes)), 
    			borderaxespad=0.,    
    			prop={'size':11},
    			frameon=False)
	
		#ax.set_xticks(np.arange(0,101,20))
		#ax.set_yticks(np.arange(0,1.1,0.2))
	#ax.axis(xmin=-1.5)
	#ax.axis(xmax=101.5)
	#ax.axis(ymin=-.03)
	#ax.axis(ymax=1.03)
		#prop=int(issprop)/10
	#fig.patch.set_alpha(0.)
	#ax.patch.set_alpha(0.)
	ax.grid()	
	#plt.title('('+figlabel[i-1]+') '+'m='+iprocessor+r', $\alpha$='+iaccessU+', r='+inumQ+', Q='+imaxUsdQ+', N='+N,size=15)			
	a='fig/'+'exp2-m='+iprocessor+'-U='+iaccessU+'-r='+inumQ+'-Q='+imaxUsdQ+'-N='+N+'.pdf'
	print a
	plt.savefig(a, format='pdf', transparent=True, bbox_inches="tight")
	plt.gcf().clear()

#plt.show()
sys.exit()


