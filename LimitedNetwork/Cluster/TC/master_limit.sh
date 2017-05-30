#!/bin/bash

RackInfoDir="RackInfo"
CMD_PATH=$(pwd)

## execute the script to get the Rack info
NodeNum=$(${CMD_PATH}/LoadCluster.sh)
echo $NodeNum

for ((i=1;i<=${NodeNum};i++))
do
    echo $i
    ## get file storing the ip info of each rack
    declare -a Rack_array
    Node_file="$CMD_PATH/${RackInfoDir}/Node${i}.txt"
    ## read info from the file
    Node=($(cat ${Node_file}))
    ssh ${Node} "mkdir /home/hadoop0master/workspace/Shell/TC" 2>/dev/null
    scp $CMD_PATH/${RackInfoDir}/Node${i}_* ${Node}:/home/hadoop0master/workspace/Shell/TC
    scp $CMD_PATH/slave*.sh ${Node}:/home/hadoop0master/workspace/Shell/TC
    ssh ${Node} "source /home/hadoop0master/workspace/Shell/TC/slave_cancel.sh"
    ssh ${Node} "source /home/hadoop0master/workspace/Shell/TC/slave_limit.sh"
done

