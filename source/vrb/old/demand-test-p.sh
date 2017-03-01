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

FPTDT=1
FPTQB=0
FPTVRBL2=0
RMQB=0
RMQBL=0
RMQBP=0

totBucket=100
tasksinBkt=10

UStart=60
UEnd=90
UStep=1

PStart=2
PEnd=2
PStep=3
TASKFILE="taskset-m.txt"

for p in $(eval echo "{$PStart..$PEnd..$PStep}")
do
if [ "$FPTDT" -eq "1" ]; then
	echo "" > tmpFPTDTm
fi
if [ "$FPTQB" -eq "1" ]; then
	echo "" > tmpFPTQBm
fi
if [ "$FPTVRBL2" -eq "1" ]; then
	echo "" > tmpFPTVRBL2m
fi
if [ "$RMQBL" -eq "1" ]; then
	echo "" > tmpRMQBLm
fi
if [ "$RMQBP" -eq "1" ]; then
	echo "" > tmpRMQBPm
fi
if [ "$RMQB" -eq "1" ]; then
	echo "" > tmpRMQBm
fi
for u in $(eval echo "{$UStart..$UEnd..$UStep}")
	do	
		
		numFailFPTDT=0
		numFailFPTQB=0
		numFailRMQBL=0
		numFailRMQBP=0
		numFailRMQB=0
		numFailFPTVRBL2=0
		for i in $(eval echo "{1..$totBucket}")
		do
			echo "U:" $u "Test:" $i
			prop=$(echo $p/10| bc -l)
			python tg.py -o $TASKFILE -i $i -u $u -n $tasksinBkt -p $prop

			if [ "$FPTDT" -eq "1" ]; then

				python ut.py -x 1 -s DTP -o $TASKFILE > FPTDT-tmp-result
				if grep -q fail FPTDT-tmp-result ;	then
 					echo "FPTDT fail at ",$i 
 					let numFailFPTDT+=1
				fi	

			fi
			if [ "$RMQBL" -eq "1" ]; then

				
				#success=$(awk 'BEGIN{pick='$tasksinBkt';beta='$beta'}{if(NR==pick){ un=$1}else {sum+=$1;sqt+=$1^2;}}END{if(un> 1-(1+beta)*sum+beta*0.5*sum^2+beta*0.5*sqt)print 1;else print 0;}' maxuset.txt)
				python ut.py -x 0 -s RMQBL -o $TASKFILE > RMQBL-tmp-result
				if grep -q fail RMQBL-tmp-result ;	then
 					echo "RMQBL fail at ",$i 
 					let numFailRMQBL+=1
				fi			
			fi
			if [ "$RMQB" -eq "1" ]; then

				
				#success=$(awk 'BEGIN{pick='$tasksinBkt';beta='$beta'}{if(NR==pick){ un=$1}else {sum+=$1;sqt+=$1^2;}}END{if(un> 1-(1+beta)*sum+beta*0.5*sum^2+beta*0.5*sqt)print 1;else print 0;}' maxuset.txt)
				python ut.py -x 0 -s RMQB -o $TASKFILE > RMQB-tmp-result
				if grep -q fail RMQB-tmp-result ;	then
 					echo "RMQB fail at ",$i 
 					let numFailRMQB+=1
				fi			
			fi
			if [ "$FPTQB" -eq "1" ]; then

				python ut.py -x 1 -s FPTQB -o $TASKFILE > FPTQB-tmp-result
				if grep -q fail FPTQB-tmp-result ;	then
 					echo "FPTQB fail at ",$i 
 					let numFailFPTQB+=1
				fi					
			fi
			
			if [ "$RMQBP" -eq "1" ]; then

				python ut.py -x 0 -s RMQBP -o $TASKFILE > RMQBP-tmp-result
				if grep -q fail RMQBP-tmp-result ;	then
 					echo "RMQBP fail at ",$i 
 					let numFailRMQBP+=1
				fi					
			fi
			if [ "$FPTVRBL2" -eq "1" ]; then

				python ut.py -x 1 -s FPTVRBL2 -o $TASKFILE > FPTVRBL2-tmp-result
				if grep -q fail FPTVRBL2-tmp-result ;	then
 					echo "FPTVRBL2 fail at ",$i 
 					let numFailFPTVRBL2+=1
				fi					
			fi


		done
		
		if [ "$FPTDT" -eq "1" ]; then
			echo "FPTDT:" $u $(echo 1-$numFailFPTDT/$totBucket | bc -l)
			echo $u $(echo 1-$numFailFPTDT/$totBucket | bc -l) >> tmpFPTDTm #plot
		fi

		if [ "$RMQBL" -eq "1" ]; then
			echo "RMQBL:" $u $(echo 1-$numFailRMQBL/$totBucket | bc -l)
			echo $u $(echo 1-$numFailRMQBL/$totBucket | bc -l) >> tmpRMQBLm #plot
		fi
		if [ "$FPTQB" -eq "1" ]; then
			echo "FPTQB:" $u $(echo 1-$numFailFPTQB/$totBucket | bc -l)
			echo $u $(echo 1-$numFailFPTQB/$totBucket | bc -l) >> tmpFPTQBm #plot
		fi		
		if [ "$RMQBP" -eq "1" ]; then
			echo "RMQBP:" $u $(echo 1-$numFailRMQBP/$totBucket | bc -l)
			echo $u $(echo 1-$numFailRMQBP/$totBucket | bc -l) >> tmpRMQBPm #plot
		fi	
		if [ "$FPTVRBL2" -eq "1" ]; then
			echo "FPTVRBL2:" $u $(echo 1-$numFailFPTVRBL2/$totBucket | bc -l)
			echo $u $(echo 1-$numFailFPTVRBL2/$totBucket | bc -l) >> tmpFPTVRBL2m #plot
		fi
		if [ "$RMQB" -eq "1" ]; then
			echo "RMQB:" $u $(echo 1-$numFailRMQB/$totBucket | bc -l)
			echo $u $(echo 1-$numFailRMQB/$totBucket | bc -l) >> tmpRMQBm #plot
		fi

	done

	#sort for plot
	for i in $(eval echo "{0..100..$UStep}")
		do
			if [ "$i" -lt "$UStart" ] ; then
				if [ "$FPTDT" -eq "1" ]; then
					echo $i 1 >> tmpFPTDTm
				fi
				if [ "$RMQBL" -eq "1" ]; then
					echo $i 1 >> tmpRMQBLm
				fi
				if [ "$FPTQB" -eq "1" ]; then
					echo $i 1 >> tmpFPTQBm
				fi	
					
				if [ "$RMQBP" -eq "1" ]; then
					echo $i 1 >> tmpRMQBPm
				fi
				if [ "$FPTVRBL2" -eq "1" ]; then
					echo $i 1 >> tmpFPTVRBL2m
				fi
				if [ "$RMQB" -eq "1" ]; then
					echo $i 1 >> tmpRMQBm
				fi
				
					
			elif [ "$i" -gt "$UEnd" ] ; then
				if [ "$FPTDT" -eq "1" ]; then
					echo $i 0 >> tmpFPTDTm
				fi
				if [ "$RMQBL" -eq "1" ]; then
					echo $i 0 >> tmpRMQBLm
				fi
				if [ "$FPTQB" -eq "1" ]; then
					echo $i 0 >> tmpFPTQBm
				fi	
				if [ "$RMQB" -eq "1" ]; then
					echo $i 0 >> tmpRMQBm
				fi
				if [ "$RMQBP" -eq "1" ]; then
					echo $i 0 >> tmpRMQBPm
				fi
				if [ "$FPTVRBL2" -eq "1" ]; then
					echo $i 0 >> tmpFPTVRBL2m
				fi

			fi
		done

