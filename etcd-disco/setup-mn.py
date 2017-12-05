#!/usr/bin/python

from mininet.topo import Topo
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
import time


def setup():

    topo = SingleSwitchTopo( k=3 )
    net = Mininet( topo=topo, xterms=True)
    #net.addNAT().configDefault()
    net.start() #neccessary for nat to work.

    controller = net.get('c0')
    #DISCO = controller.cmd('${ETCD_DISCOVERY:-$(curl https://discovery.etcd.io/new?size=3)}')
    UUID = ((controller.cmd('uuidgen')).strip('\n')).strip('\r')
    print("UUID %s" %UUID,)
    DISCO="http://10.0.0.1:2379/v2/keys/discovery/"+UUID
    print("DISCO %s" %DISCO,)
    with open('etcd.config', 'w') as f:
        f.write(DISCO)
    h1 = net.get('h1')
    setup_res = h1.cmd('./setupDisco.sh')
    print("setup_res %s" %setup_res)
    time.sleep(1) # need to give etcd cluster time to start.

    cmd = "curl -X PUT "+DISCO+"/_config/size -d value=2"
    print("cmd %s" %cmd)
    put_res = h1.cmd(cmd)
    print("put res %s" %put_res)
    result = h1.cmd("curl -X GET "+DISCO+"/_config/size")
    print("disco result: %s" %result)
    nodes = net.keys()
    print("nodes are %s" %nodes)

    for key in net.__iter__():
        if 'h' in key and key!='h1':
            node = net.get(key)
            print(node.cmd("./etcd-setup.sh "))
#
#
#     # h1 = net.get('h1')
#     # result = h1.cmd('ifconfig')
#     # print (result)
    CLI(net) #opens mn in terminal. Also is a kind of pause
    net.stop() #shuts everything down.

if __name__ == '__main__':
    setLogLevel( 'info' )
    setup()
