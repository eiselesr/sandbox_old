#!/bin/bash

# Source for this script : https://docs.openstack.org/install-guide/environment-etcd-ubuntu.html
# This scipt also contains info on setting up systemd service.

mkdir -p /etc/etcd
#chown etcd:etcd /etc/etcd
mkdir -p /var/lib/etcd
#chown etcd:etcd /var/lib/etcd

ETCD_VER=v3.2.11
rm -rf /tmp/etcd && mkdir -p /tmp/etcd
curl -L https://github.com/coreos/etcd/releases/download/${ETCD_VER}/etcd-${ETCD_VER}-linux-arm64.tar.gz -o /tmp/etcd-${ETCD_VER}-linux-arm64.tar.gz
tar xzvf /tmp/etcd-${ETCD_VER}-linux-arm64.tar.gz -C /tmp/etcd --strip-components=1
cp /tmp/etcd/etcd /usr/bin/etcd
cp /tmp/etcd/etcdctl /usr/bin/etcdctl
