#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
import ipaddress
import socket

def hostnameResolves(hostname: str) -> bool:
    import socket

    # can this name be resolved to IPV4ADDRESS?
    try:
        ipaddr = socket.gethostbyname(hostname.strip())
        return True

    except NameError:
        return False

    except socket.gaierror as e:
        # this should go to logger:
        # print(f"Unable to resolve hostname {hostname} --- Exception: e {e}")
        return False

    print("end of the hostnameResolves function")


def validIP(address: str) -> bool:
    from ipaddress import ip_address

    #
    # Input could be
    # - IP in dotted notation
    #   - use checkIP to see if this is a valid IP address.
    # - a string
    #   - try to resolves this to a an IP address.
    #   - use checkIP to see that the result is a valid IP.
    try:
        # Return an IPv4Address or IPv6Address object depending on the IP address
        # passed as argument. Either IPv4 or IPv6 addresses may be supplied;
        # integers less than 2**32 will be considered to be IPv4 by default.
        # A ValueError is raised if address does not represent a valid IPv4 or IPv6 address.
        #
        newIP = ip_address(address)
    except ValueError:
        # should use logger here:
        # print(f"validIP:: address {address} was a dud")
        return False
    except socket.gaierror:
        print(f"validIP:: Nodename not valid ....")

    return True




addresses = [
    "127.0.0.1",
    "255.255.255.255",
    "1.1.1.1",
    "1.a.2.3",
    "www.idx.com.au",
    "8.8.8.8",
    "139.130.4.4",
]
for address in addresses:
    print(f"{'-' * 10} Checking {address} {'-' * 10}")
    if hostnameResolves(address):
        print(f"Valid hostname::  {address} ...")
    else:
        print(f"NOT A VALID HOSTNAME::  {address} ...")

    if validIP(address):
        print(f"Valid IP address  {address} ...\n")
    else:
        print(f"NOT a valid IP address {address} ...\n")
