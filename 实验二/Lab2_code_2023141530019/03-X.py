from scapy.all import *
from scapy.layers.inet import IP, TCP

dst_ip = "wjlpt.com"
src_port = RandShort()
dst_port = 22

xmas_scan_resp = sr1(IP(dst=dst_ip) / TCP(dport=dst_port, 
                                          flags="FSRPAUECN"), 
                timeout=1)

# 根据实际情况做修改
if (xmas_scan_resp == None):
    print("Open")
elif (xmas_scan_resp.haslayer(TCP)):
    if (xmas_scan_resp.getlayer(TCP).flags == "RA"):
        print("Closed")
