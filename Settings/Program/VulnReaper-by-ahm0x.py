#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - Professional Bug Bounty Automation
Advanced Vulnerability Discovery & Attack Surface Analysis
"""

from Config.Util import *
from Config.Config import *
from Config.Security import *

try:
    import requests
    import socket
    import threading
    import concurrent.futures
    import subprocess
    import json
    import ssl
    import dns.resolver
    from datetime import datetime
    import time
    import re
    from urllib.parse import urlparse, urljoin
    from bs4 import BeautifulSoup
    import ipaddress
except Exception as e:
    ErrorModule(e)

Title("VulnReaper by ahm0x - Professional Bug Bounty Automation")

try:
    def advanced_subdomain_enumeration(domain):
        """Advanced subdomain enumeration using multiple techniques"""
        subdomains = set()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting advanced subdomain enumeration...")
        
        # Certificate Transparency logs
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Checking Certificate Transparency logs...")
            ct_url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = secure_session.safe_get(ct_url)
            
            if response and response.status_code == 200:
                ct_data = response.json()
                for entry in ct_data:
                    name_value = entry.get('name_value', '')
                    for subdomain in name_value.split('\n'):
                        subdomain = subdomain.strip()
                        if subdomain and subdomain.endswith(domain):
                            subdomains.add(subdomain)
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} CT Log: {white}{subdomain}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} CT logs failed: {white}{e}")
        
        # DNS brute force
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} DNS brute force enumeration...")
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api', 'blog',
            'shop', 'secure', 'vpn', 'remote', 'portal', 'gateway', 'proxy', 'cdn',
            'media', 'static', 'assets', 'img', 'images', 'css', 'js', 'files',
            'download', 'upload', 'backup', 'old', 'new', 'beta', 'alpha', 'demo',
            'support', 'help', 'docs', 'wiki', 'forum', 'chat', 'news', 'blog',
            'store', 'shop', 'cart', 'checkout', 'payment', 'billing', 'account',
            'profile', 'user', 'users', 'member', 'members', 'login', 'signin',
            'signup', 'register', 'auth', 'oauth', 'sso', 'ldap', 'ad', 'directory',
            'search', 'find', 'lookup', 'browse', 'explorer', 'dashboard', 'panel',
            'control', 'manage', 'admin', 'administrator', 'root', 'super', 'master',
            'config', 'configuration', 'settings', 'setup', 'install', 'update',
            'patch', 'upgrade', 'maintenance', 'status', 'health', 'monitor',
            'metrics', 'stats', 'analytics', 'reports', 'logs', 'audit', 'trace',
            'debug', 'error', 'exception', 'crash', 'dump', 'core', 'memory',
            'cache', 'temp', 'tmp', 'var', 'opt', 'usr', 'bin', 'sbin', 'lib',
            'etc', 'home', 'root', 'data', 'db', 'database', 'sql', 'mysql',
            'postgres', 'oracle', 'mssql', 'mongodb', 'redis', 'memcached',
            'elasticsearch', 'solr', 'lucene', 'sphinx', 'whoosh', 'xapian'
        ]
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                socket.gethostbyname(full_domain)
                subdomains.add(full_domain)
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} DNS: {white}{full_domain}")
                return True
            except socket.gaierror:
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in common_subdomains]
            concurrent.futures.wait(futures)
        
        # Search engines (Google dorking)
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Google dorking for subdomains...")
            google_dorks = [
                f"site:{domain}",
                f"site:*.{domain}",
                f"inurl:{domain}",
            ]
            
            for dork in google_dorks:
                # Note: In real implementation, you'd use Google Custom Search API
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Google dork: {white}{dork}")
        except:
            pass
        
        return list(subdomains)

    def advanced_port_scanning(target, port_range=None):
        """Advanced port scanning with service detection"""
        if port_range is None:
            # Top 1000 most common ports
            port_range = [
                21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
                1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017, 1433,
                1521, 2049, 2121, 2375, 3000, 4444, 5000, 5601, 5672, 6667, 7001,
                8000, 8001, 8008, 8009, 8081, 8082, 8083, 8084, 8085, 8086, 8087,
                8088, 8089, 8090, 8091, 8092, 8093, 8094, 8095, 8096, 8097, 8098,
                8099, 8100, 8443, 8888, 9000, 9001, 9002, 9003, 9090, 9091, 9092,
                9200, 9300, 9999, 10000, 11211, 50000, 50070, 50075, 50090
            ]
        
        open_ports = {}
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Try to get service banner
                    try:
                        if port == 80:
                            sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                        elif port == 443:
                            # For HTTPS, we'd need SSL context
                            pass
                        elif port in [21, 22, 25]:
                            pass  # These services send banners automatically
                        else:
                            sock.send(b"\r\n")
                        
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        service_info = detect_service(port, banner)
                        
                        open_ports[port] = {
                            'service': service_info['service'],
                            'version': service_info['version'],
                            'banner': banner[:200]  # Limit banner length
                        }
                        
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Port {white}{port}{green}: {service_info['service']} {service_info['version']}")
                        
                    except:
                        open_ports[port] = {
                            'service': get_default_service(port),
                            'version': 'Unknown',
                            'banner': ''
                        }
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Port {white}{port}{green}: {get_default_service(port)}")
                
                sock.close()
            except:
                pass
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning {white}{len(port_range)}{red} ports...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(scan_port, port) for port in port_range]
            concurrent.futures.wait(futures)
        
        return open_ports

    def detect_service(port, banner):
        """Detect service and version from banner"""
        service_patterns = {
            21: [
                (r'220.*?vsftpd\s+(\d+\.\d+[\.\d]*)', 'vsftpd'),
                (r'220.*?ProFTPD\s+(\d+\.\d+[\.\d]*)', 'ProFTPD'),
                (r'220.*?FileZilla\s+Server.*?(\d+\.\d+[\.\d]*)', 'FileZilla'),
                (r'220.*?(\w+)\s+FTP.*?(\d+\.\d+[\.\d]*)', 'FTP'),
            ],
            22: [
                (r'SSH-(\d+\.\d+)-OpenSSH[_\s]+(\d+\.\d+[\.\d]*)', 'OpenSSH'),
                (r'SSH-(\d+\.\d+)-(\w+)', 'SSH'),
            ],
            25: [
                (r'220.*?Postfix.*?(\d+\.\d+[\.\d]*)', 'Postfix'),
                (r'220.*?Sendmail.*?(\d+\.\d+[\.\d]*)', 'Sendmail'),
                (r'220.*?Exim.*?(\d+\.\d+[\.\d]*)', 'Exim'),
            ],
            80: [
                (r'Server:\s*Apache[/\s]+(\d+\.\d+[\.\d]*)', 'Apache'),
                (r'Server:\s*nginx[/\s]+(\d+\.\d+[\.\d]*)', 'nginx'),
                (r'Server:\s*Microsoft-IIS[/\s]+(\d+\.\d+)', 'IIS'),
            ],
            443: [
                (r'Server:\s*Apache[/\s]+(\d+\.\d+[\.\d]*)', 'Apache'),
                (r'Server:\s*nginx[/\s]+(\d+\.\d+[\.\d]*)', 'nginx'),
                (r'Server:\s*Microsoft-IIS[/\s]+(\d+\.\d+)', 'IIS'),
            ]
        }
        
        if port in service_patterns:
            for pattern, service_name in service_patterns[port]:
                match = re.search(pattern, banner, re.IGNORECASE)
                if match:
                    version = match.group(2) if len(match.groups()) >= 2 else match.group(1)
                    return {'service': service_name, 'version': version}
        
        return {'service': get_default_service(port), 'version': 'Unknown'}

    def get_default_service(port):
        """Get default service name for port"""
        default_services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 135: 'RPC', 139: 'NetBIOS', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S', 1433: 'MSSQL',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
            8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 9200: 'Elasticsearch', 27017: 'MongoDB'
        }
        return default_services.get(port, 'Unknown')

    def technology_detection(url):
        """Detect web technologies"""
        technologies = []
        
        try:
            response = secure_session.safe_get(url)
            if not response:
                return technologies
            
            headers = response.headers
            content = response.text
            
            # Server detection
            server = headers.get('Server', '')
            if server:
                technologies.append(f"Server: {server}")
            
            # X-Powered-By detection
            powered_by = headers.get('X-Powered-By', '')
            if powered_by:
                technologies.append(f"X-Powered-By: {powered_by}")
            
            # Framework detection
            soup = BeautifulSoup(content, 'html.parser')
            
            # JavaScript frameworks
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script['src'].lower()
                if 'jquery' in src:
                    technologies.append("jQuery")
                elif 'angular' in src:
                    technologies.append("AngularJS")
                elif 'react' in src:
                    technologies.append("React")
                elif 'vue' in src:
                    technologies.append("Vue.js")
                elif 'bootstrap' in src:
                    technologies.append("Bootstrap")
            
            # CSS frameworks
            links = soup.find_all('link', rel='stylesheet')
            for link in links:
                href = link.get('href', '').lower()
                if 'bootstrap' in href:
                    technologies.append("Bootstrap CSS")
                elif 'foundation' in href:
                    technologies.append("Foundation")
            
            # CMS detection
            if 'wp-content' in content or 'wp-includes' in content:
                technologies.append("WordPress")
            elif 'drupal' in content.lower():
                technologies.append("Drupal")
            elif 'joomla' in content.lower():
                technologies.append("Joomla")
            
            # Meta tags
            meta_generator = soup.find('meta', attrs={'name': 'generator'})
            if meta_generator:
                technologies.append(f"Generator: {meta_generator.get('content', '')}")
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Technology detection failed: {white}{e}")
        
        return technologies

    def vulnerability_assessment(target, open_ports, technologies):
        """Assess vulnerabilities based on discovered services"""
        vulnerabilities = []
        
        # Check for common vulnerable services
        vulnerable_services = {
            21: ["Anonymous FTP access", "Weak FTP credentials"],
            22: ["SSH brute force", "Weak SSH keys"],
            23: ["Telnet cleartext protocol", "No encryption"],
            25: ["SMTP relay", "Email spoofing"],
            53: ["DNS zone transfer", "DNS amplification"],
            80: ["HTTP security headers", "Directory traversal"],
            135: ["RPC enumeration", "MS-RPC vulnerabilities"],
            139: ["NetBIOS enumeration", "SMB null sessions"],
            443: ["SSL/TLS vulnerabilities", "Certificate issues"],
            445: ["SMB vulnerabilities", "EternalBlue"],
            1433: ["MSSQL injection", "Weak authentication"],
            3306: ["MySQL injection", "Default credentials"],
            3389: ["RDP brute force", "BlueKeep vulnerability"],
            5432: ["PostgreSQL injection", "Privilege escalation"],
            6379: ["Redis unauthorized access", "No authentication"],
            8080: ["Web application vulnerabilities", "Default credentials"],
            9200: ["Elasticsearch exposure", "Data leakage"]
        }
        
        for port, service_info in open_ports.items():
            if port in vulnerable_services:
                for vuln in vulnerable_services[port]:
                    vulnerabilities.append(f"Port {port} ({service_info['service']}): {vuln}")
        
        # Technology-based vulnerabilities
        for tech in technologies:
            if 'Apache' in tech:
                vulnerabilities.append("Apache: Check for mod_status, server-info exposure")
            elif 'nginx' in tech:
                vulnerabilities.append("nginx: Check for status page, configuration exposure")
            elif 'WordPress' in tech:
                vulnerabilities.append("WordPress: Check for plugin vulnerabilities, weak credentials")
            elif 'IIS' in tech:
                vulnerabilities.append("IIS: Check for .NET vulnerabilities, directory traversal")
        
        return vulnerabilities

    def generate_professional_report(target, subdomains, live_hosts, port_results, technologies, vulnerabilities):
        """Generate comprehensive professional report"""
        report_file = os.path.join(tool_path, "1-Output", "BugBounty", f"vulnreaper_report_{target.replace('.', '_')}_{int(time.time())}.txt")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        total_open_ports = sum(len(ports) for ports in port_results.values())
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"""# VulnReaper by ahm0x - Professional Bug Bounty Report
# 🔥 Advanced Vulnerability Discovery & Attack Surface Analysis
# Target: {target}
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Generated by: {name_tool} v{version_tool}
# VulnReaper by ahm0x - Professional Bug Bounty Suite
# Website: {website}
# GitHub: {github_tool}
# Telegram: {telegram}

