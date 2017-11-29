#!/bin/bash
echo "hello"

DISCO=${ETCD_DISCOVERY:-$(curl https://discovery.etcd.io/new?size=3)}

echo $DISCO:1111

ip="$(hostname -I | cut -d " " -f 1)" #there was a trailing whitespace
echo $ip:2380

# $NF gives the number of fields in a record. So here it is used to get the last
#record.

id="$(ifconfig | awk '/eth0/ {id=$NF;}{print id;exit 0}')"#NEEDS ETH0
#id='08:00:27:41:01:26'
echo $id

./etcd-download-test/etcd --name $id --initial-advertise-peer-urls http://$ip:2380 \
  --listen-peer-urls http://$ip:2380 \
  --listen-client-urls http://$ip:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://$ip:2379 \
  --discovery $DISCO
