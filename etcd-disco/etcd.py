import etcd3
import subprocess
import json
import pprint
import time


if False:
    node1 = etcd3.client(host='10.0.0.1', port=2379)
    node2 = etcd3.client(host='10.0.0.2', port=2379)
    node3 = etcd3.client(host='10.0.0.3', port=2379)

    node2.create_alarm()
    node2.list_alarms()
    node2.disarm_alarm()

    node1.put('/key', 'doot')

    key = node1.get('/key')[0]
    keys = node1.get_all()
    for key in keys:
        print(key)


with open ('./app/WeatherMonitor_app.json') as f:
    appJSON = json.load(f)
pprint.pprint(appJSON)

appJSON['nodes'] = {'node1':0, 'node2':0, 'node3':0}
print(appJSON['nodes'])
pprint.pprint(appJSON)

node1 = etcd3.client(host='10.0.0.1', port=2379)
node2 = etcd3.client(host='10.0.0.2', port=2379)
node3 = etcd3.client(host='10.0.0.3', port=2379)

def isHealthy(ip):
    bashCommand = "ETCDCTL_API=3 ./etcd-download-test/etcdctl --endpoints 'http://"+ip+":2379' endpoint health"
    p1 = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE)
    output, error = p1.communicate()
    return ("is healthy" in str(output))

#Rather than doing this each node can change its value periodically and if it isn't updated then it is assumed to have died.
while True:
    if isHealthy('10.0.0.2'):
        appJSON['nodes']['node2'] = 1
        p = json.dumps(appJSON)
        node1.put('appWM', p)
    else:
        appJSON['nodes']['node2'] = 0
        p = json.dumps(appJSON)
        node1.put('appWM', p)
    time.sleep(1)
    print(appJSON['nodes']['node2'])
    pprint.pprint(node3.get('appWM'))

#Watch
def watch_callback(event):
    print(event)
node3.add_watch_callback("appWM", watch_callback)
#Lease
lease3 = node3.lease(10)
print(lease3)
#discovery

#Don't care whose leader
#namespaces
