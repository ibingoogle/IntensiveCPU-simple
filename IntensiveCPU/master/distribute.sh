#!/bin/bash

Path="/home/hadoop0master/workspace/Shell/intensive/cpu"

cat conf | while read slave
do 
 arr=(${slave//,/ })
 command="scp ../slaves/* ${arr[0]}@${arr[1]}:$Path"
 $command
done
