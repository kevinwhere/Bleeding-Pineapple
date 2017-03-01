"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import math
b = np.arange(0.0, 1.0, 0.001)
s = 1/(((1+b)/2)+np.sqrt((np.power(b,2)+1)/4))
plt.plot(b, s,linewidth=5.0)

plt.xlabel(r'Load Factor $ (\beta) $', fontsize=20)
plt.ylabel('Utilization', fontsize=20)
plt.xticks(size = 14)
plt.yticks(size = 14)
#plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.show()
