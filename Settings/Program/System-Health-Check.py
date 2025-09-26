#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - System Health Check
Comprehensive system and framework health monitoring
"""

from Config.Util import *
from Config.Config import *
from Config.Security import *
from Config.ErrorHandler import error_handler

try:
    import psutil
    import platform
    import shutil
    import subprocess
    import socket
    import ssl
    from datetime import datetime
    import json
except Exception as e:
    ErrorModule(e)

Title("VulnReaper System Health Check")

try:
    def check_system_resources():
        """Check system resource availability"""
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Checking system resources...")
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_status = "Good" if cpu_percent < 80 else "High" if cpu_percent < 95 else "Critical"
            cpu_color = green if cpu_percent < 80 else yellow if cpu_percent < 95 else red
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} CPU Usage: {cpu_color}{cpu_percent}%{red} ({cpu_status})")
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_status = "Good" if memory_percent < 80 else "High" if memory_percent < 95 else "Critical"
            memory_color = green if memory_percent < 80 else yellow if memory_percent < 95 else red
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Memory Usage: {memory_color}{memory_percent}%{red} ({memory_status})")
            print(f"    Available: {white}{format_file_size(memory.available)}{red} / Total: {white}{format_file_size(memory.total)}")
            
            # Disk usage
            disk = shutil.disk_usage(tool_path)
            disk_free_gb = disk.free / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            disk_percent = ((disk.total - disk.free) / disk.total) * 100
            disk_status = "Good" if disk_percent < 80 else "High" if disk_percent < 95 else "Critical"
            disk_color = green if disk_percent < 80 else yellow if disk_percent < 95 else red
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Disk Usage: {disk_color}{disk_percent:.1f}%{red} ({disk_status})")
            print(f"    Free: {white}{disk_free_gb:.1f}GB{red} / Total: {white}{disk_total_gb:.1f}GB")
            
            # Network interfaces
            network_interfaces = psutil.net_if_addrs()
            active_interfaces = [iface for iface in network_interfaces.keys() if iface != 'lo']
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Network Interfaces: {white}{len(active_interfaces)}{red} active")
            
            return {
                'cpu': {'percent': cpu_percent, 'status': cpu_status},
                'memory': {'percent': memory_percent, 'status': memory_status},
                'disk': {'percent': disk_percent, 'status': disk_status},
                'network': {'interfaces': len(active_interfaces)}
            }
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} System resource check failed: {white}{e}")
            return None

    def check_dependencies():
        """Check all required dependencies"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Checking dependencies...")
        
        required_modules = {
            'requests': 'HTTP requests library',
            'beautifulsoup4': 'HTML parsing',
            'dnspython': 'DNS operations',
            'cryptography': 'Cryptographic operations',
            'colorama': 'Terminal colors',
            'phonenumbers': 'Phone number analysis',
            'python-whois': 'WHOIS lookups',
            'lxml': 'XML/HTML processing',
            'jinja2': 'Template engine',
            'psutil': 'System monitoring',
            'discord.py': 'Discord API',
            'Pillow': 'Image processing'
        }
        
        missing_modules = []
        installed_modules = []
        
        for module, description in required_modules.items():
            try:
                if module == 'beautifulsoup4':
                    import bs4
                elif module == 'python-whois':
                    import whois
                elif module == 'dnspython':
                    import dns.resolver
                elif module == 'discord.py':
                    import discord
                else:
                    __import__(module.replace('-', '_'))
                
                installed_modules.append((module, description))
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {module}: {white}{description}")
                
            except ImportError:
                missing_modules.append((module, description))
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {module}: {white}Missing - {description}")
        
        if missing_modules:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Missing {white}{len(missing_modules)}{red} required modules")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Install with: {white}pip install {' '.join([m[0] for m in missing_modules])}")
            return False
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} All {white}{len(installed_modules)}{red} dependencies are installed")
            return True

    def check_network_connectivity():
        """Check network connectivity and DNS resolution"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Checking network connectivity...")
        
        test_hosts = [
            ('8.8.8.8', 'Google DNS'),
            ('1.1.1.1', 'Cloudflare DNS'),
            ('github.com', 'GitHub'),
            ('google.com', 'Google'),
        ]
        
        connectivity_results = []
        
        for host, description in test_hosts:
            try:
                # Test DNS resolution
                if not host.replace('.', '').isdigit():  # If not IP address
                    socket.gethostbyname(host)
                
                # Test connectivity
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((host, 80))
                sock.close()
                
                if result == 0:
                    connectivity_results.append((host, description, True))
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {description}: {white}Connected")
                else:
                    connectivity_results.append((host, description, False))
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {description}: {white}Failed")
                    
            except Exception as e:
                connectivity_results.append((host, description, False))
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {description}: {white}Failed - {e}")
        
        successful_connections = sum(1 for _, _, success in connectivity_results if success)
        
        if successful_connections == 0:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No network connectivity detected")
            return False
        elif successful_connections < len(test_hosts):
            print(f"{BEFORE + current_time_hour() + AFTER} {yellow}WARNING{red} Limited network connectivity")
            return True
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Network connectivity: {green}Excellent")
            return True

    def check_file_permissions():
        """Check file system permissions"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Checking file permissions...")
        
        test_directories = [
            ("1-Output", "Output directory"),
            ("2-Input", "Input directory"),
            ("Settings/Program", "Program directory")
        ]
        
        permission_issues = []
        
        for directory, description in test_directories:
            dir_path = os.path.join(tool_path, directory)
            
            try:
                # Check if directory exists
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                
                # Test write permission
                test_file = os.path.join(dir_path, "permission_test.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                
                # Test read permission
                with open(test_file, 'r') as f:
                    content = f.read()
                
                # Clean up
                os.remove(test_file)
                
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {description}: {white}Read/Write OK")
                
            except Exception as e:
                permission_issues.append((directory, str(e)))
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {description}: {white}Permission denied - {e}")
        
        return len(permission_issues) == 0

    def check_security_configuration():
        """Check security configuration"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Checking security configuration...")
        
        security_checks = []
        
        # Check if running as admin/root (should warn if yes)
        try:
            if os.geteuid() == 0:  # Unix/Linux
                security_checks.append(("Running as root", "WARNING", "Consider running with limited privileges"))
        except AttributeError:
            # Windows
            try:
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin():
                    security_checks.append(("Running as Administrator", "WARNING", "Consider running with limited privileges"))
            except:
                pass
        
        # Check Python version for security
        python_version = sys.version_info
        if python_version < (3, 9):
            security_checks.append(("Python Version", "WARNING", f"Python {python_version.major}.{python_version.minor} has known security issues"))
        
        # Check SSL/TLS configuration
        try:
            context = ssl.create_default_context()
            if context.check_hostname:
                security_checks.append(("SSL Verification", "OK", "SSL certificate verification enabled"))
            else:
                security_checks.append(("SSL Verification", "WARNING", "SSL certificate verification disabled"))
        except:
            security_checks.append(("SSL Configuration", "ERROR", "SSL configuration check failed"))
        
        # Display security check results
        for check_name, status, message in security_checks:
            if status == "OK":
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {check_name}: {white}{message}")
            elif status == "WARNING":
                print(f"{BEFORE + current_time_hour() + AFTER} {yellow}WARNING{red} {check_name}: {white}{message}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {check_name}: {white}{message}")
        
        return security_checks

    def check_output_directories():
        """Check and create output directories"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Checking output directories...")
        
        required_directories = [
            "1-Output/BugBounty",
            "1-Output/CVEScanner", 
            "1-Output/DirectoryBruteforce",
            "1-Output/DoxCreate",
            "1-Output/ExploitSearch",
            "1-Output/Forensics",
            "1-Output/Logs",
            "1-Output/PhishingAttack",
            "1-Output/PortScan",
            "1-Output/Reports",
            "1-Output/RobloxCookies",
            "1-Output/RobloxGroups",
            "1-Output/ServerTemplates",
            "1-Output/Steganography",
            "1-Output/VirusBuilder",
            "1-Output/WebCrawler",
            "1-Output/WiFiAttack",
            "1-Output/Wordlists",
            "2-Input/DataBase",
            "2-Input/TokenDisc"
        ]
        
        created_directories = 0
        
        for directory in required_directories:
            dir_path = os.path.join(tool_path, directory)
            try:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    created_directories += 1
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Created: {white}{directory}")
                else:
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Exists: {white}{directory}")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to create {white}{directory}{red}: {e}")
        
        if created_directories > 0:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Created {white}{created_directories}{red} missing directories")
        
        return True

    def run_comprehensive_health_check():
        """Run comprehensive system health check"""
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Starting comprehensive health check...")
        
        health_results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': get_system_info(),
            'checks': {}
        }
        
        # System resources
        system_resources = check_system_resources()
        health_results['checks']['system_resources'] = system_resources
        
        # Dependencies
        dependencies_ok = check_dependencies()
        health_results['checks']['dependencies'] = dependencies_ok
        
        # Network connectivity
        network_ok = check_network_connectivity()
        health_results['checks']['network'] = network_ok
        
        # File permissions
        permissions_ok = check_file_permissions()
        health_results['checks']['permissions'] = permissions_ok
        
        # Security configuration
        security_checks = check_security_configuration()
        health_results['checks']['security'] = security_checks
        
        # Output directories
        directories_ok = check_output_directories()
        health_results['checks']['directories'] = directories_ok
        
        # Calculate overall health score
        checks_passed = sum([
            dependencies_ok,
            network_ok,
            permissions_ok,
            directories_ok
        ])
        
        total_checks = 4
        health_score = (checks_passed / total_checks) * 100
        
        # Determine overall status
        if health_score >= 90:
            overall_status = "Excellent"
            status_color = green
        elif health_score >= 75:
            overall_status = "Good"
            status_color = green
        elif health_score >= 50:
            overall_status = "Fair"
            status_color = yellow
        else:
            overall_status = "Poor"
            status_color = red
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Health Check Summary:")
        print(f"    Overall Status: {status_color}{overall_status}{red} ({health_score:.1f}%)")
        print(f"    Checks Passed: {white}{checks_passed}/{total_checks}")
        
        # Save health check report
        report_file = os.path.join(tool_path, "1-Output", "Reports", f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(health_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Health report saved: {white}{report_file}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to save health report: {white}{e}")
        
        return health_results

    def fix_common_issues():
        """Attempt to fix common issues automatically"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Attempting to fix common issues...")
        
        fixes_applied = 0
        
        # Create missing directories
        try:
            check_output_directories()
            fixes_applied += 1
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Directory structure verified/created")
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to create directories")
        
        # Clean up temporary files
        try:
            temp_patterns = ['*.tmp', '*.temp', '*~', '.DS_Store', 'Thumbs.db']
            cleaned_files = 0
            
            for root, dirs, files in os.walk(tool_path):
                for file in files:
                    if any(file.endswith(pattern.replace('*', '')) for pattern in temp_patterns):
                        try:
                            os.remove(os.path.join(root, file))
                            cleaned_files += 1
                        except:
                            pass
            
            if cleaned_files > 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Cleaned {white}{cleaned_files}{red} temporary files")
                fixes_applied += 1
        except:
            pass
        
        # Update pip if needed
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Checking pip version...")
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} pip is available")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} pip is not available")
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to check pip")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Applied {white}{fixes_applied}{red} fixes")
        return fixes_applied > 0

    def display_system_information():
        """Display detailed system information"""
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} System Information:")
        
        system_info = get_system_info()
        
        print(f"    Platform: {white}{system_info['platform']} {system_info['platform_version']}")
        print(f"    Architecture: {white}{system_info['architecture']}")
        print(f"    Processor: {white}{system_info['processor']}")
        print(f"    Python Version: {white}{system_info['python_version']}")
        print(f"    Hostname: {white}{system_info['hostname']}")
        
        # Additional system info
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            print(f"    System Uptime: {white}{uptime.days} days, {uptime.seconds//3600} hours")
            
            cpu_count = psutil.cpu_count()
            print(f"    CPU Cores: {white}{cpu_count}")
            
            memory = psutil.virtual_memory()
            print(f"    Total Memory: {white}{format_file_size(memory.total)}")
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Extended system info failed: {white}{e}")

    # Main health check execution
    Slow(f"""{scan_banner}
 {BEFORE}01{AFTER}{white} Quick health check
 {BEFORE}02{AFTER}{white} Comprehensive health check
 {BEFORE}03{AFTER}{white} Fix common issues
 {BEFORE}04{AFTER}{white} System information
 {BEFORE}05{AFTER}{white} Error statistics
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Health check type -> {reset}")
    
    if choice in ['1', '01']:
        # Quick health check
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Running quick health check...")
        
        dependencies_ok = error_handler.validate_dependencies()
        system_ok = error_handler.check_system_requirements()
        
        if dependencies_ok and system_ok:
            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} System health: {white}Good")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} System health: {white}Issues detected")
    
    elif choice in ['2', '02']:
        # Comprehensive health check
        health_results = run_comprehensive_health_check()
    
    elif choice in ['3', '03']:
        # Fix common issues
        fixes_applied = fix_common_issues()
        if fixes_applied:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Issues fixed. Restart recommended.")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No issues found to fix")
    
    elif choice in ['4', '04']:
        # System information
        display_system_information()
    
    elif choice in ['5', '05']:
        # Error statistics
        stats = error_handler.get_error_statistics()
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Error Statistics:")
        print(f"    Total Errors: {white}{stats['total_errors']}")
        print(f"    Total Warnings: {white}{stats['total_warnings']}")
        print(f"    Log File: {white}{stats['log_file']}")
    
    else:
        ErrorChoice()

    Continue()
    Reset()

except Exception as e:
    Error(e)