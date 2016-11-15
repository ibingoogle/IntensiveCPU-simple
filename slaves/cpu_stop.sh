#!/bin/bash

# the location to store pids
pids_location="/home/hadoop0master/workspace/Shell/intensive/cpu"

for pid in `cat ${pids_location}/pids`
do
  command="kill -s 9 ${pid}"
  $command
  echo "$pid killed"
done
