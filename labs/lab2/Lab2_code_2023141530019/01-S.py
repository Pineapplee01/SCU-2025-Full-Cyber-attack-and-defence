from scapy.all import *
from scapy.layers.inet import IP, TCP

dst_ip = "10.132.160.47"
src_port = RandShort()
dst_port = 80

stealth_scan_resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S"), timeout=10)
if (stealth_scan_resp is None):
    print("Closed")
elif (stealth_scan_resp.haslayer(TCP)):
    if (stealth_scan_resp.getlayer(TCP).flags == "SA"):
        print("Open")
    else:
        print("Closed")
