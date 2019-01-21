#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
# Require iptables queue on Forward chain

def process_packet(packet):

    scapy_pack = scapy.IP(packet.get_payload())
    print(scapy_pack.show())
    #print(polo.get_payload())
    #forward the packet
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
