README v0.0 / 01 MARCH 2017

# Multi-Mode Tasks Generation

We first generated a set of sporadic tasks. The cardinality of the task set was 10.
The UUniFast method was adopted to generate a set of utilization values with the given goal.
We use the approach suggested by Emberson et al.~\cite{emberson2010techniques} to generate the task periods according to the **exponential distribution**.
 The distribution of periods is within two orders of magnitude, i.e., $10$ms-$1000$ms. Task relative deadlines are implicit, i.e., $D_i=T_i$. 
 The worst-case execution time was computed accordingly, i.e. $C_{i}=T_iU_i$.
 We converted a proportion $p$ of tasks to multi-mode tasks:

*item A multi-mode task has $M$ execution modes
*item The generated sporadic task triplet $(C_i,T_i,D_i)$ was assigned to the setting of task mode $\tau_i^1$.
*item We use a scaling factor $1.5$ to assign     the parameters of the other modes\footnote{We use the dynamic
        programming approach to implement DT-FPT instead of using the ILP
        solver for the sake of efficiency. To comply with it, we apply a correction factor $\frac{\ceiling{T_i}}{T_i}$ on both the generated period and execution time to ensure the discrete time model.}, i.e., $C_i^{m+1}=1.5C_i^{m}$ and 
    $T_i^{m+1}=1.5T_i^{m}$. 
*item We randomly choose a mode to have the largest 
    utilization. The worst-case execution times of the remaining modes 
    were adjusted by multiplying them by uniform random 
    values in the range $[0.75, 1]$.
