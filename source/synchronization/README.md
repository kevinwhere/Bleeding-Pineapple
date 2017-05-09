README v1.0 / 20 APRIL 2017

# Synchronization Tasks Generation

We first generate a set of sporadic tasks. 
The UUniFast method is adopted to generate a set of utilization values with the given goal.
The task periods are generated according to the **log-uniform distribution**[^1].
[^1]: Schedulability test efficiency can be heavily dependent on the number of order of magnitude ranges of task periods (effectively the ratio between the smallest and largest task period). That bias can result if studies do not fully explore appropriate distributions of task periods. For example, choosing task periods at random according to a uniform distribution in the range $[1, 10^6]$ results in 99% of tasks having periods greater than $10^4$, thus the effective ratio of maximum to minimum task period is far less than might be expected (closer to $10^2$ than $10^6$ for small tasksets). To avoid these problems, a **log-uniform** distribution of task periods can be used, with tasksets generated for different ratios of the minimum (Tmin) to the maximum (Tmax) task period.



 The distribution of periods is by default within two orders of magnitude, i.e., $10$ms-$1000$ms. Task relative deadlines are implicit, i.e., $D_i=T_i$. The worst-case execution time is computed accordingly, i.e. $C_i~=T_iU_i$. We then convert the genereated tasks to suspension tasks and the details are below:


+ The suspension lengths of the tasks were generated according to a *uniform* distribution, in either of three ranges depending on the self-suspension length (sslen):  

	* short suspension (sslen=Short): $[0.01(T_i-C_i),0.1(T_i-C_i)]$ 
	* moderate susp. (sslen=Moderate): $[0.1(T_i-C_i),0.3(T_i-C_i)]$  
	* long suspension (sslen=Long): $[0.3(T_i-C_i),0.6(T_i-C_i)]$ 

```python
UB=itask['period']-itask['execution']
s=random.uniform(minCtune*UB,maxCtune*UB)
```
+ We then generated computation segment $C_{i,1}$ as a percentage of $C_i$, according to a uniform distribution, and set $C_{i,2}$ accordingly.

```python
itask["Cseg"]=seg_UUniFast(maxnumsegs,itask['execution'])
```


