#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

ack_list = []


def process_packet(packet):

    scapy_pack = scapy.IP(packet.get_payload())
    if scapy_pack.haslayer(scapy.Raw):

        try:

            if scapy_pack[scapy.TCP].dport == 80:
                print("[+] HTTP Request :")
                if ".exe" in scapy_pack[scapy.Raw].load:
                    ack_list.append(scapy_pack[scapy.TCP].ack)
                    print("polo!")
                    print("ACK :", ack_list)

            elif scapy_pack[scapy.TCP].sport == 80:
                print("[+] HTTP Response :")

            elif scapy_pack[scapy.TCP] is False:
                print("not TCP, whatever ...")
        except Exception as e:
            print(e)
        packet.accept()


queue = netfilterqueue.NetfilterQueue()


queue.bind(1, process_packet)
queue.run()
