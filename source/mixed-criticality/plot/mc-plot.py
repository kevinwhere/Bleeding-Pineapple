"""
Simple demo with multiple subplots.
"""
from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
#import matplotlib.font_manager as font_manager

#view available fonts
# prop = font_manager.FontProperties(fname='/usr/share/fonts/TTF/OpenSans-Regular.ttf')
# rcParams['font.family'] = prop.get_name()
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Tahoma']
processors=['4']
Ratio=['20','10','5']
sstype=['S','M','L']
periodlogs=['2']
numtasks=['10']

#schemes=['BCL','FF','BAK','OUR-LB','OUR-RTA','Guan']
#schemes=['FF-DM','BF-DM','WF-DM']
#schemes=['MIRROR-RAS+','MIRROR-RAS=','MIRROR-RAS-']
#schemes=['MIRROR-FF','MIRROR-BF','MIRROR-WF']
#schemes=['MRTA','MIRROR']
schemes=['RMCL','EDF-VD','EDF-VD2','DBF']
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
marker = [ 'd','v','x','o','+','D','o','+','D']
#marker = [ 'o','+','D','v']
#'g','b','r','k','k','y'
#colors = itertools.cycle(('r','y','k')) 
#colors = ['c','k','y']
colors = ['b','r','y','c','k','y','c','k','m','y']
numCL=['2']
fig=plt.figure()


## create a virtual outer subsplot for putting big x-ylabel 
ax=fig.add_subplot(111)
fig.subplots_adjust(top=0.9,left=0.1,right=0.95,hspace =0.3)

ax.set_xlabel(r'$U_{\Sigma}$/m (%)',labelpad=-2,fontsize=15)
ax.set_ylabel('Acceptance Ratio',size=15)
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

for inumCL in numCL:
	i=1	
	for isstype in sstype:
		ax=fig.add_subplot(1,3,i)
		
				
		for j in range(len(schemes)):
					
			ifile=prefix+"CL/"+inumCL+"/"+isstype+"/"+schemes[j]+".npy"
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
 				linewidth=1.0, 			
 				)
				
			
			if i ==1:				
				ax.legend(bbox_to_anchor=(1.6, 1.3),
					loc=10,
					markerscale =1.3,
    				ncol=len(schemes), 
    				borderaxespad=0.,    
    				prop={'size':12},
    				frameon=False)
		
			#ax.set_xticks(np.arange(0,101,20))
			#ax.set_yticks(np.arange(0,1.1,0.2))
			#ax.axis(xmin=0)
			#ax.axis(xmax=100)
			#ax.axis(ymin=0)
			#ax.axis(ymax=1)
			#prop=int(issprop)/10
		ax.grid()	
		ax.set_title('('+figlabel[i-1]+') ',size=10)
		i=i+1

	a='fig/'+'CL='+inumCL+'.pdf'
	plt.savefig(a, format='pdf', transparent=True, bbox_inches="tight")
	plt.gcf().clear()

#plt.show()
sys.exit()

