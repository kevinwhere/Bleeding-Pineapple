README v1.0 / 09 MAY 2017

# Synchronization Tasks Generation

We first generate a set of sporadic tasks. 
The UUniFast method is adopted to generate a set of utilization values with the given goal.
The task periods are generated according to the **log-uniform distribution**[^1].
[^1]: Schedulability test efficiency can be heavily dependent on the number of order of magnitude ranges of task periods (effectively the ratio between the smallest and largest task period). That bias can result if studies do not fully explore appropriate distributions of task periods. For example, choosing task periods at random according to a uniform distribution in the range $[1, 10^6]$ results in 99% of tasks having periods greater than $10^4$, thus the effective ratio of maximum to minimum task period is far less than might be expected (closer to $10^2$ than $10^6$ for small tasksets). To avoid these problems, a **log-uniform** distribution of task periods can be used, with tasksets generated for different ratios of the minimum (Tmin) to the maximum (Tmax) task period.



 The distribution of periods is by default within two orders of magnitude, i.e., $10$ms-$1000$ms. Task relative deadlines are implicit, i.e., $D_i=T_i$. The worst-case computation time is computed accordingly, i.e. $C_i^C=T_iU_i$. We then convert the genereated tasks to tasks with synchronizations and the details are below:



```python
X=StaffordRandFixedSum(numTasks, uC, 1)
```
```python
pair['ncriutilization']=i
pair['period']=p
pair['execution']=i*p
```
+ in the case the program is structured to one path,  We use UUnifast to generate a vector of computation segments, according to a uniform distribution.

```python
pair['C']=seg_UUniFast(2,pair['execution'])
```


