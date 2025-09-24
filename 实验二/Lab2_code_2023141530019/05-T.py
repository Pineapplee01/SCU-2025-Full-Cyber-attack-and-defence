from scapy.all import *
from scapy.layers.inet import IP, TCP

dst_ip = "wjlpt.com"
src_port = RandShort()
dst_port = 22

tcp_connect_scan_resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S"), timeout=10)
# 根据实际情况做修改
if (str(type(tcp_connect_scan_resp)) == ""):
    print("Closed")
elif (tcp_connect_scan_resp.haslayer(TCP)):
    print(tcp_connect_scan_resp.getlayer(TCP).flags)
    if (tcp_connect_scan_resp.getlayer(TCP).flags == "SA"):
        send_rst = sr(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="AR"), timeout=10)  # 全连接 AR => ACK+RST
        print("Open")
    elif (tcp_connect_scan_resp.getlayer(TCP).flags == "RA"):
        print("Closed")


