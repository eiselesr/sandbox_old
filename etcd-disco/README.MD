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


# Add new node
h4 export id=$(ifconfig | awk '/eth0/ {id=$NF; print id;}')
# the address to advertise to peers
h4 export purl=http://10.0.0.4:2380

#peer-urls is my address for peers, and endpoints is who I want to talk to 
h4 ETCDCTL_API=3 ./etcd-download-test/etcdctl member add $id --peer-urls=http://10.0.0.4:2380 --endpoints=10.0.0.2:2379
