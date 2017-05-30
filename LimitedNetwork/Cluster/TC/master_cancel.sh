#!/bin/bash

RackInfoDir="RackInfo"
CMD_PATH=$(pwd)

for ((i=1;i<=6;i++))
do
    #echo $i
    ## get file storing the ip info of each rack
    declare -a Rack_array
    Rack_file="$CMD_PATH/${RackInfoDir}/Node${i}.txt"
    ## read info from the file
    Rack_array=($(cat ${Rack_file}))
    Rack_array_size=${#Rack_array[*]}
    ## get each ip within the rack
    for ((j=0;j<${Rack_array_size};j++))
    do
       echo ${Rack_array[${j}]}
       ssh ${Rack_array[${j}]} "sh /home/hadoop0master/workspace/Shell/TC/slave_cancel.sh"
    done
done

