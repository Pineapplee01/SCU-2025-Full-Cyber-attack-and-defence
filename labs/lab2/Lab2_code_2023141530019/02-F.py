from scapy.all import *
from scapy.layers.inet import IP, TCP

dst_ip = "10.133.25.169"
src_port = RandShort()
dst_port = 82

fin_scan_resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, 
                                         dport=dst_port,
                                         flags="F"),
                timeout=1)


print(fin_scan_resp)
# 根据实际情况做修改
if (fin_scan_resp == None):
    print("Open")
elif (fin_scan_resp.haslayer(TCP)):
    if (fin_scan_resp.getlayer(TCP).flags == "RA"):
        print("Closed")
