README v1.0 / 08 MARCH 2017

# Multi-Mode Tasks Generation

We first generate a set of sporadic tasks. 
The UUniFast method is adopted to generate a set of utilization values with the given goal.
The task periods are generated according to the **log-uniform distribution**[^1].
[^1]: Schedulability test efficiency can be heavily dependent on the number of order of magnitude ranges of task periods (effectively the ratio between the smallest and largest task period). That bias can result if studies do not fully explore appropriate distributions of task periods. For example, choosing task periods at random according to a uniform distribution in the range $[1, 10^6]$ results in 99% of tasks having periods greater than $10^4$, thus the effective ratio of maximum to minimum task period is far less than might be expected (closer to $10^2$ than $10^6$ for small tasksets). To avoid these problems, a **log-uniform** distribution of task periods can be used, with tasksets generated for different ratios of the minimum (Tmin) to the maximum (Tmax) task period.

 The distribution of periods is by default within two orders of magnitude, i.e., $10$ms-$1000$ms. Task relative deadlines are implicit, i.e., $D_i=T_i$. The worst-case execution time is computed accordingly, i.e. $C_i~=T_iU_i$. We then convert a proportion $p$ of tasks to multi-mode tasks and the details are below:

* A multi-mode task has $M$ execution modes
```python
for j in range(numMode):
```
* The generated sporadic task triplet $(C_i,T_i,D_i)$ was assigned to the setting of task mode $\tau_i^1$.
* We use a scaling factor $s$ to assign the parameters of the other modes, i.e., $C_i^{m+1}=s^{m-1}C_i^{m}$ and $T_i^{m+1}=s^{m-1}T_i^{m}$. 
```python
p=iStask['period']*math.pow(scalefac, j)
c=iStask['period']*iStask['utilizatichapter-1on']*math.pow(scalefac, j) 
```
* We randomly choose a mode to have the largest utilization. 
* The worst-case execution times of the remaining modes are adjusted by multiplying them by uniform random values in the range [minCtune,maxCtune].
```python         
if j != iMaxU:      
    c=c*random.uniform(minCtune,maxCtune);
```
* To ensure the discrete time model, we here apply a correction factor on both the generated period and execution time.
```python
s=math.ceil(p)/p
pair['period']=math.ceil(p)  
pair['execution']=c*s
```

