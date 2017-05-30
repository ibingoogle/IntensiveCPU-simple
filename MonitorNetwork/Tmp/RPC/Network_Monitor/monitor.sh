#!/bin/bash

MonitorType="iftop"

CMD_PATH=$(pwd)

export $HOSTNAME

declare -a Cluster_array

Cluster_file="$CMD_PATH/cluster.txt"

Cluster_array=($(cat ${Cluster_file}))

Cluster_array_size=${#Cluster_array[*]}

hostname=$HOSTNAME

python /home/hadoop0master/workspace/Python/RPC/Network_Monitor/Network_Server/NetworkMonitor.py&

sleep 1
echo 2222222222222222222

for((i=0;i<${Cluster_array_size};i++))
do
    if [ ${Cluster_array[$i]} != $hostname ]
    then
        ssh ${Cluster_array[$i]} "python /home/hadoop0master/workspace/Python/RPC/Network_Monitor/Network_Client/${MonitorType}/${MonitorType}_monitor.py" 2>/dev/null&
        sleep 1
    fi
done
