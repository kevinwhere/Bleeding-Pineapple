README v1.0 / 17 MAY 2017

# Synchronization Tasks Generation

We first generate a set of sporadic tasks. 
The UUniFast method is adopted to generate a set of utilization values with the given goal.
The task periods are generated according to the **log-uniform distribution**.




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
Return a list of #**n** values with a total value of **u** in a uniform distribution, each of which is no more than 1.

####<a id="seguuni"></a>segUUniFast(_n,u_)
Return a list of #**n** values with a total value of **u** in a uniform distribution.



#### <a id="sssetgen"></a>SSS_generate(ssU,n,maxUsdRes,numCritical)
Generate a vector of #**n** values with a total of **ssU** in a uniform distribution, which determine how much each task will utilize the shared resoruces in utilization. We ensure each task with $A_i+C_i<=1$

#### <a id="aaagen"></a>AAA_generate(totRes,maxUsdQ,numCritical)
Generate a vector of #**maxUsdQ** values with a total of **totRes** in a uniform distribution, which determine how much each resource will be utilized by this task in utilization, i.e., $U_{i,q}$ 
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


* PIP `PIP.PIP(tasks)`: the Priority Inheritance Protocol (PIP)
* MrsP `MrsP.MrsP(tasks)`: the Multiprocessor resource sharing Protocol
(MrsP) along with the Synchronization-Aware Partitioning Algorithm (SPA).

* MPCP `MPCP.MPCP(tasks,scheme)`: the Multiprocessor Priority Ceiling Protocol
(MPCP) along with the SPA.
* ROP-PCP-FF-RM `ROP.ReasonableAllocation(tasks)`: the Resource-Oriented Protocol using PCP

* FRDFP-PCP-FF-SLM `ROP.ReasonableAllocation(tasks)`: ROP using Period Enforcement, FP on each application processor

* FRDEDF=PBminD=2-PCP-FF-SLM `ROP.ReasonableAllocation(tasks)`: ROP using Period Enforcement, EDF on each application processor

* NPDBF `NPDBF(tasks)`: The necessary condition. 




# Plotting

To genereate plots from our evaluations, we use [Matplotlib](http://matplotlib.org/ ""), a widely-used Python plotting library for 2D-graphics.

# Parallel Version Using Joblib 

```

from joblib import Parallel, delayed
import multiprocessing
inputs = range(10)

def processInput(i):
    return i * i

num_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in inputs)
```
https://blog.dominodatalab.com/simple-parallelization/
http://stsievert.com/blog/2014/07/30/simple-python-parallelism/

| Scheme         | serial time (s)       	  | parallel time (s)      	  | Speedup       	  |
| -------------  | -------------------|-------------------|------------------|
| FRDFP-PCP-FF-SLM          | 79             | 42             |1.88             |


