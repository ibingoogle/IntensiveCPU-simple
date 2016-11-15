#!/bin/bash

# Destription: simple cpu intensive example using Shell language
# Example    : sh cpu_intensive.sh 4
# Data       : Nov 15 2016

# the sequence to bind the cpu cores, default is 0,1,2,3
cpu_sequence=("0x01" "0x02" "0x04" "0x08")

# the location to store pids
pids_location="/home/hadoop0master/workspace/Shell/intensive/cpu"

# the cpu intensive while program 
while_loop()
{
 echo -ne "i=0;
 while true
 do
 i=1;
 done" | /bin/bash &
}

# cpu_intensive.sh usage
if [ $# != 1 ] ; then
  echo "usage: $0 <cpus>"
  exit 1;
fi

# start program based on arguments
for i in `seq $1`
do
  while_loop
  pid_list[$i]=$! # record the pids
  taskset -p ${cpu_sequence[$i-1]} ${pid_list[$i]} # bind to core
done

# add the pids into pids file
rm -rf ${pids_location}/pids 2>/dev/null
touch ${pids_location}/pids
for i in "${pid_list[@]}"; do
  echo 'kill -s 9 ' $i
  echo $i  >> ${pids_location}/pids;
done
