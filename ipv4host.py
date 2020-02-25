#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
#


# ipv4host
class IPv4Host:
    def __init__(self, keydata: dict, mandatory: dict, loggername="") -> None:

        """
        self.hostname = hostname        (string: valid hostname)
        self.ipv4address = ipaddress    (string: IPV4 address in dotted decimal format)
        tcpport = 0                     (integer: 1-65535)
        ping_status = "untested"        (string: "untested", "failed", "success")
        """

        self.hostname = hostname
        self.ipv4address = ipaddress
        tcpport = 0
        ping_status = "untested"

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        attrs = str([(x, self.__dict__[x]) for x in self.__dict__])
        return "<IPv4Host: %s>" % attr
