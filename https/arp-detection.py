#!/usr/bin/env python
import scapy.all as scapy
import time


def get_mac(ip):

    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    # print(arp_req_broadcast.summary())
    answer_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=0)[0]
    # print(answer_list[0])
    return answer_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=packet_Capt)


def packet_Capt(packet):



    try:

        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            mac = packet[scapy.ARP].hwsrc

            if real_mac != mac:
                print("ARP attack detected...\n")
                print("Check malicious MAC: {0} ").format(packet[scapy.ARP].hwsrc)
                time.sleep(2)
                exit(0)
            # else:
            #     print("So far so good ...")

    except IndexError:
        pass


sniff("eth0")
