#!/bin/bash

Path="/home/hadoop0master/workspace/Shell/intensive/cpu"

cat conf | while read slave
do 
 arr=(${slave//,/ })
 ssh -f ${arr[1]} "source ${Path}/cpu_stop.sh"
done
