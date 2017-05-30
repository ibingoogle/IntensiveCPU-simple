#!/bin/bash

## declare two arrays to store inter_rack and intra_rack information
declare -a inter_rack_array
declare -a intra_rack_array

## network interfance you want to limit
DEV=eth0

## get current dir
CMD_DIR=$(pwd)

## files pathes which contain the inter-rack and intra-rack ips information
inter_rack_file="${CMD_DIR}/workspace/Shell/TC/Node*_InterRack.txt"
intra_rack_file="${CMD_DIR}/workspace/Shell/TC/Node*_IntraRack.txt"

## network bandwidth and unit you want to set(actually, it is outflow network bandwidth)
net_unit=mbit
intra_speed=1
inter_speed=1

## using above declared arrays to load the inter-rack and intra-rack ips from above files
inter_rack_array=($(cat ${inter_rack_file}))
intra_rack_array=($(cat ${intra_rack_file}))
# arrays size information
inter_rack_size=${#inter_rack_array[*]}
intra_rack_size=${#intra_rack_array[*]}
echo "inter_rack_size=" $inter_rack_size
echo "intra_rack_szie=" $intra_rack_size

## clean current tc rules
sudo tc qdisc del dev $DEV root 2>/dev/null

## build a HTB queue to the network interface
#  un-classfied network flow will be distributed to class 1:1
sudo tc qdisc add dev $DEV root handle 1: htb default 1

## add the different class and set the network bandwidth
#  class 1:1 is for the intra-rack communication
sudo tc class add dev $DEV parent 1: classid 1:1 htb rate ${intra_speed}${net_unit} ceil ${intra_speed}${net_unit}
#  class 1:2 is for the inter-rack communication
sudo tc class add dev $DEV parent 1: classid 1:2 htb rate ${inter_speed}${net_unit} ceil ${inter_speed}${net_unit}

## add the filter to distribute various network outflow!!!!!!
#  add the inter-rack to class 1:2
for ((i=0;i<$inter_rack_size;i++))
do
    sudo tc filter add dev $DEV protocol ip parent 1: prio 1 u32 match ip dst ${inter_rack_array[$i]} flowid 1:2
done
