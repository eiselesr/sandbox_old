#!/bin/bash
export ETCDCTL_API=3
HOST_1=10.0.0.2
ENDPOINTS=$HOST_1:2379

ID=$1

./etcd-download-test/etcdctl \
  --endpoints=$ENDPOINTS \
  member remove $ID

response="$(./etcd-download-test/etcdctl --endpoints=$ENDPOINTS endpoint health)"
echo $response

# case $response in
#   *healthy*)
#   healthy=true;;
#   *)
#   healthy=false;;
# esac
# echo $healthy

while [[ $response != *"healthy"* ]]; do
  sleep 1
  response="$(./etcd-download-test/etcdctl --endpoints=$ENDPOINTS endpoint health)"
  echo $response
done

echo "If you intend to re-add a member with this name, don't forget to delete the data directory"
