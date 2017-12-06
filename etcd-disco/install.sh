ETCD_VER=v3.2.10

# choose either URL
GOOGLE_URL=https://storage.googleapis.com/etcd
GITHUB_URL=https://github.com/coreos/etcd/releases/download
DOWNLOAD_URL=${GOOGLE_URL}

rm -f ./etcd-${ETCD_VER}-linux-amd64.tar.gz
rm -rf ./etcd-download-test && mkdir -p ./etcd-download-test

curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o ./etcd-${ETCD_VER}-linux-amd64.tar.gz
tar xzvf ./etcd-${ETCD_VER}-linux-amd64.tar.gz -C ./etcd-download-test --strip-components=1
rm -f ./etcd-${ETCD_VER}-linux-amd64.tar.gz

./etcd-download-test/etcd --version
<<COMMENT
etcd Version: 3.2.10
Git SHA: 694728c
Go Version: go1.8.5
Go OS/Arch: linux/amd64
COMMENT

ETCDCTL_API=3 ./etcd-download-test/etcdctl version
<<COMMENT
etcdctl version: 3.2.10
API version: 3.2
COMMENT
