#!/bin/bash

MonitorType="iftop"

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
        ssh ${Cluster_array[$i]} "python /home/hadoop0master/workspace/Python/RPC/Network_Monitor/Network_Client/${MonitorType}/${MonitorType}_stop.py" 2>/dev/null
    fi
done

sleep 1
python /home/hadoop0master/workspace/Python/RPC/Network_Monitor/Network_Server/NetworkMonitor_stop.py
