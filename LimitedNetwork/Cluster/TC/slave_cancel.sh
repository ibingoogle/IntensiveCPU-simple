#!/bin/bash

## network interface
DEV=eth0

## clean current tc rules
sudo tc qdisc del dev $DEV root 2>/dev/null
