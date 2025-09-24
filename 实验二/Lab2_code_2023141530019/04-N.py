from scapy.all import *
from scapy.layers.inet import IP, TCP

dst_ip = "wjlpt.com"
src_port = RandShort()
dst_port = 80

null_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags=""),timeout=1)
print(null_scan_resp)
# 根据实际情况做修改
if (null_scan_resp==None):
    print("Open|Filtered")
elif(null_scan_resp.haslayer(TCP)):
    if(null_scan_resp.getlayer(TCP).flags == "RA"):
        print("Closed")