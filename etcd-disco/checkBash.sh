#!/bin/bash
export ETCDCTL_API=3
HOST_1=10.0.0.2
ENDPOINTS=$HOST_1:2379

ID=${1:-"$(ifconfig | awk '/eth0/ {ID=$NF; print ID;}')"}
# $NF gives the number of fields in a record. So here it is used to get the last
#record.

echo "ID: $ID"
