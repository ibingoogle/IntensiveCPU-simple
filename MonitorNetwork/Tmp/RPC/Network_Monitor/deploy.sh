#!/bin/bash

CMD_PATH=$(pwd)

export $HOSTNAME

declare -a Cluster_array

Cluster_file="$CMD_PATH/cluster.txt"

Cluster_array=($(cat ${Cluster_file}))

Cluster_array_size=${#Cluster_array[*]}

hostname=$HOSTNAME


for((i=0;i<${Cluster_array_size};i++))
do
    if [ ${Cluster_array[$i]} != $hostname ]
    then
        ssh ${Cluster_array[$i]} "mkdir /home/hadoop0master/workspace/Python/RPC/Network_Monitor" 2>/dev/null
        ssh ${Cluster_array[$i]} "rm -rf /home/hadoop0master/workspace/Python/RPC/Network_Monitor/Network_Client" 2>/dev/null
        scp -r $CMD_PATH/Network_Client_Backup ${Cluster_array[$i]}:/home/hadoop0master/workspace/Python/RPC/Network_Monitor/Network_Client
    fi
done
