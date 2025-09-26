#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - Utility Functions
Professional Cybersecurity Framework Utilities
"""

import os
import sys
import time
import subprocess
import platform
import requests
import json
from datetime import datetime
import re

# Color definitions
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Initialize colors
red = Colors.RED
green = Colors.GREEN
yellow = Colors.YELLOW
blue = Colors.BLUE
magenta = Colors.MAGENTA
cyan = Colors.CYAN
white = Colors.WHITE
reset = Colors.RESET

# Time formatting
BEFORE = f"{red}[{white}"
AFTER = f"{red}]"
BEFORE_GREEN = f"{green}[{white}"
AFTER_GREEN = f"{green}]"

# Status indicators
INFO = f"{blue}INFO{red}"
ERROR = f"{red}ERROR{red}"
WAIT = f"{yellow}WAIT{red}"
ADD = f"{green}ADD{red}"
INPUT = f"{cyan}INPUT{red}"
GEN_VALID = f"{green}VALID{red}"
GEN_INVALID = f"{red}INVALID{red}"
INFO_ADD = f"{red}[{green}+{red}]"

def current_time_hour():
    """Get current time in HH:MM:SS format"""
    return datetime.now().strftime("%H:%M:%S")

def current_time_day_hour():
    """Get current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def Clear():
    """Clear the terminal screen"""
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

def Title(title):
    """Set terminal title"""
    if sys.platform.startswith("win"):
        os.system(f"title {title}")
    else:
        print(f"\033]0;{title}\007", end="")

def Slow(text, delay=0.03):
    """Print text with typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def Continue():
    """Wait for user input to continue"""
    input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Press Enter to continue...{reset}")

def Reset():
    """Reset to main menu"""
    try:
        from Main import main
        main()
    except ImportError:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Cannot return to main menu")
        sys.exit(1)

def StartProgram(program_name):
    """Start a program module"""
    try:
        program_path = os.path.join(os.path.dirname(__file__), "..", program_name)
        if os.path.exists(program_path):
            exec(open(program_path).read())
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Program not found: {white}{program_name}")
            Continue()
            Reset()
    except Exception as e:
        Error(e)

def Error(error):
    """Handle and display errors"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} An error occurred: {white}{error}")
    Continue()
    Reset()

def ErrorModule(module):
    """Handle module import errors"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Module not found: {white}{module}")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Run 'pip install -r requirements.txt' to install dependencies")
    Continue()
    Reset()

def ErrorChoice():
    """Handle invalid choice errors"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid choice")
    time.sleep(1)

def ErrorChoiceStart():
    """Handle invalid choice and restart"""
    ErrorChoice()

def ErrorNumber():
    """Handle invalid number input"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid number format")
    Continue()
    Reset()

def ErrorId():
    """Handle invalid ID input"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid ID format")
    Continue()
    Reset()

def ErrorToken():
    """Handle invalid token"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid or expired token")
    Continue()
    Reset()

def ErrorUrl():
    """Handle invalid URL"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid URL or website not accessible")
    Continue()
    Reset()

def ErrorUsername():
    """Handle invalid username"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid username or user not found")
    Continue()
    Reset()

def ErrorWebhook():
    """Handle invalid webhook"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid webhook URL")
    Continue()
    Reset()

def OnlyWindows():
    """Show Windows-only feature message"""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} This feature is only available on Windows")
    Continue()
    Reset()

def Censored(data):
    """Log censored data for security"""
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Target: {white}[CENSORED]{red}")

def CheckWebhook(webhook_url):
    """Validate webhook URL"""
    try:
        response = requests.get(webhook_url, timeout=5)
        if response.status_code == 200:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Webhook validated successfully")
        else:
            ErrorWebhook()
    except:
        ErrorWebhook()

def Choice1TokenDiscord():
    """Get single Discord token"""
    token_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "2-Input", "TokenDisc", "TokenDisc.txt")
    
    try:
        with open(token_file, 'r') as f:
            tokens = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not tokens:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No tokens found in TokenDisc.txt")
            Continue()
            Reset()
        
        if len(tokens) == 1:
            return tokens[0]
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(tokens)}{red} tokens")
            for i, token in enumerate(tokens, 1):
                print(f" {BEFORE}{i:02d}{AFTER}{white} {token[:20]}...")
            
            try:
                choice = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Select token -> {reset}"))
                if 1 <= choice <= len(tokens):
                    return tokens[choice - 1]
                else:
                    ErrorChoice()
            except:
                ErrorNumber()
    except FileNotFoundError:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Token file not found: {white}{token_file}")
        Continue()
        Reset()

