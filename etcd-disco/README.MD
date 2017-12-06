# To Run
sudo ./setup-mn.py

#mininet host terminal example commands

mininet> h2 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.3:2379 member list
mininet> h2 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.2:2379 put foo "hello"
mininet> h3 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.2:2379 get foo
mininet> h3 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.3:2379 put foo "goobye"
mininet> h2 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.3:2379 get foo

# Get all values
ETCDCTL_API=3 $PATH/etcdctl --endpoints=10.0.0.2:2379 get --prefix ""

h2 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.2:2379 get --prefix "" -w json

# Snapshot
h2 ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db

# Watch
h3 ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints=10.0.0.3:2379 watch /WM/TempSensor/cpu/quota
