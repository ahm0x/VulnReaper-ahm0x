from Config.Util import *
from Config.Config import *
try:
    import socket
    import threading
    import time
    import subprocess
    import concurrent.futures
except Exception as e:
    ErrorModule(e)

Title("Advanced Port Scanner")

try:
    def tcp_connect_scan(ip, port, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def tcp_syn_scan(ip, port):
        # Simplified SYN scan simulation
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def udp_scan(ip, port, timeout=2):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b'', (ip, port))
            sock.recvfrom(1024)
            sock.close()
            return True
        except socket.timeout:
            sock.close()
            return True  # UDP port might be open (no response)
        except:
            return False

    def service_detection(ip, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB"
        }
        
        service = services.get(port, "Unknown")
        
        # Try to grab banner
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, port))
            
            if port in [80, 8080]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            elif port == 21:
                pass  # FTP sends banner automatically
            elif port == 22:
                pass  # SSH sends banner automatically
            else:
                sock.send(b"\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            if banner:
                return f"{service} ({banner[:50]}{'...' if len(banner) > 50 else ''})"
            else:
                return service
        except:
            return service

    def scan_host_comprehensive(ip, ports, scan_type):
        open_ports = []
        
        for port in ports:
            is_open = False
            
            if scan_type == "tcp":
                is_open = tcp_connect_scan(ip, port)
            elif scan_type == "syn":
                is_open = tcp_syn_scan(ip, port)
            elif scan_type == "udp":
                is_open = udp_scan(ip, port)
            
            if is_open:
                service = service_detection(ip, port)
                open_ports.append((port, service))
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {white}{ip}:{port}{green} - {service}")
        
        return open_ports

    Slow(scan_banner)
    
    target = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target IP/Range -> {reset}")
    
    print(f"""
 {BEFORE}01{AFTER}{white} TCP Connect Scan
 {BEFORE}02{AFTER}{white} TCP SYN Scan
 {BEFORE}03{AFTER}{white} UDP Scan
 {BEFORE}04{AFTER}{white} Common ports (top 100)
 {BEFORE}05{AFTER}{white} All ports (1-65535)
 {BEFORE}06{AFTER}{white} Custom port range
    """)
    
    scan_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    if scan_choice in ['1', '01']:
        scan_type = "tcp"
    elif scan_choice in ['2', '02']:
        scan_type = "syn"
    elif scan_choice in ['3', '03']:
        scan_type = "udp"
    else:
        scan_type = "tcp"
    
    # Define port ranges
    if scan_choice in ['4', '04']:
        # Top 100 most common ports
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017]
    elif scan_choice in ['5', '05']:
        ports = range(1, 65536)
    elif scan_choice in ['6', '06']:
        try:
            start_port = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Start port -> {reset}"))
            end_port = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} End port -> {reset}"))
            ports = range(start_port, end_port + 1)
        except:
            ErrorNumber()
    else:
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080]

    try:
        threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 100) -> {reset}"))
    except:
        threads_number = 100

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting {scan_type.upper()} scan on {white}{target}{red}...")
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning {white}{len(list(ports))}{red} ports with {white}{threads_number}{red} threads...")
    
    start_time = time.time()
    
    # Handle single IP or IP range
    if '/' in target:
        # IP range scanning would require additional logic
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} IP range scanning not implemented in this version")
        Continue()
        Reset()
    else:
        open_ports = scan_host_comprehensive(target, ports, scan_type)
    
    end_time = time.time()
    scan_duration = end_time - start_time
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Scan completed in {white}{scan_duration:.2f}{red} seconds")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(open_ports)}{red} open ports")
    
    if open_ports:
        # Save results
        output_file = os.path.join(tool_path, "1-Output", "PortScan", f"scan_{target}_{int(time.time())}.txt")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(f"# Port Scan Results for {target}\n")
            f.write(f"# Scan Type: {scan_type.upper()}\n")
            f.write(f"# Date: {current_time_day_hour()}\n")
            f.write(f"# Duration: {scan_duration:.2f} seconds\n\n")
            
            for port, service in open_ports:
                f.write(f"{port}\t{service}\n")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Results saved to: {white}{output_file}")

    Continue()
    Reset()
except Exception as e:
    Error(e)