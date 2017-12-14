IP=$1

echo $1

# ./etcd-download-test/etcd --name disco --initial-advertise-peer-urls http://$IP:2380 \
#   --listen-peer-urls http://$IP:2380 \
#   --listen-client-urls http://$IP:2379,http://127.0.0.1:2379 \
#   --advertise-client-urls http://$IP:2379 \
#   --initial-cluster-token etcd-disco-cluster-1 \
#   --initial-cluster disco=http://$IP:2380 \
#   --initial-cluster-state new &