def ChoiceMultiTokenDisord():
    """Get multiple Discord tokens"""
    token_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "2-Input", "TokenDisc", "TokenDisc.txt")
    
    try:
        with open(token_file, 'r') as f:
            tokens = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not tokens:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No tokens found in TokenDisc.txt")
            Continue()
            Reset()
        
        return tokens
    except FileNotFoundError:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Token file not found: {white}{token_file}")
        Continue()
        Reset()

def ChoiceMultiChannelDiscord():
    """Get multiple Discord channels"""
    channels_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Channel IDs (comma separated) -> {reset}")
    channels = [ch.strip() for ch in channels_input.split(',') if ch.strip()]
    
    if not channels:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No channels provided")
        Continue()
        Reset()
    
    return channels

def MainColor(text):
    """Apply main color formatting"""
    return f"{red}{text}{reset}"

def MainColor2(text):
    """Apply secondary color formatting"""
    return f"{white}{text}{reset}"

# Banner definitions
scan_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🔍 ADVANCED SCANNING MODULE 🔍{red}                           ║
║                                                                                      ║
║                    {yellow}Professional Vulnerability Discovery{red}                     ║
║                              {yellow}Real-time Analysis{red}                              ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

discord_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}📱 DISCORD SECURITY SUITE 📱{red}                           ║
║                                                                                      ║
║                    {yellow}Advanced Discord Analysis Tools{red}                         ║
║                              {yellow}Token & Server Security{red}                        ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

osint_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🔍 OSINT FRAMEWORK 🔍{red}                                 ║
║                                                                                      ║
║                    {yellow}Open Source Intelligence Gathering{red}                     ║
║                              {yellow}Professional OSINT Tools{red}                       ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

sql_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}💉 SQL INJECTION SCANNER 💉{red}                          ║
║                                                                                      ║
║                    {yellow}Advanced SQL Vulnerability Detection{red}                   ║
║                              {yellow}Professional Web Security{red}                      ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

phishing_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🎣 PHISHING ANALYSIS TOOL 🎣{red}                          ║
║                                                                                      ║
║                    {yellow}Website Cloning & Analysis{red}                             ║
║                              {yellow}Educational Purposes Only{red}                      ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

virus_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🦠 MALWARE ANALYSIS TOOLS 🦠{red}                          ║
║                                                                                      ║
║                    {yellow}Educational Security Research{red}                           ║
║                              {yellow}Ethical Use Only{red}                               ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

wifi_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}📶 WIRELESS SECURITY TOOLS 📶{red}                        ║
║                                                                                      ║
║                    {yellow}WiFi Network Analysis{red}                                  ║
║                              {yellow}Network Security Assessment{red}                    ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

map_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🗺️ GEOLOCATION ANALYSIS 🗺️{red}                           ║
║                                                                                      ║
║                    {yellow}IP & Location Intelligence{red}                             ║
║                              {yellow}Geographic Information{red}                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

dox_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}📋 INFORMATION GATHERING 📋{red}                          ║
║                                                                                      ║
║                    {yellow}Professional OSINT Research{red}                            ║
║                              {yellow}Educational Purposes Only{red}                      ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

tor_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🧅 DARK WEB RESEARCH 🧅{red}                              ║
║                                                                                      ║
║                    {yellow}Educational Research Links{red}                             ║
║                              {yellow}Security Research Only{red}                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

encrypted_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🔐 ENCRYPTION TOOLS 🔐{red}                               ║
║                                                                                      ║
║                    {yellow}Cryptographic Operations{red}                               ║
║                              {yellow}Security Research{red}                              ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

decrypted_banner = f"""{red}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                        {white}🔓 DECRYPTION TOOLS 🔓{red}                               ║
║                                                                                      ║
║                    {yellow}Hash Cracking & Analysis{red}                               ║
║                              {yellow}Educational Purposes{red}                           ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
"""

