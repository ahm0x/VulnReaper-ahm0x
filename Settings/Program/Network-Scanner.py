from Config.Util import *
from Config.Config import *
try:
    import socket
    import threading
    import ipaddress
    import subprocess
    import concurrent.futures
except Exception as e:
    ErrorModule(e)

Title("Network Scanner")

try:
    def ping_host(ip):
        try:
            if sys.platform.startswith("win"):
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], 
                                      capture_output=True, text=True, timeout=2)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                      capture_output=True, text=True, timeout=2)
            return result.returncode == 0
        except:
            return False

    def scan_port(ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            return result == 0
        except:
            return False

    def get_hostname(ip):
        try:
            hostname = socket.gethostbyaddr(str(ip))[0]
            return hostname
        except:
            return "Unknown"

    def scan_host(ip, common_ports):
        if ping_host(ip):
            hostname = get_hostname(ip)
            open_ports = []
            
            for port in common_ports:
                if scan_port(ip, port):
                    open_ports.append(port)
            
            if open_ports:
                ports_str = ', '.join(map(str, open_ports))
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Host: {white}{ip}{green} ({hostname}) Ports: {white}{ports_str}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Host: {white}{ip}{red} ({hostname}) - No common ports open")

    Slow(wifi_banner)
    
    print(f"""
 {BEFORE}01{AFTER}{white} Scan local network (192.168.1.0/24)
 {BEFORE}02{AFTER}{white} Scan custom network range
 {BEFORE}03{AFTER}{white} Scan single host
    """)
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]
    
    if choice in ['1', '01']:
        network = ipaddress.IPv4Network('192.168.1.0/24', strict=False)
        hosts = list(network.hosts())
    elif choice in ['2', '02']:
        network_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Network range (e.g., 192.168.1.0/24) -> {reset}")
        try:
            network = ipaddress.IPv4Network(network_input, strict=False)
            hosts = list(network.hosts())
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid network range")
            Continue()
            Reset()
    elif choice in ['3', '03']:
        host_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target host -> {reset}")
        try:
            hosts = [ipaddress.IPv4Address(host_input)]
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid host address")
            Continue()
            Reset()
    else:
        ErrorChoice()

    try:
        threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 50) -> {reset}"))
    except:
        threads_number = 50

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning {white}{len(hosts)}{red} hosts...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_number) as executor:
        futures = [executor.submit(scan_host, ip, common_ports) for ip in hosts]
        concurrent.futures.wait(futures)

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Network scan completed")
    Continue()
    Reset()
except Exception as e:
    Error(e)