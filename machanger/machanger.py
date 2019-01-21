#!/usr/bin/env python
import subprocess
import optparse
import re


def get_args():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="ifce", help="Choose interface ")
    parser.add_option("-m", "--mac", dest="mac", help="Input MAC ")
    (options, arguments) = parser.parse_args()

    if not options.ifce:
        parser.error("[-] Enter a valid interface, use --help for more info")
        exit(0)
    elif not options.mac:
        parser.error("[-] Enter a valid MAC address, use --help for more info")

    else:
        return options

def get_default_mac(interface):

    if_result = subprocess.check_output(["ifconfig", options.ifce])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", if_result)

    if new_mac:
        # print("[+] MAC updated to value {0}").format(mac)
        return new_mac.group(0)

    else:
        print("[-] Error MAC not changed ")


def macupdate(ifce, mac):

    print("[+] Using MAC " + mac + " for Interface " + ifce)

    if len(mac) != 17:
        print("[-] Invalid MAC address, exiting ...")
        exit(0)
    else:

        subprocess.call(["ifconfig", ifce, "down"])
        subprocess.call(["ifconfig", ifce, "hw", "ether", mac])
        subprocess.call(["ifconfig", ifce, "up"])


options = get_args()
get_mac = get_default_mac(options.ifce)
print("Current MAC is {0}").format(get_mac)
macupdate(options.ifce, options.mac)
get_mac = get_default_mac(options.ifce)

if get_mac == options.mac:
    print("[+] MAC Address successfully updated to {0}").format(get_mac)

else:

    print("[-] Unable to change MAC")


