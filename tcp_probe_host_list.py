#!/usr/bin/python

from pprint import pprint
import datetime
import socket
import threading
import time

def probeHostList(hosts):

    while True:
        changes = []
        threads = []
        for host in hosts:
            t = threading.Thread(target=parseHost, args=(host,))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if len(changes) > 0:
            sendMessage()
            del changes[:]
        del threads[:]

        # it's all over
        pprint(hostlist)
        break

def printD(string, indent):
    strindent = ""
    for x in range(0, indent):
        strindent = strindent + " "
    print(
        "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]" + strindent + " " + string
    )


def tcpCheck(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


def checkHost(host):

    ipup = False
    for i in range(retry):
        if tcpCheck(host["ip"], host["port"]):
            ipup = True
            break
        else:
            printD(
                "No response from "
                + host["ip"]
                + ":"
                + str(host["port"])
                + ":"
                + host["conntype"]
                + ", retrying in "
                + str(delay)
                + "s...",
                0,
            )
            time.sleep(delay)
    return ipup


def parseHost(host):

    prestatus = host["status"]
    printD("Checking " + host["ip"] + ":" + str(host["port"]) + ":" + host["conntype"] + "...", 0)
    if checkHost(host):
        host["status"] = "up"
        if prestatus == "down":
            changes.append(
                host["ip"]
                + ":"
                + str(host["port"])
                + ":"
                + host["conntype"]
                + " is "
                + host["status"]
            )
    else:
        host["status"] = "down"
        if prestatus == "up":
            changes.append(
                host["ip"]
                + ":"
                + str(host["port"])
                + ":"
                + host["conntype"]
                + " is "
                + host["status"]
            )
    printD(
        "Status of "
        + host["ip"]
        + ":"
        + str(host["port"])
        + ":"
        + host["conntype"]
        + ": "
        + host["status"],
        0,
    )


retry = 1
delay = 2
timeout = 3  # Socket initialization timeout, used in tcpCheck()
interval = 3  # Will wait this long before retrying checks

hosts = []
hostlist = ["172.30.30.5", "172.30.30.30"]
hostlist = ["172.30.30.5", "172.30.30.9", "172.30.30.30"]
port = 22

for ip in hostlist:
    conntype = "tcp"
    hosts.append({"ip": ip, "port": port, "conntype": "tcp", "status": "unknown"})

pprint(hosts)
probeHostList(hosts)