def validate_input(input_value, input_type="string", min_length=1, max_length=None):
    """Validate user input"""
    if input_type == "string":
        if len(input_value.strip()) < min_length:
            return False, f"Input too short (minimum {min_length} characters)"
        if max_length and len(input_value) > max_length:
            return False, f"Input too long (maximum {max_length} characters)"
        return True, "Valid"
    
    elif input_type == "number":
        try:
            num = int(input_value)
            if min_length and num < min_length:
                return False, f"Number too small (minimum {min_length})"
            if max_length and num > max_length:
                return False, f"Number too large (maximum {max_length})"
            return True, "Valid"
        except ValueError:
            return False, "Invalid number format"
    
    elif input_type == "url":
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if url_pattern.match(input_value):
            return True, "Valid"
        else:
            return False, "Invalid URL format"
    
    elif input_type == "email":
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if email_pattern.match(input_value):
            return True, "Valid"
        else:
            return False, "Invalid email format"
    
    return True, "Valid"

def safe_request(url, method="GET", **kwargs):
    """Make safe HTTP requests with error handling"""
    try:
        kwargs.setdefault('timeout', 10)
        kwargs.setdefault('headers', {
            'User-Agent': 'VulnReaper-Security-Scanner/1.0 (Educational-Research)'
        })
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        else:
            return None
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Request failed: {white}{e}")
        return None

def create_output_directory(subdirectory):
    """Create output directory if it doesn't exist"""
    output_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "1-Output", subdirectory)
    os.makedirs(output_path, exist_ok=True)
    return output_path

def log_activity(activity, target="", status="INFO"):
    """Log activity to file"""
    try:
        log_dir = create_output_directory("Logs")
        log_file = os.path.join(log_dir, f"activity_{datetime.now().strftime('%Y%m%d')}.log")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = current_time_day_hour()
            f.write(f"[{timestamp}] [{status}] {activity}")
            if target:
                f.write(f" - Target: [CENSORED]")
            f.write("\n")
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Logging failed: {white}{e}")

def check_internet_connection():
    """Check if internet connection is available"""
    try:
        response = requests.get("https://8.8.8.8", timeout=5)
        return True
    except:
        try:
            response = requests.get("https://1.1.1.1", timeout=5)
            return True
        except:
            return False

def get_system_info():
    """Get system information"""
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'python_version': sys.version.split()[0],
        'hostname': platform.node()
    }

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def is_valid_ip(ip):
    """Validate IP address format"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False

def is_private_ip(ip):
    """Check if IP is private"""
    try:
        parts = [int(x) for x in ip.split('.')]
        return (
            parts[0] == 10 or
            (parts[0] == 172 and 16 <= parts[1] <= 31) or
            (parts[0] == 192 and parts[1] == 168)
        )
    except:
        return False

def generate_report_header(tool_name, target="", scan_type=""):
    """Generate standard report header"""
    return f"""# {tool_name} Report
# Generated by: VulnReaper by ahm0x v1.0
# Website: https://ahm0x.github.io/
# GitHub: https://github.com/ahm0x/VulnReaper
# Date: {current_time_day_hour()}
# Target: [CENSORED]
# Scan Type: {scan_type}
# 
# ⚠️  DISCLAIMER: This tool is for educational and authorized testing only
# ⚠️  Unauthorized use is strictly prohibited and may be illegal
#
{'='*80}
"""

def print_legal_disclaimer():
    """Print legal disclaimer"""
    print(f"""
{yellow}╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                              {red}⚠️  LEGAL DISCLAIMER ⚠️{yellow}                              ║
║                                                                                      ║
║  This tool is for educational and authorized security testing purposes only.        ║
║  Unauthorized access to computer systems is illegal and punishable by law.          ║
║  Users are responsible for complying with all applicable laws and regulations.      ║
║  The author assumes no liability for misuse of this software.                       ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{reset}
""")

# Initialize logging
def init_logging():
    """Initialize logging system"""
    try:
        log_dir = create_output_directory("Logs")
        log_activity("VulnReaper Framework Started", status="INIT")
    except:
        pass

# Auto-initialize when module is imported
init_logging()