#!/usr/bin/python

from mininet.topo import Topo
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI


def setup():

    topo = SingleSwitchTopo( k=4 )
    net = Mininet( topo=topo, xterms=True)
    net.addNAT().configDefault()
    net.start() #neccessary for nat to work.

    controller = net.get('c0')
    #DISCO = controller.cmd('${ETCD_DISCOVERY:-$(curl https://discovery.etcd.io/new?size=3)}')
    DISCO = controller.cmd('curl https://discovery.etcd.io/new?size=3')

    print("DISCO %s" %DISCO)
    nodes = net.keys()
    print("nodes are %s" %nodes)
    for key in net.__iter__():
        if 'h' in key:
            node = net.get(key)
            result = node.cmd('ifconfig')
            node.cmd('export ETCD_DISCOVERY=%s' %DISCO)
            print("node.cmd: %s" %node.cmd('echo $ETCD_DISCOVERY'))
            print (result)
    # h1 = net.get('h1')
    # result = h1.cmd('ifconfig')
    # print (result)
    CLI(net) #opens mn in terminal. Also is a kind of pause
    net.stop() #shuts everything down.

if __name__ == '__main__':
    setLogLevel( 'info' )
    setup()
