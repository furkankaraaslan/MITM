import scapy.all as scapy
from scapy.layers import http
import optparse


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface", dest="interface_name", help="Enter interface name")
    (users_input, arguments) = parse_object.parse_args()

    if not users_input.interface_name:
        print("Enter interface name")

    return users_input


def listen_packets(interface):
    scapy.sniff(iface=interface, store=False, prn=analyze_packets)


def analyze_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)


user_input = get_user_input()
target_interface = user_input.interface_name
listen_packets(target_interface)
