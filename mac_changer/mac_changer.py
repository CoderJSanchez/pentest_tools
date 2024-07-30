import subprocess as sb
import optparse
import re

#commands used to parse the user input when typing out the command from the command line
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC address")
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] You did not enter a usable interface")
    elif not options.new_mac_address:
        parser.error("[-] You did not enter a usable MAC address")
    return options


#function that runs the commands to change the MAC address
def change_mac(interface, new_mac_address):
    #print(f'[+] Changing MAC address for {interface}')

    sb.call(["ifconfig", interface, "down"])
    sb.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    sb.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = str(sb.check_output(["ifconfig", interface]))
    mac_address_search_result  = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f'Current MAC is {current_mac}')


#calling the function change_mac() that was created at the top
change_mac(options.interface, options.new_mac_address)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac_address:
    print(f'[+] MAC address was successfully changed to {current_mac}')
else:
    print(f'[-] MAC address did not get changed.')