#mininet with xterms for each node in hub topology
sudo mn -x --topo single, 4

#run on each node
etcd-download-test/etcd --name infra0 --initial-advertise-peer-urls http://10.0.0.1:2380 \
  --listen-peer-urls http://10.0.0.1:2380 \
  --listen-client-urls http://10.0.0.1:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.0.1:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.0.1:2380,infra1=http://10.0.0.2:2380,infra3=http://10.0.0.3:2380 \
  --initial-cluster-state new

etcd-download-test/etcd --name infra1 --initial-advertise-peer-urls http://10.0.0.2:2380 \
  --listen-peer-urls http://10.0.0.2:2380 \
  --listen-client-urls http://10.0.0.2:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.0.2:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.0.1:2380,infra1=http://10.0.0.2:2380,infra2=http://10.0.0.3:2380 \
  --initial-cluster-state new

etcd-download-test/etcd --name infra2 --initial-advertise-peer-urls http://10.0.0.3:2380 \
  --listen-peer-urls http://10.0.0.3:2380 \
  --listen-client-urls http://10.0.0.3:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.0.3:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.0.1:2380,infra1=http://10.0.0.2:2380,infra2=http://10.0.0.3:2380 \
  --initial-cluster-state new

#Get all keys
ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints 'https://10.0.0.2:2379' get "" --prefix

#SAVE JSON TO BASH ENVIRONMENT VARIABLE
APPJSON=$(cat app/WeatherMonitor_app.json)

#PASS AS VALUE TO ETCD
ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints 'https://10.0.0.2:2379' put appWM "$APPJSON"

#PLACE VALUE DIRECTLY WITH cat
cat file | put <key>
