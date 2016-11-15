#!/bin/bash

#not reommeonded, clear the background ssh ASAP
cat conf | while read slave
do 
 arr=(${slave//,/ })
 ssh -f -p 22 ${arr[0]}@${arr[1]} 'mkdir /home/hadoop0master/workspace >/dev/null 2>&1 &'
 ssh -f -p 22 ${arr[0]}@${arr[1]} 'mkdir /home/hadoop0master/workspace/Shell >/dev/null 2>&1 &'
 ssh -f -p 22 ${arr[0]}@${arr[1]} 'mkdir /home/hadoop0master/workspace/Shell/intensive >/dev/null 2>&1 &'
 ssh -f -p 22 ${arr[0]}@${arr[1]} 'mkdir /home/hadoop0master/workspace/Shell/intensive/cpu >/dev/null 2>&1 &'
done
