from ast import arguments
import scapy.all as scapy
import optparse

#this function get the IP range from the user when they type in the command
def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i","--ip", dest="ip_range", help="Enter IP range to scan")
    (options,arguments) = parser.parse_args()
    return options

#This function sends out the broadcast
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether()
    broadcast =scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    clients_list = []
    
    for element in answered_list:
        client_dict = {"ip":element[1].psrc, "MAC":element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["MAC"])

options = get_args()

scan_result = scan(options.ip_range)
print_result(scan_result)