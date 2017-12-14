#!/bin/bash
export ETCDCTL_API=3
HOST_1=10.0.0.2
ENDPOINTS=$HOST_1:2379
#echo $ENDPOINTS

# $NF gives the number of fields in a record. So here it is used to get the last
#record.
ID=${1:-"$(ifconfig | awk '/eth0/ {ID=$NF; print ID;}')"}
echo "ID: $ID"

mapfile -t MEMBERS< <(./etcd-download-test/etcdctl --endpoints=$ENDPOINTS member list)

#-----------------------------------------------------
#  BUILD ETCD_INITIAL_CLUSTER
OIFS=$IFS
shopt -s extglob
for i in "${MEMBERS[@]}"
  do
    IFS=','
    set -- $i
    item=${3##*( )}=${4##*( )} # https://www.cyberciti.biz/faq/bash-remove-whitespace-from-string/
    echo "item $item space"
    IFS=$OIFS
    ETCD_INITIAL_CLUSTER+=$item,
done
echo $ETCD_INITIAL_CLUSTER
#----------------------------------------
#     EXAMPLE
# set -- ${MEMBERS[1]}
# item=${3##*( )}=${4##*( )}
# echo "item $item"
#----------------------------------------
shopt -u extglob
#IFS=$OIFS
###############################################################################

ip="$(hostname -I | cut -d " " -f 1)" #there was a trailing whitespace
echo "IP: $ip:2380"

./etcd-download-test/etcdctl member add $ID \
  --peer-urls=http://$ip:2380 \
  --endpoints=$ENDPOINTS
ETCD_INITIAL_CLUSTER+="$ID=http://$ip:2380"

export ETCD_NAME=$ID
export ETCD_INITIAL_CLUSTER_STATE=existing
export ETCD_INITIAL_CLUSTER=$ETCD_INITIAL_CLUSTER
echo "ETCD_NAME $ETCD_NAME"
echo "ETCD_INITIAL_CLUSTER_STATE $ETCD_INITIAL_CLUSTER_STATE"
echo "ETCD_INITIAL_CLUSTER $ETCD_INITIAL_CLUSTER"

#./etcd-download-test/etcdctl member remove $ID \
  # --endpoints=$ENDPOINTS

#sleep 10s

if true; then
	./etcd-download-test/etcd \
		--listen-client-urls http://${ip}:2379 \
		--advertise-client-urls http://${ip}:2379 \
		--listen-peer-urls http://${ip}:2380 \
		--initial-advertise-peer-urls http://${ip}:2380 &
fi
