#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#

# NEXT: TO_DO:
# parse arguments for
#   tcp test
#   icmp test
#   tcp_port to probe
#   timeout
#   wait
# TCP test parameters:
#   retry = 4
#   delay = 2
#   interval = 3
# Add UDP test
#   with check for netcat
#   udp_port to probe


import ipaddress
import validators
from pprint import pprint


def line() -> None:
    print("-" * 80)


class HostList(object):

    """ Dictionary
        key: hostname (str) 
        value: IPHost (objects) - refer to class IPHost()
    """

    def __init__(self):
        self._hosts = {}

    def host(self, hostname, ipaddress, tcp_timeout, tcp_port):
        if hostname not in self._hosts:
            self._hosts[hostname] = IPHost(ipaddress, tcp_timeout, tcp_port)
        return self._hosts[hostname]

    def print_myself(self) -> None:
        for hostname in self._hosts:
            line()
            print(f"{hostname} [{self._hosts[hostname].ipv4address}]")
            print(f"TCP port\t{self._hosts[hostname].tcp_port}")
            print(f"TCP timeout\t{self._hosts[hostname].tcp_timeout}")
            print(f"ICMP state:\t{self._hosts[hostname].ping_status}")
            print(f"TCP state:\t{self._hosts[hostname].tcp_status}")

    def icmp_poll_myhosts(self):
        for hostname in self._hosts:
            self._hosts[hostname].ping()

    def tcp_poll_myhosts(self):
        for hostname in self._hosts:
            self._hosts[hostname].tcp_test()


class IPHost:

    import time

    def __init__(self, ipaddress, tcp_timeout=3, tcp_port=22) -> None:

        """
        self.hostname = hostname        (string: valid hostname)
        self.ipv4address = ipaddress    (string: IPV4 address in dotted decimal format)
        tcp_port = 0                     (integer: 1-65535)
        ping_status = "untested"        (string: "untested", "failed", "success")
        """

        # self.hostname = hostname
        self.ipv4address = ipaddress
        self.tcp_port = 0
        self.ping_status = "untested"
        self.tcp_status = "untested"
        self.tcp_timeout = tcp_timeout
        self.tcp_port = tcp_port

    def __str__(self):
        return str(self.__dict__)

    # def __repr__(self):
    #     attrs = str([(x, self.__dict__[x]) for x in self.__dict__])
    #     return "<IPHost: %s>" % attr

    def ping(self):
        """
        Returns True if host responds to a ping request
        """
        import subprocess, platform

        # Ping parameters differ for Windows vs. OSX/Linux OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

        status, result = subprocess.getstatusoutput(
            "ping " + " " + ping_str + " " + self.ipv4address
        )
        if status == 0:  # successful ping
            self.ping_status = "success"

        else:
            self.ping_status = "failure"

    def tcp_test(self):

        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.tcp_timeout)
        try:
            print("tcp_test: about to open")
            # double bracket needed so as to pass a tuple, not two args
            s.connect((self.ipv4address, int(self.tcp_port)))
            s.shutdown(socket.SHUT_RDWR)
            print("tcp_test: connect OK")
            self.tcp_status = "success"
            return True
        except:
            self.tcp_status = "failed"
            return False
        finally:
            s.close()

    def test_host_tcp(self):
        import time

        retry = 4
        delay = 2
        interval = 3  # Will wait this long before retrying checks

        for i in range(retry):
            # if self.tcp_test(self.ipv4address, self.tcp_port):
            if self.tcp_test():
                self.tcp_status = "success"
                break
            else:
                print("No response:" + self.ipv4address)
                time.sleep(delay)
                self.tcp_status = "failure"


def read_hosts_file(hostfile: str = "/etc/hosts") -> list:

    import sys

    # Input: name of hosts file
    # Output: list of tuples, each containing: (ipaddress, hostname)
    host_list = []
    try:
        with open(hostfile) as fp:
            while True:
                line = fp.readline()
                if not line:  # i.e. this is EOF
                    break
                line = line.strip().lstrip()
                result = line.split()

                if (
                    (len(result) > 1)
                    and (result[0][0] != "#")
                    and (validators.ip_address.ipv4(result[0]))
                    and (validators.domain(result[1] + ".com"))
                ):
                    # NB: double brackets to pass a tuple
                    # host_list.append(IPHost(result[0], result[1]))
                    host_list.append((result[0], result[1]))
    except FileNotFoundError:
        print(f"Error 'FileNotFoundError:' hosts file {hostfile}.")
    except PermissionError:
        print(f"Error 'PermissionError: access to file {hostfile}  ... ")
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except:  # handle other exceptions such as attribute errors
        print(f"Unexpected error:{sys.exc_info()[0]}")
    return host_list


def get_args():

    import argparse

    parser = argparse.ArgumentParser(description="ping host file entries")
    parser.add_argument("infiles", metavar="N", type=str, help="Host file to use as input.")
    parser.add_argument("-n", "--linenumbers", action="store_true", help="number lines.")
    args = parser.parse_args()

    return args


def main():

    tcp_timeout = 5  # Socket initialization timeout, used in tcp_test()
    tcp_port = 443  # port to be probed

    args = get_args()
    count = 0
    host_list_as_tuples = read_hosts_file(args.infiles)
    my_host_list = HostList()

    print("\n\n--- A list of hosts, no tests have been done yet ----------")
    for ipaddress, hostname in host_list_as_tuples:
        print(f"{ipaddress} - {hostname}")
        my_host_list.host(hostname, ipaddress, tcp_timeout, tcp_port)

    print("--- NO POLLING DONE YET")
    my_host_list.print_myself()

    my_host_list.icmp_poll_myhosts()
    print("--- ICMP POLLING IS DONE")
    my_host_list.print_myself()

    my_host_list.tcp_poll_myhosts()
    print("--- TCP POLLING IS DONE")
    my_host_list.print_myself()


if __name__ == "__main__":
    main()
