"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools

var1="m/5/"
var2="m/8/"
var3="m/10/"
f1 = open(var1+'fig-FPTDT', 'r')
f2 = open(var1+'fig-FPTQB', 'r')
f3= open(var1+'fig-FPTVRBL2', 'r')
f4 = open(var1+'fig-RMQBL', 'r')
f5= open(var1+'fig-RMQBP', 'r')


f6 = open(var2+'fig-FPTDT', 'r')
f7 = open(var2+'fig-FPTQB', 'r')
f8= open(var2+'fig-FPTVRBL2', 'r')
f9 = open(var2+'fig-RMQBL', 'r')
f10= open(var2+'fig-RMQBP', 'r')


f11= open(var3+'fig-FPTDT', 'r')
f12= open(var3+'fig-FPTQB', 'r')
f13= open(var3+'fig-FPTVRBL2', 'r')
f14= open(var3+'fig-RMQBL', 'r')
f15= open(var3+'fig-RMQBP', 'r')

f16= open(var1+'fig-RMTB', 'r')
f17= open(var2+'fig-RMTB', 'r')
f18= open(var3+'fig-RMTB', 'r')

f19= open(var1+'fig-RMQB', 'r')
f20= open(var2+'fig-RMQB', 'r')
f21= open(var3+'fig-RMQB', 'r')
x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []
x5 = []
y5 = []
x6 = []
y6 = []
x7 = []
y7 = []
x8 = []
y8 = []
x9 = []
y9 = []
x10 = []
y10 = []
x11 = []
y11 = []
x12 = []
y12 = []
x13 = []
y13 = []
x14 = []
y14 = []
x15 = []
y15 = []
x16 = []
y16 = []
x17 = []
y17 = []
x18 = []
y18 = []
x19 = []
y19 = []
x20 = []
y20 = []
x21 = []
y21 = []
#x1 = np.linspace(0.0, 5.0)
#x2 = np.linspace(0.0, 2.0)

#y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
#y2 = np.cos(2 * np.pi * x2)
lines= f1.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x1.append(float(p[0]))
		y1.append(float(p[1]))

lines= f2.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x2.append(float(p[0]))
		y2.append(float(p[1]))

lines= f3.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x3.append(float(p[0]))
		y3.append(float(p[1]))		

lines= f4.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x4.append(float(p[0]))
		y4.append(float(p[1]))

lines= f5.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x5.append(float(p[0]))
		y5.append(float(p[1]))

lines= f6.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x6.append(float(p[0]))
		y6.append(float(p[1]))
lines= f7.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x7.append(float(p[0]))
		y7.append(float(p[1]))

lines= f8.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x8.append(float(p[0]))
		y8.append(float(p[1]))

lines= f9.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x9.append(float(p[0]))
		y9.append(float(p[1]))
lines= f10.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x10.append(float(p[0]))
		y10.append(float(p[1]))

lines= f11.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x11.append(float(p[0]))
		y11.append(float(p[1]))

lines= f12.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x12.append(float(p[0]))
		y12.append(float(p[1]))
lines= f13.readlines()

for line in lines:
	print line
	p = line.split()
	if p:
		x13.append(float(p[0]))
		y13.append(float(p[1]))
lines= f14.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x14.append(float(p[0]))
		y14.append(float(p[1]))
lines= f15.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x15.append(float(p[0]))
		y15.append(float(p[1]))
lines= f16.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x16.append(float(p[0]))
		y16.append(float(p[1]))
lines= f17.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x17.append(float(p[0]))
		y17.append(float(p[1]))
lines= f18.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x18.append(float(p[0]))
		y18.append(float(p[1]))
lines= f19.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x19.append(float(p[0]))
		y19.append(float(p[1]))
lines= f20.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x20.append(float(p[0]))
		y20.append(float(p[1]))
lines= f21.readlines()
for line in lines:
	print line
	p = line.split()
	if p:
		x21.append(float(p[0]))
		y21.append(float(p[1]))
f1.close()	
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()
f9.close()
f10.close()
f11.close()
f12.close()
f13.close()
f14.close()
f15.close()
f16.close()
f17.close()
f18.close()
f19.close()
f20.close()
f21.close()
#plt.subplot(2, 1, 1)




#plt.plot(x4, y4, 'yx-', label='BUT')
# plt.plot(x4, y4, 'mo-', label='MUT')
#plt.title('Success ratio for n = 10, D = T with different m')

#plt.xticks(np.arange(min(x1), max(x1), 5))

fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.85, 0.3])
ax1.set_xlabel(r'$U_{\Sigma }/M$ (%)',labelpad=-2,fontsize=15)
ax1.set_ylabel('Acceptance Ratio',size=15)
#ax=fig.add_subplot(111)
#ax1=fig.add_subplot(311)
#ax2=fig.add_subplot(312)
#ax3=fig.add_subplot(313)
marker = itertools.cycle(('o', 'v', '+', 's')) 
colors = itertools.cycle(('r','r','k','k')) 
ax1.plot(x2, y2,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QT-FPT',linewidth=1.0, clip_on=False)

ax1.plot(x1, y1,'--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='DT-FPT',linewidth=1.0, clip_on=False)
#ax1.plot(x3, y3,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='FPTVRBL2',linewidth=1.0, clip_on=False)
#ax1.plot(x19, y19,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='RMQBF',linewidth=1.0, clip_on=False)
ax1.plot(x4, y4,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QB-RM',linewidth=1.0, clip_on=False)
ax1.plot(x5, y5,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QT-RM',linewidth=1.0, clip_on=False)

#ax1.plot(x16, y16,'--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='RMTBL',linewidth=1.0, clip_on=False)



#ax1.plot(x10, y10,'yx--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='MUT',linewidth=1.0, clip_on=False)
# plt.ylabel('m = 5')
#ax1.legend(loc=2,fontsize=9)
ax1.legend(bbox_to_anchor=(0.5, 1.2),
						loc=10,
						markerscale =1.5,
    					ncol=6, 
    					borderaxespad=0.,    
    					prop={'size':13},frameon=False)
ax1.grid()
ax1.set_xlim(xmin=0,xmax=100)
plt.savefig('fig/RMFPT-m1.pdf', format='pdf', transparent=True, bbox_inches="tight")
plt.gcf().clear()


fig = plt.figure()
ax2 = fig.add_axes([0.1, 0.1, 0.85, 0.3])
ax2.set_xlabel(r'$U_{\Sigma }/M$ (%)',labelpad=-2,fontsize=15)
ax2.set_ylabel('Acceptance Ratio',size=15)

ax2.plot(x7, y7,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QT-FPT',linewidth=1.0, clip_on=False)
ax2.plot(x6, y6,'--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='DT-FPT',linewidth=1.0, clip_on=False)

#ax2.plot(x8, y8,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='FPTVRBL2',linewidth=1.0, clip_on=False)
#ax2.plot(x20, y20,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='RMQBF',linewidth=1.0, clip_on=False)
ax2.plot(x9, y9,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QB-RM',linewidth=1.0, clip_on=False)
ax2.plot(x10, y10,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QT-RM',linewidth=1.0, clip_on=False)

#ax2.plot(x17, y17,'--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='RMTBL',linewidth=1.0, clip_on=False)

ax2.legend(bbox_to_anchor=(0.5, 1.2),
						loc=10,
						markerscale =1.5,
    					ncol=6, 
    					borderaxespad=0.,    
    					prop={'size':13},frameon=False)

#ax2.plot(x11, y11,'yx--',label='MUT',linewidth=1.0, clip_on=False)
# plt.ylabel('m =10')
#ax2.legend(loc=2,fontsize=9)
ax2.grid()

ax2.set_xlim(xmin=0,xmax=100)

plt.savefig('fig/RMFPT-m2.pdf', format='pdf', transparent=True, bbox_inches="tight")
plt.gcf().clear()



fig = plt.figure()
ax3 = fig.add_axes([0.1, 0.1, 0.85, 0.3])
ax3.set_xlabel(r'$U_{\Sigma }/M$ (%)',labelpad=-2,fontsize=15)
ax3.set_ylabel('Acceptance Ratio',size=15)
ax3.plot(x12, y12,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QT-FPT',linewidth=1.0, clip_on=False)
ax3.plot(x11, y11,'--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='DT-FPT',linewidth=1.0, clip_on=False)

#ax3.plot(x13, y13,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='FPTVRBL2',linewidth=1.0, clip_on=False)
#ax3.plot(x21, y21,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='RMQBF',linewidth=1.0, clip_on=False)
ax3.plot(x14, y14,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QB-RM',linewidth=1.0, clip_on=False)
ax3.plot(x15, y15,'-',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='QT-RM',linewidth=1.0, clip_on=False)
ax3.legend(bbox_to_anchor=(0.5, 1.2),
						loc=10,
						markerscale =1.5,
    					ncol=6, 
    					borderaxespad=0.,    
    					prop={'size':13},frameon=False)
#ax3.plot(x18, y18,'--',marker=marker.next(),color=colors.next(),markersize=8,markevery=3,fillstyle='none',label='RMTBL',linewidth=1.0, clip_on=False)
#
##ax3.plot(x12, y12,'yx--',label='MUT',linewidth=1.0, clip_on=False)
#ax3.legend(loc=2,fontsize=9)
ax3.grid()
#ax1.set_ylabel('P= 20%')
#ax2.set_ylabel('P= 50%')
#ax3.set_ylabel('P= 80%')
ax3.set_xlim(xmin=0,xmax=100)
#
#ax4.plot(x10, y10,'o-', label='DT',linewidth=1.0, clip_on=False)
#ax4.plot(x11, y11,'s-',label='QB',linewidth=1.0, clip_on=False)
#ax4.plot(x12, y12,'D-',label='LQB',linewidth=1.0, clip_on=False)
##ax4.plot(x12, y12,'yx--',label='MUT',linewidth=1.0, clip_on=False)
#ax4.legend(loc=2)
#ax4.grid()
#ax4.set_ylabel('M= 20')
#ax4.set_xlim(xmin=0,xmax=100)



ax3.set_xlabel('Utilization (%)',size=18)
ax3.set_ylabel('Acceptance Ratio',size=18,labelpad=20)


#ax.spines['top'].set_color('none')
#ax.spines['bottom'].set_color('none')
#ax.spines['left'].set_color('none')
#ax.spines['right'].set_color('none')
#ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
#plt.subplot(2, 1, 2)
#plt.plot(x2, y2, 'r.-')
#plt.xlabel('time (s)')
#plt.ylabel('Undamped')

plt.savefig('fig/RMFPT-m3.pdf', format='pdf', transparent=True, bbox_inches="tight")
plt.gcf().clear()
#plt.show()
#plt.close()
