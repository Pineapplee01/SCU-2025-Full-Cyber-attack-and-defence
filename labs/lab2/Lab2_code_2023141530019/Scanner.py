from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP

dst_ip = "10.133.25.169"
src_port = RandShort()

def ICMP_scan():
    # ICMP Ping Scan
    print("ICMP Ping Scan")

    # 定义发送与ICMP包的接收
    try:
        icmp_pkt = IP(dst=dst_ip)/ICMP()
        icmp_resp = sr1(icmp_pkt, timeout=2, verbose=0)

        if icmp_resp is None:
            print(f"[✗] {dst_ip} Host is down or unresponsive")
        elif icmp_resp.haslayer(ICMP):
            if icmp_resp.getlayer(ICMP).type == 0:
                print(f"[✓] {dst_ip} Host is up")
                return True
            else:
                print(f"[!] {dst_ip} Unrecognized ICMP response (type: {icmp_resp.getlayer(ICMP).type})")
                return False

    except Exception as e:
        print(f"ICMP Scan Error: {e}")
        return False

def Port_scan(dst_ip, scan_name, tcp_layer, timeout):

    try:
        scan_resp = sr1(IP(dst=dst_ip)/tcp_layer, timeout=timeout, verbose=0)
        
        print(scan_resp)
        # 根据实际情况做修改
        if (scan_resp==None):
            print("Open")
            return True
        elif(scan_resp.haslayer(TCP)):
            if(scan_resp.getlayer(TCP).flags == "RA"):
                print("Closed")
                return False

    except Exception as e:
        return f"Error: {e}"




def main():

    # 端口扫描配置
    scan_types = {
        "SYN Scan": TCP(sport=src_port, dport=80, flags="S"),
        "FIN Scan": TCP(sport=src_port, dport=80, flags="F"),
        "XMAS Scan": TCP(sport=src_port, dport=80, flags="FPU"),
        "NULL Scan": TCP(sport=src_port, dport=80, flags="")
    }

    Timeout = {
        "SYN Scan": 10,
        "FIN Scan": 1,
        "XMAS Scan": 1,
        "NULL Scan": 1
    }

    host_up = ICMP_scan()
    if not host_up:
        print("[!] Host is down, exiting scanner")
        return

    # 显示扫描选项
    print("Available scan types:")
    for scan in scan_types.keys():
        print(scan)
    
    scan_options = list(scan_types.keys())
    for i, scan_name in enumerate(scan_options, 1):
        port = scan_types[scan_name].dport
        print(f"{i}. {scan_name} (port number {port})")

    print("0. Exit")

    while True:
        try:
            print("\nPlease select a scan type (enter number):")
            choice = input("> ").strip()
            
            if choice == "0":
                print("Exiting scanner")
                break
            
            elif choice in ["1", "2", "3", "4"]:
                # 执行单个扫描
                scan_index = int(choice) - 1
                scan_name = scan_options[scan_index]
                tcp_layer = scan_types[scan_name]
                timeout = Timeout[scan_name]

                print(f"\nExecuting {scan_name}...")
                result = Port_scan(dst_ip, scan_name, tcp_layer, timeout)
                print(f"Result: {result}")
            else:
                print("Invalid selection, please enter 0-4")

        except KeyboardInterrupt:
            print("\n\nUser interrupted, exiting scanner")
            break
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()