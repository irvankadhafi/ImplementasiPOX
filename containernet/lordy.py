#!/usr/bin/python
from mininet.net import Containernet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Docker, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import info, setLogLevel
from subprocess import call

net = 0

def myNetwork() :
    global net
    net = Containernet( topo=None, build=False,ipBase='10.0.0.0/8')
    info( '*** Adding controller\n' )
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    c0=net.addController(name='c0', controller=RemoteController, ip='0.0.0.0', protocol='tcp', port=6633)
    info( '*** Add switches\n')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    d4 = net.addDocker('d4', ip='10.0.0.4',
    defaultRoute=None, dimage="ubuntu:trusty")
    d6 = net.addDocker('d6', ip='10.0.0.6',
    defaultRoute=None, dimage="ubuntu:trusty")
    d1 = net.addDocker('d1', ip='10.0.0.1',
    defaultRoute=None, dimage="ubuntu:trusty")
    d3 = net.addDocker('d3', ip='10.0.0.3',
    defaultRoute=None, dimage="mysql/mysql-server:latest")
    d2 = net.addDocker('d2', ip='10.0.0.2',
    defaultRoute=None, dimage="nazarpc/phpmyadmin:latest")
    d5 = net.addDocker('d5', ip='10.0.0.5',
    defaultRoute=None, dimage="mysql/mysql-server:latest")

    info( '*** Add links\n')
    net.addLink(s1, s2)
    net.addLink(s2, s5)
    net.addLink(s5, s3)
    net.addLink(s3, s1)
    net.addLink(s3, s2)
    #net.addLink(s1, s4)
    net.addLink(s4, s3)
    net.addLink(s4, d1)
    net.addLink(s4, d2)
    net.addLink(s3, d3)
    net.addLink(s3, d4)
    net.addLink(s5, d5)
    net.addLink(s5, d6)

    net.removeLink(None,s4,s3)

    info("*** starting net")
    net.start()
    info("*** Kodingan Tambahan Lordy\n")
    tambahDocker('11','10.0.0.11/8','ubuntu:trusty','s3')
    print('sudah ditambah')
    #CLI(net)
    #net.stop()

def tambahDocker(nomor, ipAddress, jenis, switchNo) :
    global net
    nomor='d'+nomor
    d11 = net.addDocker(nomor, defaultRoute=None, dimage=jenis)
    net.addLink(d11,net.get(switchNo),params1={"ip": ipAddress}) #aslinya /8
    #netBuild() unneeded
    #/8 netmask, buat nandain IP jaringannya yg mana, ga penting se

def netBuild() : #unneeded
    global net
    info( '*** Starting network versi LORDY\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
    info( '*** Starting switches\n')
    net.get('s5').start([net.get('c0')])
    net.get('s4').start([net.get('c0')])
    net.get('s3').start([net.get('c0')])
    net.get('s1').start([net.get('c0')])
    net.get('s2').start([net.get('c0')])
    info( '*** Post configure switches and hosts\n')

def lordyNet():
    global net
    return str(net.values())
    #return 0

def lordyAddSwitch(switchName):
    global net
    s_user = net.addSwitch(switchName, cls=OVSKernelSwitch)
    net.get(switchName).start([net.get('c0')])
    #net.addLink(s_user,net.get('s1'))

def lordyAddLink(source,dest) :
    global net
    net.addLink(net.get(source),net.get(dest))

def lordyDelLink(source,dest) :
    global net
    net.removeLink(None,net.get(source),net.get(dest))

if __name__ == '__main__' :
    setLogLevel( 'info' )
    #myNetwork()