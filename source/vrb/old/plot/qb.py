"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import math
b = np.arange(0.0, 1.0, 0.001)
s = 1-(2*b)+b**2
y = 0.75-b
c= 0.82-b
d= 2/(1+b)-1
plt.plot(b, s, 'r',label='Quadratic Bound (QB)',linewidth=4.0)
plt.plot(b, y ,'b',label='Total Utilization Bound',linewidth=4.0)
plt.plot(b, c ,'y--',label='L&L Bound',linewidth=4.0)
plt.plot(b, d ,'m--',label='HP Bound',linewidth=4.0)
plt.xlabel('$U_1$', fontsize=20)
plt.ylabel('$U_2$', fontsize=20)
plt.ylim(ymin=0,ymax=1)
#plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.xticks(size = 14)
plt.yticks(size = 14)
plt.legend(prop={'size':20})
plt.show()
