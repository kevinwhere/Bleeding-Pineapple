import math
def Workload_w_C(T,C,WCRT,t):
	n=int((t-C+WCRT)/T)	
	return n*C+min(C,t-C+WCRT-T*n)

def Workload(T,C,t):
	return  C*math.ceil(t/T)

def dbf_constrained(C,D,T,t):
	return max(0,C*int((t+(T-D))/T))

def dbf_constrained_apprx(C,D,T,t):
	if t<0:
		print "Oops dbf"
		sys.exit()
	return C*((t+(T-D))/T)


	

