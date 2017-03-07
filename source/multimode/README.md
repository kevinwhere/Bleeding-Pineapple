README v1.0 / 06 MARCH 2017

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

# Schedulability Tests for Multi-Mode Tasks 

Available tests are listed as follows:

* Demand-based Test under FPT (DT-FPT) `DTest(k,tasks,mode,priortyassigned)`: the response-time analysis(RTA)-based approach using **dynamic programming (DP)** under FPT presented in Section III.D.

**NOTE: the RTA-based approach can only be used when the critical instant exists.**

* FPTVRBL2 `VRBL2(mode,Tasks)`: the utilization-based test under FPT based on Eq. (7) and (8) in~\cite{davis2008response,DBLP:conf/rtas/DavisFPS14}
* Quadratic Test `RMQT(tasks,scheme)`: Theorem~\ref{theorem:beta-utilization-bound}.


## Dynamic Programming 
a recursive function, even though we started with a recursive solution to this problem.


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