| Built-in Functions |
| ------------------- |
| [UUniFast(n,u)](#uuni)|
|[SetGenerate(Pmin,numLog)](#setgen)|
| [segUUniFast(n,total)](#seguuni)|
|[SSSetGenerate(vRatio,minCtune,maxCtune,numsegs)](#sssetgen)|

	
####<a id="uuni"></a>UUniFast(_n,u_)
Uniformly generate a list of **n** values with a total value of **u**.

####<a id="seguuni"></a>segUUniFast(_n,u_)
Return a list of **n** values with a total value of **u** in a uniform distribution.

#### <a id="setgen"></a>SetGenerate(_Pmin,numLog_)
Generate a log-uniform distribution of periods, with **numLog** orders of magnitude and the minimum period of **Pmin**, operated on the task set generated from [UUniFast(n,u)](#uuni).

#### <a id="sssetgen"></a>SSSetGenerate(vRatio,minCtune,maxCtune,numsegs)
Convert a proportion **vRatio** of the genereated tasks to suspension tasks, each of which is with **numsegs** computation segments, and each of whose suspension length is drawn by **minCtune** and **maxCtune**, depending on which type of suspensions it is.

## Data Structures (Tasks)

A task set is composed of a set of tasks. We use data type *dictionary* built into Python to decribe each suspension task.

| Object         | Data Type       	  |
| -------------  | -------------------|
| tasks          | _list_             |
| task           | _dictionary_       |
| Cseg           | _list_             |
| Sseg           | _list_             |

The keywords of the dictionary and their meaning are below:

| Keyword        | Meaning                                  |
| -------------  | -----------------------------------------------|
| period         | the period/inter-arrival time of this task             |
| execution      | the total computation time of this task   |
| sslength       | the total suspension time of this task   |
| Cseg           | a list of the upper bounds on each computation segment   									|
| Sseg           | a list of the upper bounds on each suspension interval   |

**NOTE: we implicitly assume implicit deadlines here, so we don't need deadlines to be specified. Alternaively, one can add deadline as keywords to decribe deadlines.**

### Example 
```python
for itask in tasks:			
	print itask
```
```bash
{'Cseg': [1, 1], 'execution': 2, 'period': 89.0, 'sslength': 51, 'Sseg': [51]}
```

# Schedulability tests for suspension tasks 

Available tests are below:

* SCEDF `SC_EDF(tasks)`: the suspension-oblivious approach by converting suspension time into computation time; The original task system is schedulable if the total utilization of the transformed task system is no greater than 1.
* EDA `EDA(tasks)`: An enforcement approach using Equal-Deadline Assignment (EDA)
	under linear demand bound approximations, in Theorem 8 in *Jian-Jia Chen and Cong Liu. "Fixed-Relative-Deadline Scheduling of Hard Real-Time Tasks with Self-Suspensions" In Proceedings of the 35th IEEE Real-Time Systems Symposium (RTSS)*

* SEIFDA `greedy(tasks,scheme)`: a greedy approch, *Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen and Cong Liu. "Uniprocessor Scheduling Strategies for Self-Suspending Task Systems." In Proceedings of the 24th International Conference on Real-Time Networks and Systems (RTNS)*, see [here](http://dl.acm.org/ft_gateway.cfm?id=2997497\&ftid=1804918\&dwn=1\&CFID=691780547\&CFTOKEN=64912419).
* MILP `mip(tasks)`: The proposed approach in Section~\ref{sec:LP}, *Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen and Cong Liu. "Uniprocessor Scheduling Strategies for Self-Suspending Task Systems." In Proceedings of the 24th International Conference on Real-Time Networks and Systems (RTNS)*, see [here](http://dl.acm.org/ft_gateway.cfm?id=2997497\&ftid=1804918\&dwn=1\&CFID=691780547\&CFTOKEN=64912419).
	
* NC `NC(tasks)`: The necessary condition. We compared to the necessary condition to know how much we may lose to a
theoretical optimal algorithm in the worst case. 



# Logical constraints

We use the state-of-the-art optimization solver [Gurobi](http://www.gurobi.com/index ""), for our optimization problem, where the problem was intuitively formulated with some _logical_ constraints, e.g.,   

```
if x-y <=0: then 2b+c>0
else: 3b+2c<5
```


In CPLEX there is support for _logical_ constraints. Unfortunately, as of 2016, Gurobi (6.5) still could not handle logical constraints. Nevertheless, we can manually refomulate our optimization problem to the standard MILP by referring the *Big-M* method.

NOTE: [Gurobi 7.0](http://www.gurobi.com/products/whats-new/whats-new-in-the-latest-version) seems to have support for _logical_ constraints. 


## Big-M method
The idea of *Big-M* method is to use a _binary_ variable to activate the contraint in `if` while neutralizing another in `else`, and vice versa, by associating the violation of a constaint with a large positive penalty constant *M*.

For example, for a sufficiently large M and z binary variable (0 or 1), we can formulate the above logical constraints as follows:
```
x-y<=Mz
-x+y>-M(1-z)
-2b-c<Mz
-3b-2c+5>-M(1-z)
```

Let's take a closer look at these constraints. Suppose **z=0**, we can find that the `x-y<=Mz` and `-2b-c<Mz` are exactly the two constraints we orignally have, and `-x+y>-M(1-z)` and `-3b-2c+5>-M(1-z)` become `-x+y>-M` and `-3b-2c+5>-M`, which are natually satisfied if M is sufficiently large. With the some logicl, we can find the similar care for **z=1**. For more information, please see [here](https://ocw.mit.edu/courses/sloan-school-of-management/15-053-optimization-methods-in-management-science-spring-2013/tutorials/MIT15_053S13_tut09.pdf).


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
