#!/bin/bash
# file.sh: a sample shell script to demonstrate the concept of Bash shell functions
# # define usage function
# usage(){
# 	echo "Usage: $0 filename"
# 	exit 1
# } 
# # define is_file_exits function 
# # $f -> store argument passed to the script
# is_file_exits(){
# 	local f="$1"
# 	[[ -f "$f" ]] && return 0 || return 1
# }
#PYTHON="/bin/python"
#exec "/bin/python  tg.py"
# echo "The first choice is nice"
# invoke  usage
# call usage() function if filename not supplied
#[[ $# -eq 0 ]] && usage 
# Invoke is_file_exits
# if ( is_file_exits "$1" )
# then
#  echo "File found"
# else
#  echo "File not found"
# fi
#set -x 
DEMANDTEST=1

totBucket=100
tasksinBkt=10

UStart=58
UEnd=58
UStep=5
FStart=15
FEnd=15
FStep=5



for f in $(eval echo "{$FStart..$FEnd..$FStep}")
do
echo "" > log
echo "" > tmpDTf #plot
for u in $(eval echo "{$UStart..$UEnd..$UStep}")
	do	
		
		numFailDT=0

		for i in $(eval echo "{1..$totBucket}")
		do
			echo "U:" $u "Test:" $i
			sfactor=$(echo $f/10 | bc -l)
			python tg.py -i $i -u $u -n $tasksinBkt -f $sfactor

			if [ "$DEMANDTEST" -eq "1" ]; then
				python dp-recursive.py > tmp-demand-test-f

				if grep -q fail tmp-demand-test-f ;	then
 					echo "DT fail at ",$i 
 					let numFailDT+=1
				fi

			fi

		done
		
		if [ "$DEMANDTEST" -eq "1" ]; then
			echo "DT:" $u $(echo 1-$numFailDT/$totBucket | bc -l)
			echo $u $(echo 1-$numFailDT/$totBucket | bc -l) >> tmpDTf #plot
		fi

	done

	#sort for plot
	for i in $(eval echo "{0..100..$UStep}")
		do
			if [ "$i" -lt "$UStart" ] ; then
				if [ "$DEMANDTEST" -eq "1" ]; then
					echo $i 1 >> tmpDTf
				fi

				
					
			elif [ "$i" -gt "$UEnd" ] ; then
				if [ "$DEMANDTEST" -eq "1" ]; then
					echo $i 0 >> tmpDTf
				fi

			fi
		done
if [ "$DEMANDTEST" -eq "1" ]; then
	cat tmpDTf | sort -k1,1n > $(echo fig-DT-f$f)
	mv $(echo fig-DT-f$f) plot/
fi

done
# if [ "$REAL_MULTI_SCH" -eq "1" ]; then
	
# 	#interested interval
# 	for u in $(eval echo "{$UStart..$UEnd..$UStep}")
# 	do	
# 		numFail=0
# 		#number of buckets for evaluation at a drawing point
# 		for i in $(eval echo "{1..$totBucket}")
# 		do	  
			
# 			#tast sets generation
# 			if [ -f tg.py ];	then
# 				echo "Task set generating..." >> log
# 				python tg.py $i $u $ratioSoft $tasksinBkt >> log
# 			fi
# 			#multiprocessor scheduling for hard real-time tasks
# 			if [ -f mp.py ];	then
# 				echo "scheduling...",$i >> log
# 				python mp.py taskset.txt $ALG $avbProcessor > result
# 			fi		
			
# 			#check feasiability
# 			if grep -q fail result ;	then
# 				echo "periodic fail",$i >> log
# 				let numFail+=1
# 			elif [ "$IF_DEDICATED" -eq "0" ]; then
# 				sumUss=$(awk '/proc/{if($4==0){sum+=1}else{u=2*($3/$4+1)^(-$4)-1; if(u>0){sum+=u}}}END{print sum}' result)	
# 				awk '/proc/{if($4==0){sum+=1; print 1}else{u=2*($3/$4+1)^(-$4)-1; print u}}END{}' result > sfactor	
# 				softU=$(echo $u*$ratioSoft*0.01| bc -l) 
# 				if
# 				[ $(echo "$softU>$sumUss" | bc) -eq "1" ] ;
# 				then
# 					#soft fail
# 					echo "soft fail",$i >> log
# 					echo "soft fail",$i >> WCRT
# 					let numFail+=1
# 				else
# 					if [ "$WCRT_EN" -eq "1" ]; then
# 						#WCRT calcuation for LPT-DIS
# 						python tg-pnc.py $i $u $ratioSoft $tasksinBkt >> log
# 						python lpt.py CSet.txt LPT >> WCRT
# 					fi
# 				fi
# 			fi
	
# 		done
# 		echo $u $(echo 1-$numFail/$totBucket | bc -l) >> tmp #plot
		
# 	done
	
# 	#fill out the uninterested interval
# 	for i in $(eval echo "{100..$(($numProcessor*100))..$UStep}")
# 		do
# 			if [ "$i" -lt "$UStart" ] ; then
# 				echo $i 1 >> tmp
# 			elif [ "$i" -gt "$UEnd" ] ; then
# 				echo $i 0 >> tmp
# 			fi
# 		done
# 	#sort for plot
# 	cat tmp | sort > $(echo fig-D=$IF_DEDICATED-r=$ratioSoft-m=$numProcessor)

# else
# 	for u in $(eval echo "{$UStar_S..$UEnd_S..$UStep}")
# 	do	
# 		numFail=0
# 		echo "" > WCRT #LPT WCRT
# 		#number of buckets for evaluation at a drawing point
# 		for i in $(eval echo "{1..$totBucket}")
# 		do	  
# #tast sets generation
# 				 if [ -f tg.py ];	then
# 				 	echo "Processor distruburation generating..." >> log
# 				 	python tg.py $i $u $ZERORatio $numProcessor >> log
# 				 fi
# 				 cat taskset.txt | tr "[]" " " | sed s/,/\\n/g > sfactor
					
				
				
# 					#WCRT calcuation for LPT-DIS
# 					python tg-pnc.py $i $U_IRQ $ONERatio $tasksinBkt >> log
# 					python lpt.py CSet.txt LPT >> WCRT
				
# 		done
# 		avg_WCRT=$(awk '/CSUM/{sum+=$2;line+=1;} END{print sum/line}' WCRT)
# 		echo $u $avg_WCRT >> tmp #plot
		
# 	done
# fi