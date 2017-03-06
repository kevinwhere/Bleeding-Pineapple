README v1.0 / 06 MARCH 2017

# Multi-Mode Tasks Generation

We first generated a set of sporadic tasks. The cardinality of the task set was 10.
The UUniFast method was adopted to generate a set of utilization values with the given goal.
We use the approach suggested by Emberson et al.~\cite{emberson2010techniques} to generate the task periods according to the **exponential distribution**.
 The distribution of periods is within two orders of magnitude, i.e., $10$ms-$1000$ms. Task relative deadlines are implicit, i.e., D~i~=T~i~$. 
 The worst-case execution time was computed accordingly, i.e. $C~i~=T~i~U~i~$. H~2~O
 We converted a proportion $p$ of tasks to multi-mode tasks:

* A multi-mode task has $M$ execution modes
```python
for j in range(numMode):
```
* The generated sporadic task triplet $(C_i,T_i,D_i)$ was assigned to the setting of task mode $\tau_i^1$.
* We use a scaling factor to assign the parameters of the other modes, i.e., $C_i^{m+1}=1.5C_i^{m}$ and 
    $T_i^{m+1}=1.5T_i^{m}$. 
* We randomly choose a mode to have the largest utilization. 
```python
iMaxU=random.randrange(numMode)
```
* The worst-case execution times of the remaining modes 
    were adjusted by multiplying them by uniform random 
    values in the range [minCtune,maxCtune].
```python
def wiki_rocks(text):
    p=iStask['period']*math.pow(scalefac, j)
    c=iStask['period']*iStask['utilization']*math.pow(scalefac, j) 
```         
#tune C for non- MaxU by multiplying them by uniform random values in the range [minCtune,maxCtune]
if j != iMaxU:      
    c=c*random.uniform(minCtune,maxCtune);
```
* Ensure the discrete time model
```python
s=math.ceil(p)/p
pair['period']=math.ceil(p) 
pair['execution']=c*s
```