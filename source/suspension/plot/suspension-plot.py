"""
Simple demo with multiple subplots.
"""
from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt


sstype= ['S','M','L']
ssofftypes = ['R']
ssoprops = ['2','5','8']
schemes=['SCEDF','EDA','MIP','SEIFDA-minD-1','SEIFDA-maxD-1','SEIFDA-PBminD-1','NC']
figlabel=['a','b','c','d','e','f','g','h','i']
prefix="data/"

#'o', 'v','+' ,'x','*'
marker = ['o', 'v','+','*','D','x','+']
#'b','r','g','k','y'
colors = ['b','r','k','g','c','y','m','b'] 

fig=plt.figure()
## create a virtual outer subsplot for putting big x-ylabel 
ax=fig.add_subplot(111)
fig.subplots_adjust(top=0.9,left=0.1,right=0.95,hspace =0.3)

ax.set_xlabel('Utilization (%)',size=15)
ax.set_ylabel('Acceptance Ratio',size=15)
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

i=1
for isstype in sstype:
	for issofftypes in ssofftypes:
	#for issoprops in ssoprops:	
			#ax=fig.add_subplot(len(sstype),len(ssofftypes),i)
			ax=fig.add_subplot(len(ssofftypes),len(sstype),i)
			j=0
			for ischeme in schemes:
				
				ifile=prefix+isstype+"/"+issofftypes+"/"+ischeme+".npy"
				#ifile=prefix+isstype+"/"+issoprops+"/"+ischeme+".npy"
				data=np.load(ifile)
				print len(data[0][0::1])
				x=data[0][0::1]*5
				y=data[1][0::1]
				ax.plot(x, y,
 					'-', 
 					color=colors[j],
 					marker=marker[j],
 					markersize=4,
 					markevery=1,
 					fillstyle='none',
 					label=ischeme,
 					linewidth=1.0,
 					clip_on=False)
				if i==1:
					ax.legend(bbox_to_anchor=(1.8, 1.3),
						loc=10,
						markerscale =1.5,
    					ncol=len(schemes), 
    					borderaxespad=0.,    
    					prop={'size':10})
				j+=1
			
			ax.set_title('('+figlabel[i-1]+') '+'sslen:'+isstype+',sstype:'+issofftypes,size=10, y=0.98)
			#ax.set_title('('+figlabel[i-1]+') '+'sslen:'+isstype+',prop:.'+issoprops,size=10, y=0.98)			
			ax.grid()
			i+=1

plt.show()
sys.exit()


