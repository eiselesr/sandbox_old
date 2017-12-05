#!/bin/bash
echo "hello"


#UUID=${UUID:-$(uuidgen)} # generate
#UUID="188e06eb-9259-4466-88cf-778722dccace" #use for all nodes in cluster
#e.g. DISCO=http://10.0.0.1:2379/v2/keys/discovery/$UUID
DISCO=`cat etcd.config`
echo "DISCO: $DISCO"

ip="$(hostname -I | cut -d " " -f 1)" #there was a trailing whitespace
echo "IP: $ip:2380"

# $NF gives the number of fields in a record. So here it is used to get the last
#record.

id="$(ifconfig | awk '/eth0/ {id=$NF; print id;}')"
echo "ID: $id"

./etcd-download-test/etcd --name ${id} \
	--initial-advertise-peer-urls http://${ip}:2380 \
  --listen-peer-urls http://${ip}:2380 \
	--advertise-client-urls http://${ip}:2379 \
  --listen-client-urls http://${ip}:2379 \
	--discovery $DISCO &
