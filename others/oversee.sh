#!/bin/bash 

pidfile=/tmp/mydaemon.pid 


while true 
do 
	procid="`cat /tmp/mydaemon.pid`" 
#	echo $procid
	process="`ps $procid |awk '{print $6}'|awk '{if(NR>1)print}'`"
#	echo $process
#	if [ -z "$process"] 
	if [ "$process" == "" ]; 
	then 
		procid2="`ps -ef|grep "python main.py"|grep -v grep|awk '{print $2}'`"
		if [ -z "$procid2" ]; 
		then
		       	rm "$pidfile" 	
			python main.py
			echo "python main.py started"
		else 
			kill -9 $procid2
			python main.py
			echo "python main.py restarted"
		fi 
	else 
		echo "$process is running fine"
	fi 
	sleep 0.5 
done 



