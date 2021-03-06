"""
Simple demo with multiple subplots.
"""
from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt


modes=['5','8','10']
periodlogs=['2']
schemes=['QT-RM','QT-OPA']
figlabel=['a','b','c','d','e','f','g','h','i']
prefix="data/"


marker = [ 's','*','+','D','p','s']
#'g','b','r','k','k','y'
#colors = itertools.cycle(('r','y','k')) 
colors = ['k','y','c','k','k','y']


# fig=plt.figure()
# ## create a virtual outer subsplot for putting big x-ylabel 
# ax=fig.add_subplot(111)
# fig.subplots_adjust(top=0.9,left=0.1,right=0.95,hspace =0.3)

# ax.set_xlabel(r'$U_{\Sigma }/M$ (%)',labelpad=-2,size=15)
# ax.set_ylabel('Acceptance Ratio',size=15)
# ax.spines['top'].set_color('none')
# ax.spines['bottom'].set_color('none')
# ax.spines['left'].set_color('none')
# ax.spines['right'].set_color('none')
# ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

i=1
for iprocessor in modes:
	for iplog in periodlogs:		
		fig = plt.figure()
		ax = fig.add_axes([0.1, 0.1, 0.85, 0.3])
		ax.set_xlabel(r'$U_{\Sigma}$ (%)',labelpad=-2,fontsize=15)
		ax.set_ylabel('Acceptance Ratio',size=15)
			

		for j in range(len(schemes)):
			#ifile=prefix+"m/"+iprocessor+"/P/"+iplog+"/"+ischeme+".npy"
			ifile=prefix+"m/"+iprocessor+"/"+schemes[j]+".npy"			
			data=np.load(ifile)
			x=data[0,::1]*5
			y=data[1,::1]
			#data=np.load(ifile)
			#x=data[0,:]/100
			#y=data[1,:]
			name=schemes[j]
			if name == 'QT-FPT':
				name='QT-FPT-OPA'
			elif  name == 'QT-RM':
				name='QT-RM'
			elif  name == 'QT-OPA':
				name='QT-FPM-OPA'
			ax.plot(x, y,
 				'-', 
 				color=colors[j],
 				marker=marker[j],
 				markersize=8,
 				markevery=1,
 				fillstyle='none',
 				label=name, 					
 				linewidth=1.0, clip_on=False)
			
			ax.legend(bbox_to_anchor=(0.5, 1.1),
					loc=10,
					markerscale =1.3,
    				ncol=int(len(schemes)), 
    				borderaxespad=0.,    
    				prop={'size':12},
    				frameon=False)
			j=j+1
			#ax.axis(xmin=0.3)
		#prop=int(issprop)/10
		
		#ax.set_title('('+figlabel[i-1]+') '+'M='+iprocessor,size=10)			
		ax.grid()
		i+=1
		name='fig/'+'MM-OPA-m='+iprocessor+'.pdf'
		plt.savefig(name, format='pdf', transparent=True, bbox_inches="tight")
		plt.gcf().clear()