if [ "$FPTDT" -eq "1" ]; then
	cat tmpFPTDTm | sort -k1,1n > $(echo fig-FPTDT)
	mv $(echo fig-FPTDT) plot/p/$p
	#rm FPTDT-tmp-result
	#rm tmpFPTDTm
fi

if [ "$FPTQB" -eq "1" ]; then
	cat tmpFPTQBm | sort -k1,1n > $(echo fig-FPTQB)
	mv $(echo fig-FPTQB) plot/p/$p
	
	#rm tmpFPTQBm
fi	
if [ "$RMQBL" -eq "1" ]; then
	cat tmpRMQBLm | sort -k1,1n > $(echo fig-RMQBL)
	mv $(echo fig-RMQBL) plot/p/$p
	#rm RMQBL-tmp-result
	#rm tmpRMQBLm
fi
if [ "$RMQB" -eq "1" ]; then
	cat tmpRMQBm | sort -k1,1n > $(echo fig-RMQB)
	mv $(echo fig-RMQB) plot/p/$p
	#rm RMQBL-tmp-result
	#rm tmpRMQBLm
fi
if [ "$RMQBP" -eq "1" ]; then
	cat tmpRMQBPm | sort -k1,1n > $(echo fig-RMQBP)
	mv $(echo fig-RMQBP) plot/p/$p
	#rm RMQBP-tmp-result
	#rm tmpRMQBPm
fi	
if [ "$FPTVRBL2" -eq "1" ]; then
	cat tmpFPTVRBL2m | sort -k1,1n > $(echo fig-FPTVRBL2)
	mv $(echo fig-FPTVRBL2) plot/p/$p
	#rm FPTVRBL2-tmp-result
	#rm tmpRMQBPm
fi	

done