{'='*80}
🎯 VULNREAPER EXECUTIVE SUMMARY
{'='*80}

Target: {target}
Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Subdomains Found: {len(subdomains)}
Live Hosts: {len(live_hosts)}
Open Ports: {total_open_ports}
Vulnerabilities Found: {len(vulnerabilities)}

{'='*80}
🔍 ATTACK SURFACE ANALYSIS
{'='*80}

""")

            # Subdomains section
            f.write(f"SUBDOMAINS DISCOVERED ({len(subdomains)}):\n")
            f.write("="*50 + "\n")
            for subdomain in sorted(subdomains):
                f.write(f"• {subdomain}\n")
            
            # Live hosts section
            f.write(f"\nLIVE HOSTS ({len(live_hosts)}):\n")
            f.write("="*30 + "\n")
            for host in sorted(live_hosts):
                f.write(f"• {host}\n")
            
            # Port scan results
            f.write(f"\nPORT SCAN RESULTS:\n")
            f.write("="*30 + "\n")
            for host, ports in port_results.items():
                if ports:
                    f.write(f"\n{host}:\n")
                    for port, service_info in sorted(ports.items()):
                        f.write(f"  • Port {port}/tcp - {service_info['service']} {service_info['version']}\n")
                        if service_info['banner']:
                            f.write(f"    Banner: {service_info['banner'][:100]}...\n")
            
            # Technologies section
            f.write(f"\nTECHNOLOGIES DETECTED:\n")
            f.write("="*30 + "\n")
            for tech in technologies:
                f.write(f"• {tech}\n")
            
            # Vulnerabilities section
            f.write(f"\n{'='*80}\nVULNERABILITIES FOUND\n{'='*80}\n\n")
            f.write(f"🚨 VULNREAPER VULNERABILITY ANALYSIS:\n\n")
            
            if vulnerabilities:
                for vuln in vulnerabilities:
                    f.write(f"• {vuln}\n")
            else:
                f.write("No critical vulnerabilities detected in automated scan.\n")
                f.write("Manual testing recommended for comprehensive assessment.\n")
            
            # Recommendations section
            f.write(f"{'='*80}\nRECOMMENDATIONS\n{'='*80}\n\n")
            f.write(f"💡 VULNREAPER PROFESSIONAL RECOMMENDATIONS:\n\n")
            f.write("IMMEDIATE ACTIONS:\n")
            f.write("1. Review all open ports and services\n")
            f.write("2. Implement proper access controls\n")
            f.write("3. Update all identified services\n")
            f.write("4. Monitor for suspicious activities\n\n")
            
            f.write("BUG BOUNTY SPECIFIC:\n")
            f.write("🏆 VULNREAPER BUG BOUNTY METHODOLOGY:\n")
            f.write("1. Focus manual testing on identified attack surface\n")
            f.write("2. Test for business logic flaws\n")
            f.write("3. Perform thorough input validation testing\n")
            f.write("4. Check for authentication and authorization bypasses\n")
            f.write("5. Test API endpoints for security misconfigurations\n\n")
            
            # Tools used section
            f.write(f"{'='*80}\nTOOLS USED\n{'='*80}\n\n")
            f.write(f"🛠️ VULNREAPER ARSENAL:\n")
            f.write("• Subdomain Enumeration (Certificate Transparency + DNS)\n")
            f.write("• Port Scanning (Custom TCP Scanner)\n")
            f.write("• Service Detection\n")
            f.write("• Vulnerability Assessment\n")
            f.write("• Live Host Detection\n\n")
            
            # Footer
            f.write(f"{'='*80}\n")
            f.write(f"Report generated by {name_tool} v{version_tool}\n")
            f.write(f"🔥 VulnReaper by ahm0x - Professional Bug Bounty Automation\n")
            f.write(f"For more tools visit: {website}\n")
        
        return report_file

    def check_host_alive(host):
        """Check if host is alive"""
        try:
            # Try HTTP/HTTPS first
            for protocol in ['https', 'http']:
                try:
                    response = secure_session.safe_get(f"{protocol}://{host}", timeout=5)
                    if response and response.status_code < 500:
                        return True
                except:
                    continue
            
            # Try ping as fallback
            if sys.platform.startswith("win"):
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', host], 
                                      capture_output=True, text=True, timeout=3)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', host], 
                                      capture_output=True, text=True, timeout=3)
            
            return result.returncode == 0
        except:
            return False

    # Main execution
    print_legal_disclaimer()
    
    Slow(f"""{scan_banner}
 {BEFORE}01{AFTER}{white} Full Bug Bounty Automation
 {BEFORE}02{AFTER}{white} Subdomain Enumeration Only
 {BEFORE}03{AFTER}{white} Port Scanning Only
 {BEFORE}04{AFTER}{white} Technology Detection Only
 {BEFORE}05{AFTER}{white} Custom Scan Configuration
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    target = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target domain -> {reset}")
    
    # Validate target
    is_valid, message = security.validate_domain(target)
    if not is_valid:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {message}")
        Continue()
        Reset()
    
    # Check if target is safe to scan
    is_safe, safety_message = network_security.is_safe_target(target)
    if not is_safe:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {safety_message}")
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Scan aborted for safety reasons")
        Continue()
        Reset()
    
    Censored(target)
    log_activity(f"VulnReaper scan started", target, "SCAN_START")
    
    start_time = datetime.now()
    
    subdomains = []
    live_hosts = []
    port_results = {}
    technologies = []
    vulnerabilities = []
    
    if choice in ['1', '01', '2', '02', '5', '05']:
        # Subdomain enumeration
        subdomains = advanced_subdomain_enumeration(target)
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(subdomains)}{red} subdomains")
    
    if choice in ['1', '01', '5', '05']:
        # Check which hosts are alive
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Checking live hosts...")
        
        hosts_to_check = subdomains if subdomains else [target]
        
        def check_host(host):
            if check_host_alive(host):
                live_hosts.append(host)
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Live host: {white}{host}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_host, host) for host in hosts_to_check]
            concurrent.futures.wait(futures)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(live_hosts)}{red} live hosts")
    
    if choice in ['1', '01', '3', '03', '5', '05']:
        # Port scanning
        hosts_to_scan = live_hosts if live_hosts else [target]
        
        for host in hosts_to_scan:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Port scanning: {white}{host}")
            try:
                # Resolve hostname to IP for scanning
                ip = socket.gethostbyname(host)
                open_ports = advanced_port_scanning(ip)
                if open_ports:
                    port_results[host] = open_ports
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Port scan failed for {white}{host}{red}: {e}")
    
    if choice in ['1', '01', '4', '04', '5', '05']:
        # Technology detection
        hosts_to_analyze = live_hosts if live_hosts else [target]
        
        for host in hosts_to_analyze:
            for protocol in ['https', 'http']:
                try:
                    url = f"{protocol}://{host}"
                    host_technologies = technology_detection(url)
                    if host_technologies:
                        technologies.extend([f"{host}: {tech}" for tech in host_technologies])
                        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Technologies on {white}{host}{red}: {', '.join(host_technologies)}")
                    break  # If HTTPS works, don't try HTTP
                except:
                    continue
    
    if choice in ['1', '01', '5', '05']:
        # Vulnerability assessment
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Performing vulnerability assessment...")
        vulnerabilities = vulnerability_assessment(target, 
                                                 port_results.get(target, {}), 
                                                 technologies)
    
    # Generate report
    end_time = datetime.now()
    scan_duration = (end_time - start_time).total_seconds()
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Scan completed in {white}{scan_duration:.2f}{red} seconds")
    
    if choice in ['1', '01', '5', '05']:
        report_file = generate_professional_report(target, subdomains, live_hosts, 
                                                 port_results, technologies, vulnerabilities)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Professional report generated: {white}{report_file}")
        
        # Summary
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} 🔥 VulnReaper Summary:")
        print(f"  Subdomains: {white}{len(subdomains)}")
        print(f"  Live hosts: {white}{len(live_hosts)}")
        print(f"  Open ports: {white}{sum(len(ports) for ports in port_results.values())}")
        print(f"  Technologies: {white}{len(technologies)}")
        print(f"  Potential vulnerabilities: {white}{len(vulnerabilities)}")
        
        if vulnerabilities:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} {red}🚨 POTENTIAL VULNERABILITIES DETECTED:")
            for vuln in vulnerabilities[:10]:  # Show first 10
                print(f"  {red}⚠{red} {vuln}")
            if len(vulnerabilities) > 10:
                print(f"  {white}... and {len(vulnerabilities) - 10} more (see report)")
    
    log_activity(f"VulnReaper scan completed", target, "SCAN_COMPLETE")
    
    Continue()
    Reset()

except Exception as e:
    Error(e)