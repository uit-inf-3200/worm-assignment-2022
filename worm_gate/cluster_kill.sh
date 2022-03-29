#!/bin/bash

# Kills all user processes on the cluster, and cleans up worm temp files
# Author: Mike Murphy <michael.j.murphy@uit.no>

USER=$(whoami)

for COMPUTE in $(rocks list host compute | cut -d : -f1 | grep -v HOST)
do
    ssh -o PasswordAuthentication=false -f $COMPUTE killall -u $USER
    ssh -o PasswordAuthentication=false -f $COMPUTE killall -9 -u $USER
    ssh -o PasswordAuthentication=false -f $COMPUTE rm /dev/shm/*
done
