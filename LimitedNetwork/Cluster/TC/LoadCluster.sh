#!/bin/bash

declare -a w_c_i_array
declare -a d_c_array

## whole cluster info file path and cluster division file path
w_c_i_file="./WholeClusterInfo.txt"
d_c_file="./DivisionCluster.txt"

## The directory stores the Rack, Rack_Inter and Rack_Intra info
RackInfoDir="RackInfo"

## create the RackInfo directory
mkdir $RackInfoDir 2>/dev/null

## load the info from two files
w_c_i_array=($(cat ${w_c_i_file}))
w_c_i_size=${#w_c_i_array[*]}
#echo "w_c_i_size =" $w_c_i_size
d_c_array=($(cat ${d_c_file}))
d_c_size=${#d_c_array[*]}
#echo "d_c_size = " $d_c_size

## nodess number in Cluster
NodeNum=0

## create files to store the rack
rm "./${RackInfoDir}/Node"*".txt" 2>/dev/null
for ((i=0; i<${w_c_i_size}; i++))
do
    length=${#w_c_i_array[$i]}
    if [ $length -eq 1 ]
    then
        NodeNum=$((NodeNum+1))
        touch "./${RackInfoDir}/Node${NodeNum}.txt"
        touch "./${RackInfoDir}/Node${NodeNum}_InterRack.txt"
        touch "./${RackInfoDir}/Node${NodeNum}_IntraRack.txt"
    else
        echo ${w_c_i_array[$i]} >> "./${RackInfoDir}/Node${NodeNum}.txt"
    fi
done
echo $NodeNum

## determine the inter-rack and intra-rack info
for ((i=0; i<${d_c_size}; i++))
do
    # get each sub cluster
    subcluster=(${d_c_array[$i]//,/ })
    ## consider each rack in sub cluster
    for node in ${subcluster[@]}
    do
        # scan all nodes
        for (( j=1; j<=NodeNum; j++ ))
        do
            flag=1 # represent node j belongs to the inter-rack
            for element in ${subcluster[@]}
            do
                if [ $element -eq $j ]
                then
                    flag=0 # represent rack j is in the same sub cluster
                    break
                fi
            done
            if [ $flag -eq 1 ]
            then
                cat ./${RackInfoDir}/Node${j}.txt >> ./${RackInfoDir}/Node${node}_InterRack.txt # add the inter-rack node ip to file
            else
                cat ./${RackInfoDir}/Node${j}.txt >> ./${RackInfoDir}/Node${node}_IntraRack.txt # add the intra-rack node ip to file
            fi
        done
    done
done
