#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []

def process_packet(packets):

    scapy_pack = scapy.IP(packets.get_payload())
    if scapy_pack.haslayer(scapy.Raw):

        try :
            if scapy_pack[scapy.TCP].dport == 80:
                print("[+] HTTP Request :")
                if ".exe" in scapy_pack[scapy.Raw].load:
                    ack_list.append(scapy_pack[TCP].ack)
                    print("ACK :", ack_list)

                    print(scapy_pack.show())
                #print(scapy_pack.show())
                #print(scapy_pack[scapy.Raw].load)

            elif scapy_pack[scapy.TCP].sport == 80:
                print("[+] HTTP Responce :")

        except IndexError or NameError:
            pass


    packets.accept()



queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
