#!/usr/bin/env python

from re import search
from os import geteuid
from datetime import date
from random import randint
from scapy.all import get_if_list
from optparse import OptionParser
from time import strftime, localtime
from subprocess import call, check_output
from colorama import Fore, Back, Style

status_color = {
	'+': Fore.GREEN,
	'-': Fore.RED,
	'*': Fore.YELLOW,
	':': Fore.CYAN,
	' ': Fore.WHITE,
}

mac_elements = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
mac_divider = [':', '-']

def get_time():
	return strftime("%H:%M:%S", localtime())
def display(status, data):
	print(f"{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {get_time()}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}")

def get_arguments(*args):
	parser = OptionParser()
	for arg in args:
		parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
	return parser.parse_args()[0]

def check_root():
	return geteuid() == 0

def check_mac(mac):
	mac = mac.lower()
	for divider in mac_divider:
		parts = mac.split(divider)
		if len(parts) != 6:
			continue
		for elements in parts:
			for element in elements:
				if element not in mac_elements:
					return -1
		return ':'.join(parts)
	return -1
def generate_mac():
	return mac_elements[randint(0, 15)]+mac_elements[randint(0, 15)]+':'+mac_elements[randint(0, 15)]+mac_elements[randint(0, 15)]+':'+mac_elements[randint(0, 15)]+mac_elements[randint(0, 15)]+':'+mac_elements[randint(0, 15)]+mac_elements[randint(0, 15)]+':'+mac_elements[randint(0, 15)]+mac_elements[randint(0, 15)]+':'+mac_elements[randint(0, 15)]+mac_elements[randint(0, 15)]
def get_mac(interface):
	iface_info = check_output(["ifconfig", interface])
	search_result = search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", iface_info.decode())
	if search_result:
		return search_result.group(0)
	else:
		-1

def change_mac(interface, mac):
	call(["ifconfig", interface, "down"])
	call(["ifconfig", interface, "hw", "ether", mac])
	call(["ifconfig", interface, "up"])

def execute(data, verbose=False):
	if not check_root():
		if verbose:
			display('-', f"This Program requires {Back.MAGENTA}root{Back.RESET} Privileges")
		return -1
	if not data.interface:
		if verbose:
			display('-', "Please specify an Interface")
			display(':', f"Available Interfaces : {Back.MAGENTA}{get_if_list()}{Back.RESET}")
		return -2
	elif data.interface not in get_if_list():
		if verbose:
			display('-', f"Interface {Back.MAGENTA}{data.interface}{Back.RESET} not found!")
			display(':', f"Available Interfaces : {Back.MAGENTA}{get_if_list()}{Back.RESET}")
		return -3
	current_mac = get_mac(data.interface)
	if verbose:
		display(':', f"Current MAC Address of {Back.MAGENTA}{data.interface}{Back.RESET} = {Back.MAGENTA}{current_mac}{Back.RESET}")
	if not data.mac:
		if verbose:
			display('*', "No MAC Address specified! Generating Random MAC Address")
		data.mac = generate_mac()
		while data.mac == current_mac:
			data.mac = generate_mac()
	else:
		data.mac = check_mac(data.mac)
	if data.mac == -1:
		if verbose:
			display('-', f"Please Enter a valid MAC Address!")
			display(':', f"Format of Valid Mac Address = {Back.MAGENTA}XX:XX:XX:XX:XX:XX{Back.RESET} (where X = {Back.MAGENTA}{mac_elements}{Back.RESET})")
		return -3
	if verbose:
		display(':', f"Changing MAC Address of {Back.MAGENTA}{data.interface}{Back.RESET} to {Back.MAGENTA}{data.mac}{Back.RESET}")
	change_mac(data.interface, data.mac)
	new_mac = get_mac(data.interface)
	if new_mac != data.mac:
		if verbose:
			display('-', f"Failed to Change the MAC Address of {Back.MAGENTA}{data.interface}{Back.RESET}")
			display(':', f"Current MAC Address of {Back.MAGENTA}{data.interface}{Back.RESET} = {Back.MAGENTA}{new_mac}{Back.RESET}")
		return -4
	else:
		if verbose:
			display('+', f"Successfully Changed MAC Address of {Back.MAGENTA}{data.interface}{Back.RESET} to {Back.MAGENTA}{data.mac}{Back.RESET}")
		return 0

if __name__ == "__main__":
	data = get_arguments(('-i', "--iface", "interface", "interface to chance MAC Address of"),
		      			 ('-m', "--mac", "mac", "MAC Address to set"))
	execute(data, verbose=True)