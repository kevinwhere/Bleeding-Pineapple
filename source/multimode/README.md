README v1.0 / 07 MARCH 2017

# Multi-Mode Tasks Generation

We first generate a set of sporadic tasks. 
The UUniFast method is adopted to generate a set of utilization values with the given goal.
The task periods are generated according to the **exponential distribution**.
 The distribution of periods is by default within two orders of magnitude, i.e., $10$ms-$1000$ms. Task relative deadlines are implicit, i.e., $D_i=T_i$. The worst-case execution time is computed accordingly, i.e. $C_i~=T_iU_i$. We then convert a proportion $p$ of tasks to multi-mode tasks and the details are below:

* A multi-mode task has $M$ execution modes
```python
for j in range(numMode):
```
* The generated sporadic task triplet $(C_i,T_i,D_i)$ was assigned to the setting of task mode $\tau_i^1$.
* We use a scaling factor $s$ to assign the parameters of the other modes, i.e., $C_i^{m+1}=s^{m-1}C_i^{m}$ and $T_i^{m+1}=s^{m-1}T_i^{m}$. 
```python
p=iStask['period']*math.pow(scalefac, j)
c=iStask['period']*iStask['utilization']*math.pow(scalefac, j) 
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
| UUniFast(numTasks,uTotal)|
|SetGenerate(Pmin,numLog)|


## Data Structures
*list*
We use data type *dictionary* built into Python to decribe modes.

| Keyword              		| Meaning                                     |
| -------------------     | -----------------------------------------------       |
| period           | the period/inter-arrival time of this mode             |
| execution           | the worst-case execution time of this mode             |

**NOTE: we implicitly assume implicit deadlines here, so we don't need deadlines to be specified. Alternaively, one can add deadline as keyword to decribe deadlines.**

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
Suppose we are given a limit of total weight, and a set of items. Each item has its *weight (period)* and *profit (execution)*, and can be used unboundedly. What is the *largest* profit of items we can select.

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

```
#!python

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