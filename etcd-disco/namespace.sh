#SOURCE : https://coreos.com/blog/etcd-3.2-announcement

# start etcd
PATH="etcd-download-test"
$PATH/etcd &
etcd grpc-proxy start --endpoints=http://localhost:2379 \
                      --listen-addr=localhost:23790 \
                      --namespace=/app-A/ &
etcd grpc-proxy start --endpoints=http://localhost:2379 \
                      --listen-addr=localhost:23791 \
                      --namespace=/app-B/ &
# write to /app-A/ and /app-B/
ETCDCTL_API=3 $PATH/etcdctl --endpoints=http://localhost:23790 put abc a
ETCDCTL_API=3 $PATH/etcdctl --endpoints=http://localhost:23791 put abc z
# confirm the different keys were written
ETCDCTL_API=3 $PATH/etcdctl --endpoints=http://localhost:2379 get --prefix /app
