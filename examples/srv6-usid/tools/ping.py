#! /usr/bin python3

# Set log level to benefit from Scapy warnings
import logging
logging.getLogger("scapy").setLevel(0)

from scapy.all import *

# sonic01:Ethernet4 = 52:54:00:74:c1:01
p0 = Ether(src = "fe:54:00:11:01:01", dst = "52:54:00:74:c1:01") \
/ IP(src = "10.101.1.100", dst = "10.101.2.1") / ICMP()
p0.show()
sendp(p0, iface="vnet1", count=4)