| Built-in Functions |
| ------------------- |
| [UUniFast(n,u)](#uuni)|
|[SetGenerate(Pmin,numLog)](#setgen)|
|[MMSetGenerate(numMode,vRatio,gscaleFac)](#mmsetgen)|

####<a id="uuni"></a>UUniFast(_n,u_)
Uniformly generate a list of **n** values with a total value of **u**.

#### <a id="setgen"></a>SetGenerate(_Pmin,numLog_)
Generate a log-uniform distribution of periods, with **numLog** orders of magnitude and the minimum period of **Pmin**, operated on the task set generated from [UUniFast(n,u)](#uuni).

#### <a id="mmsetgen"></a>MMSetGenerate(_numMode,vRatio,gscaleFac_)
Convert a proportion **vRatio** of the genereated tasks to multi-mode tasks, each of which is with **numMode** modes and a scale factor of **gscaleFac**.

## Data Structures (Tasks)

Each multi-mode task is composed of a set of modes. We use data type *dictionary* built into Python to decribe modes.

| Object              		| Data Type                                     |
| -------------------     | -----------------------------------------------       |
| task           | _list_            |
| mode           | _dictionary_             |


The keywords of the dictionary and their meaning are below:

| Keyword              		| Meaning                                     |
| -------------------     | -----------------------------------------------       |
| period           | the period/inter-arrival time of this mode             |
| execution           | the worst-case execution time of this mode             |

**NOTE: we implicitly assume implicit deadlines here, so we don't need deadlines to be specified. Alternaively, one can add deadline as keywords to decribe deadlines.**

### Example 
```python
for itask in tasks:			
	print itask
```
```bash
[{'execution': 0.0054703680453322403, 'period': 2.0}, {'execution': 0.0049247204918443253, 'period': 2.0}, {'execution': 0.0076162508284702349, 'period': 3.0}, {'execution': 0.012200111224485971, 'period': 4.0}, {'execution': 0.014841495809564743, 'period': 6.0}]
```
```python
for itask in tasks:	
	for imode in itask:
		print imode['period']
```
```bash
2.0
2.0
3.0
4.0
6.0
```
# Schedulability Tests for Multi-Mode Tasks 

Available tests are below:

* Demand-based Test under FPT (DT-FPT) `DTest(k,tasks,mode,priortyassigned)`: the response-time analysis(RTA)-based approach using **dynamic programming (DP)** under FPT presented in *Huang and Chen. "Techniques for Schedulability Analysis in Mode Change Systems under Fixed-Priority Scheduling." In RTCSA2015*, see [here](http://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/polynomial-mode-change.pdf), or *Robert I. Davis et al. "Schedulability tests for tasks with Variable Rate-dependent Behaviour under fixed priority scheduling."*

* FPTVRBL2 `VRBL2(mode,Tasks)`: the utilization-based test under FPT based on Eq. (7) and (8) in *Robert I. Davis et al. "Schedulability tests for tasks with Variable Rate-dependent Behaviour under fixed priority scheduling."*
* Quadratic Test for fixed-priority task-level `QT(mode,HPTasks)`: Theorem 1 presented in *Huang and Chen. "Techniques for Schedulability Analysis in Mode Change Systems under Fixed-Priority Scheduling." In RTCSA2015*, see [here](http://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/polynomial-mode-change.pdf)
* Quadratic Test for fixed-priority mode-level `modeQT(mode,tasks)`: Theorem 4 presented in *Huang and Chen. "Techniques for Schedulability Analysis in Mode Change Systems under Fixed-Priority Scheduling." In RTCSA2015*, see [here](http://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/polynomial-mode-change.pdf)

**NOTE: the RTA-based approach can only be used when the critical instant exists, i.e. under the FPT case.**


## Dynamic Programming 
Suppose we are given a limit of total weight, and a set of items. Each item has its *weight (period)* and *profit (execution)*, and can be used unboundedly. What is the *largest* profit of items we can select? This problem can be solved by using **dynamic programming (DP)**.

```python
def dp_recursive(t,dpTB,dirtTB,incM,idptask,tasks):
	choice=[]

	if t ==0:
		dirtTB[0]=0
		dpTB[t]=0

	if dirtTB[t]==0:
		return dpTB[t]

	for i in range(incM):
		imode=tasks[idptask][i]
		if imode['period']<=t:
			## dp table look one time unit behind when float
			## safe
			choice.append(dp_recursive(t-int(imode['period']),dpTB,dirtTB,incM,idptask,tasks)+imode['execution'])
		else:
			choice.append(0)

		dirtTB[t]=0
		dpTB[t]=max(choice)
	return dpTB[t]
```
The bulk of the work in this function is done by the loop that starts on `for i in range(incM):`.

# Optimal Priority Assignment
Checking the FPT feasibility of a multi-mode task set was achieved by using the **Audsley's Algorithm**, a.k.a. **Optimal Priority Assignment (OPA)**. Its source code for mode-level fixed-priority scheduling is attached below (the one for task-level FP scheduling is also similar): 

```python

def modeAudsley(tasks,scheme):
	num_modes=0
	## to know how many priority levels we need to decide
	for itask in tasks:
		num_modes+=len(itask)
		## put an attribute for each mode used as an indicator for whether or not its priority level is assigned
		for imode in itask:
			imode['ifassigned']=False		
	## assign priority levels to modes, from the lowest to the highest
	for plevel in range(num_modes):
	
		canAssign=0
		for i in range(len(tasks)):
			primeTasks=tasks[:i]+tasks[i+1:]		

			for imode in tasks[i]:
				##ignore modes whose priority levels have been decided
				if imode['ifassigned']==True:
					continue
				## checking if this mode can be assigned to this priority level by QT test
				if tests.modeQT(imode,primeTasks):										
					imode['ifassigned']=True
					canAssign=1
					break
				else:
					continue
			## greedily assign the first mode feasible to this priority level
			if canAssign==1:
				break
		## if none of the modes can be assigned at this priority level, return unscheduable
		if canAssign==0:
			return False
	return True
```

# Plotting

To genereate plots from our evaluations, we use [Matplotlib](http://matplotlib.org/ ""), a widely-used Python plotting library for 2D-graphics.


### Create a virtual outer subsplot for putting big x-ylabel 

To make the figures space-efficient and concise, what we typically did is to put several figures into one and leave out labels. This can be done by creating a virtual subsplot `fig.add_subplot`:

```python
ax=fig.add_subplot(111)
fig.subplots_adjust(top=0.9,left=0.1,right=0.95,hspace =0.3)

ax.set_xlabel(r'$U_{\Sigma }/M$',labelpad=-2,size=15)
ax.set_ylabel('Acceptance Ratio',size=15)
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

for iprocessor in modes:
	for iplog in periodlogs:		
			ax=fig.add_subplot(len(modes),len(periodlogs),i)
```
### You read what you store
```python
## multimode.py

plotfile=prefixdata+"/m/"+imode+"/"+ischeme
np.save(plotfile,np.array([x,y]))
```

```python
## multimode-plot.py

ifile=prefix+"m/"+iprocessor+"/"+schemes[j]+".npy"			
data=np.load(ifile)
```
### Make the curves foregrounded  `clip_on=False`

```python
marker = [ '*','o','+','D','p','s']
colors = ['k','y','c','k','k','y']

ax.plot(x, y,
 		'-', 
 		color=colors[j],
 		marker=marker[j],
 		markersize=8,
 		markevery=1,
 		fillstyle='none',
 		label=name, 					
 		linewidth=1.0, clip_on=False)
```