| Built-in Functions |
| ------------------- |
| [StaffordRandFixedSum(n,u)](#rfs)|
| [segUUniFast(n,total)](#seguuni)|
|[SSS_generate(ssU,n,maxUsdRes,numCritical)](#sssetgen)|
|[AAA_generate(totRes,maxUsdQ,numCritical)](#aaagen)|

####<a id="rfs"></a>StaffordRandFixedSum(_n,u_)
Return a list of **n** values with a total value of **u** in a uniform distribution, each of which is no more than 1.

####<a id="seguuni"></a>segUUniFast(_n,u_)
Return a list of **n** values with a total value of **u** in a uniform distribution.



#### <a id="sssetgen"></a>SSS_generate(ssU,n,maxUsdRes,numCritical)
Generate a vector of **n** values with a total of **ssU** in a uniform distribution, which determine how much each task will utilize the shared resoruces in utilization. We ensure each task with $A_i+C_i<=1$

#### <a id="aaagen"></a>AAA_generate(totRes,maxUsdQ,numCritical)
Generate a vector of **maxUsdQ** values with a total of **totRes** in a uniform distribution, which determine how much each resource will be utilized by this task in utilization, i.e., $U_{i,q}$ 
```python
SS=seg_UUniFast(maxUsdQ,itask['accUtilization'])
```
Then, we determine which of shared resources this task may access.

```python
X=random.sample(xrange(totRes), maxUsdRes)
```
Last, we set the access time accordingly, i.e., $A_{i,q}=T_iU_{i,q}$
## Data Structures (Tasks)

A task set is composed of a set of tasks. We use data type *dictionary* built into Python to decribe each suspension task.

| Object         | Data Type       	  |
| -------------  | -------------------|
| tasks          | _list_             |
| task           | _dictionary_       |
| C           | _list_             |
| resGraph           | _dictionary_             |
| resEdge        | _list_             |

The keywords of the dictionary and their meaning are below:

| Keyword        | Meaning                                  |
| -------------  | -----------------------------------------------|
| period         | the period/inter-arrival time of this task             |
| execution      | the total computation time of this task (excluding the time on resource access)   |
| accExecution       | the total resource access time of this task   |
| resEdge        | a list of resources this task may access   |
| C           | a list of the upper bounds on each computation segment   									|
| resGraph           | a list of the upper bounds on each resource access   |



**NOTE: we implicitly assume implicit deadlines here, so we don't need deadlines to be specified. Alternaively, one can add deadline as keywords to decribe deadlines.**

### Example 
```python
for itask in tasks:			
	print itask
```
```bash
{'numCritical': 1, 'ncriutilization': 4.4418970387358962e-05, 'C': [1.5266608362070544e-05, 0.00013328956401820489], 'maxUsdRes': 1, 'resEdge': [3], 'accUtilization': 0.00014400728283304499, 'period': 3.3444307935276347, 'utilization': 0.00018842625322040396, 'accExecution': 0.00048162239119907922, 'execution': 0.00014855617238027544, 'resGraph': [{'totacc': 0}, {'totacc': 0}, {'totacc': 0}, {'totacc': 0.00048162239119907922, 'maxacc': 0.00048162239119907922}]}
```
Here is a task that may access resource $R_3$ with an upper bound on the total access time of 0.00048162239119907922 and an upper bound on the computation time $C_i$ of 0.00014855617238027544, where two segments are 1.5266608362070544e-05 and  0.00013328956401820489 if the program is structured to one path.

# Schedulability tests for synchrnoization tasks 

Available tests are below:


* PIP `PIP.PIP(tasks)`: the suspension-oblivious approach by converting suspension time into computation time; The original task system is schedulable if the total utilization of the transformed task system is no greater than 1.
* MrsP `MrsP.MrsP(tasks)`: An enforcement approach using Equal-Deadline Assignment (EDA)
	under linear demand bound approximations, in Theorem 8 in *Jian-Jia Chen and Cong Liu. "Fixed-Relative-Deadline Scheduling of Hard Real-Time Tasks with Self-Suspensions" In Proceedings of the 35th IEEE Real-Time Systems Symposium (RTSS)*

* MPCP `MPCP.MPCP(tasks,scheme)`: a greedy approch, *Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen and Cong Liu. "Uniprocessor Scheduling Strategies for Self-Suspending Task Systems." In Proceedings of the 24th International Conference on Real-Time Networks and Systems (RTNS)*, see [here](http://dl.acm.org/ft_gateway.cfm?id=2997497\&ftid=1804918\&dwn=1\&CFID=691780547\&CFTOKEN=64912419).
* PCP-ROP-FF-RM `ROP.ReasonableAllocation(tasks)`: The proposed approach in Section~\ref{sec:LP}, *Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen and Cong Liu. "Uniprocessor Scheduling Strategies for Self-Suspending Task Systems." In Proceedings of the 24th International Conference on Real-Time Networks and Systems (RTNS)*, see [here](http://dl.acm.org/ft_gateway.cfm?id=2997497\&ftid=1804918\&dwn=1\&CFID=691780547\&CFTOKEN=64912419).

* FRDEDF=PBminD=2-PCP-FF-SLM `ROP.ReasonableAllocation(tasks)`: The proposed approach in Section~\ref{sec:LP}, *Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen and Cong Liu. "Uniprocessor Scheduling Strategies for Self-Suspending Task Systems." In Proceedings of the 24th International Conference on Real-Time Networks and Systems (RTNS)*, see [here](http://dl.acm.org/ft_gateway.cfm?id=2997497\&ftid=1804918\&dwn=1\&CFID=691780547\&CFTOKEN=64912419)

* NPDBF `NPDBF(tasks)`: The necessary condition. We compared to the necessary condition to know how much we may lose to a
theoretical optimal algorithm in the worst case. 




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
## suspension.py

plotfile=prefixdata+"/m/"+imode+"/"+ischeme
np.save(plotfile,np.array([x,y]))
```

```python
## suspension-plot.py

ifile=prefix+isstype+"/"+issofftypes+"/"+ischeme+".npy"		
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
