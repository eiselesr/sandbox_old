#!/usr/bin/python

#https://github.com/mininet/mininet/wiki/FAQ


from mininet.topo import Topo
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.nodelib import NAT

class NatTopo( Topo ):
    def build( self, natIP='10.0.2.254' ):
        self.hopts = { 'defaultRoute': 'via ' + natIP }
        hosts  = [ self.addHost( h ) for h in 'h1', 'h2' ]
        s1 = self.addSwitch( 's1' )
        for h in hosts:
            self.addLink( s1, h )
        nat1 = self.addNode( 'nat1', cls=NAT, ip=natIP,
                             inNamespace=False )
        self.addLink( nat1, s1 )

def setup():


    #topo = SingleSwitchTopo( k=4 )
    topo = NatTopo()
    net = Mininet( topo=topo, xterms=True)
    net.start() #neccessary for nat to work.

    controller = net.get('c0')
    CLI(net) #opens mn in terminal. Also is a kind of pause
    net.stop() #shuts everything down.

if __name__ == '__main__':
    setLogLevel( 'info' )
    setup()
