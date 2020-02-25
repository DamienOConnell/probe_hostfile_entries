#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#

# NEXT: TO_DO:
# Create a new class:  class HostList():
#
#

import ipaddress
import validators
from pprint import pprint


class IPv4Host:

    import time

    def __init__(self, ipaddress, hostname) -> None:

        """
        self.hostname = hostname        (string: valid hostname)
        self.ipv4address = ipaddress    (string: IPV4 address in dotted decimal format)
        tcpport = 0                     (integer: 1-65535)
        ping_status = "untested"        (string: "untested", "failed", "success")
        """

        self.hostname = hostname
        self.ipv4address = ipaddress
        self.tcpport = 0
        self.ping_status = "untested"
        self.tcp_status = "untested"

    def __str__(self):
        return str(self.__dict__)

    # def __repr__(self):
    #     attrs = str([(x, self.__dict__[x]) for x in self.__dict__])
    #     return "<IPv4Host: %s>" % attr

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

    def tcp_test(self, timeout):

        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            print("tcp_test: about to open")
            # double bracket needed so as to pass a tuple, not two args
            s.connect((self.ipv4address, int(self.tcpport)))
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
        timeout = 3  # Socket initialization timeout, used in tcp_test()
        interval = 3  # Will wait this long before retrying checks

        for i in range(retry):
            # if self.tcp_test(self.ipv4address, self.tcpport):
            if self.tcp_test(timeout):
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
                    host_list.append(IPv4Host(result[0], result[1]))
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

    args = get_args()
    count = 0
    host_list = read_hosts_file(args.infiles)

    print("\n\n--- A list of hosts, no tests have been done yet ----------")
    for host in host_list:
        print(host)

    for host in host_list:
        host.tcpport = 22

    print("\n\n--- tcpport is now set to 22 for each host ----------------")
    for host in host_list:
        print(host)

    for host in host_list:
        host.ping()

    print("\n\n--- A list of hosts, ping() has been tried for each one ---")
    for host in host_list:
        print(host)

    for host in host_list:
        host.test_host_tcp()

    print("\n\n--- A list of hosts, tcptest() has been tried for each  ---")
    for host in host_list:
        print(host)


if __name__ == "__main__":
    main()
