from .Config import *
try:
    import colorama
    import ctypes
    import subprocess
    import os
    import time
    import sys
    import datetime
    import requests
    import logging
    import json
    import hashlib
    import platform
    
    # Initialize colorama for cross-platform colored output
    colorama.init()
except Exception as e:
    print(f"[x] | Error Module (Restart Setup.bat): {e}")
    if sys.platform.startswith("win"):
        os.system("pause")
    else:
        input("Press Enter to continue...")

# Setup logging
def setup_logging():
    """Setup logging configuration"""
    log_dir = os.path.join(tool_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"vulnreaper_{datetime.datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

# Color definitions
color = colorama.Fore
red = color.RED
white = color.WHITE
green = color.GREEN
reset = color.RESET
blue = color.BLUE
yellow = color.YELLOW
magenta = color.MAGENTA
cyan = color.CYAN

# Get username safely
try: 
    username_pc = os.getlogin()
except: 
    username_pc = os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))

def current_time_day_hour():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def current_time_hour():
    return datetime.datetime.now().strftime('%H:%M:%S')

def get_system_info():
    """Get comprehensive system information"""
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'hostname': platform.node(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'username': username_pc
    }

def validate_input(input_value, input_type="string", min_length=1, max_length=None):
    """Validate user input with proper sanitization"""
    if not input_value or not input_value.strip():
        return False, "Input cannot be empty"
    
    input_value = input_value.strip()
    
    if len(input_value) < min_length:
        return False, f"Input must be at least {min_length} characters"
    
    if max_length and len(input_value) > max_length:
        return False, f"Input must be less than {max_length} characters"
    
    if input_type == "url":
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(input_value):
            return False, "Invalid URL format"
    
    elif input_type == "ip":
        import ipaddress
        try:
            ipaddress.ip_address(input_value)
        except ValueError:
            return False, "Invalid IP address format"
    
    elif input_type == "email":
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(input_value):
            return False, "Invalid email format"
    
    return True, input_value

def safe_request(url, method='GET', headers=None, data=None, timeout=10, verify=True):
    """Make safe HTTP requests with proper error handling"""
    try:
        default_headers = {
            'User-Agent': 'VulnReaper/1.0 (Professional Security Scanner)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        if headers:
            default_headers.update(headers)
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=default_headers, timeout=timeout, verify=verify)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=default_headers, data=data, timeout=timeout, verify=verify)
        else:
            response = requests.request(method, url, headers=default_headers, data=data, timeout=timeout, verify=verify)
        
        logger.info(f"HTTP {method} {url} - Status: {response.status_code}")
        return response
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error for {url}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for {url}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for {url}: {e}")
        return None

BEFORE = f'{blue}[{white}'
AFTER = f'{blue}]'

BEFORE_GREEN = f'{green}[{white}'
AFTER_GREEN = f'{green}]'

INPUT = f'{BEFORE}>{AFTER} |'
INFO = f'{BEFORE}!{AFTER} |'
ERROR = f'{BEFORE}x{AFTER} |'
ADD = f'{BEFORE}+{AFTER} |'
WAIT = f'{BEFORE}~{AFTER} |'

GEN_VALID = f'{BEFORE_GREEN}+{AFTER_GREEN} |'
GEN_INVALID = f'{BEFORE}x{AFTER} |'

INFO_ADD = f'{white}[{blue}+{white}]{blue}'

def Censored(text):
    """Enhanced input validation and censoring"""
    if not text or not isinstance(text, str):
        print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid input provided.')
        Continue()
        Reset()
        return
    
    # Sanitize input
    text = text.strip()
    
    # Check for potentially malicious patterns
    malicious_patterns = [
        r'<script.*?>.*?</script>',  # XSS
        r'javascript:',  # JavaScript injection
        r'data:.*base64',  # Data URI
        r'file://',  # File protocol
        r'\.\./.*\.\.',  # Path traversal
        r'[;&|`$]',  # Command injection
    ]
    
    import re
    for pattern in malicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} Potentially malicious input detected.')
            Continue()
            Reset()
            return
    
    # Original censored content check
    censored = ["loxy", "BashMagno", website, creator]
    for censored_text in censored:
        if text in censored:
            print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} Unable to find "{white}{text}{red}".')
            Continue()
            Reset()
            return
        elif censored_text in text:
            print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} Unable to find "{white}{text}{red}".')
            Continue()
            Reset()
            return
    
    logger.info(f"Input validated: {text[:50]}{'...' if len(text) > 50 else ''}")

def Title(title):
    """Set console title with enhanced cross-platform support"""
    try:
        safe_title = f"{name_tool} {version_tool} | {title}"
        logger.info(f"Setting title: {safe_title}")
        
    if sys.platform.startswith("win"):
            ctypes.windll.kernel32.SetConsoleTitleW(safe_title)
    elif sys.platform.startswith("linux"):
            sys.stdout.write(f"\x1b]2;{safe_title}\x07")
            sys.stdout.flush()
    except Exception as e:
        logger.error(f"Error setting title: {e}")
        
def Clear():
    """Clear console with enhanced cross-platform support"""
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

def Reset():
    """Reset application with proper error handling"""
    try:
        logger.info("Resetting application")
    if sys.platform.startswith("win"):
        file = ['python', os.path.join(tool_path, "Main.py")]
        else:
        file = ['python3', os.path.join(tool_path, "Main.py")]
        
        subprocess.run(file, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error resetting application: {e}")
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error restarting application")
    except FileNotFoundError:
        logger.error("Python interpreter not found")
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Python interpreter not found")

def StartProgram(program):
    """Start program with enhanced error handling and validation"""
    try:
        program_path = os.path.join(tool_path, "Settings", "Program", program)
        
        if not os.path.exists(program_path):
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Program not found: {white}{program}")
            Continue()
            Reset()
            return
        
        logger.info(f"Starting program: {program}")
        
    if sys.platform.startswith("win"):
        file = ['python', os.path.join(tool_path, "Settings", "Program", program)]
        else:
        file = ['python3', os.path.join(tool_path, "Settings", "Program", program)]
        
        subprocess.run(file, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting program {program}: {e}")
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error starting program: {white}{program}")
        Continue()
        Reset()
    except Exception as e:
        Error(e)

def Slow(texte):
    delai = 0.03
    lignes = texte.split('\n')
    for ligne in lignes:
        print(ligne)
        time.sleep(delai)

def Continue():
    input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)

def Error(e):
    """Enhanced error handling with logging"""
    error_msg = str(e)
    logger.error(f"Application error: {error_msg}")
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error: {white}{e}", reset)
    
    # Save error to file for debugging
    try:
        error_file = os.path.join(tool_path, "logs", "errors.log")
        os.makedirs(os.path.dirname(error_file), exist_ok=True)
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(f"{current_time_day_hour()} - {error_msg}\n")
    except:
        pass
    
    Continue()
    Reset()

def create_output_directories():
    """Create all necessary output directories"""
    output_dirs = [
        "1-Output/BugBounty",
        "1-Output/CVEScanner", 
        "1-Output/DirectoryBruteforce",
        "1-Output/DoxCreate",
        "1-Output/ExploitSearch",
        "1-Output/Forensics",
        "1-Output/NetworkScan",
        "1-Output/OSINT",
        "1-Output/PhishingAttack",
        "1-Output/PortScan",
        "1-Output/RobloxCookies",
        "1-Output/RobloxGroups",
        "1-Output/ServerTemplates",
        "1-Output/SQLInjection",
        "1-Output/Steganography",
        "1-Output/SubdomainEnum",
        "1-Output/WebCrawler",
        "1-Output/WiFiAttack",
        "1-Output/Wordlists",
        "logs"
    ]
    
    for directory in output_dirs:
        dir_path = os.path.join(tool_path, directory)
        os.makedirs(dir_path, exist_ok=True)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        'requests', 'colorama', 'beautifulsoup4', 'dnspython', 
        'phonenumbers', 'cryptography', 'psutil', 'Pillow'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Missing dependencies: {white}{', '.join(missing_modules)}")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Run: {white}pip install -r requirements.txt")
        return False
    
    return True

def generate_session_id():
    """Generate unique session ID for tracking"""
    import uuid
    return str(uuid.uuid4())[:8]

def save_scan_metadata(scan_type, target, results_count, session_id):
    """Save scan metadata for tracking and reporting"""
    try:
        metadata_file = os.path.join(tool_path, "logs", "scan_history.json")
        
        metadata = {
            'timestamp': current_time_day_hour(),
            'session_id': session_id,
            'scan_type': scan_type,
            'target': target,
            'results_count': results_count,
            'user': username_pc,
            'system': get_system_info()
        }
        
        # Load existing metadata
        existing_data = []
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                existing_data = []
        
        existing_data.append(metadata)
        
        # Keep only last 1000 entries
        if len(existing_data) > 1000:
            existing_data = existing_data[-1000:]
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Scan metadata saved: {scan_type} on {target}")
    except Exception as e:
        logger.error(f"Error saving scan metadata: {e}")
def ErrorChoiceStart():
    print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Choice !", reset)
    time.sleep(1)

def ErrorChoice():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Choice !", reset)
    logger.warning("Invalid choice made by user")
    time.sleep(3)
    Reset()

def ErrorId():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid ID !", reset)
    logger.warning("Invalid ID provided by user")
    time.sleep(3)
    Reset()

def ErrorUrl():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid URL !", reset)
    logger.warning("Invalid URL provided by user")
    time.sleep(3)
    Reset()

def ErrorResponse():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Response !", reset)
    logger.warning("Invalid response received")
    time.sleep(3)
    Reset()

def ErrorEdge():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Edge not installed or driver not up to date !", reset)
    logger.error("Edge browser or driver issue")
    time.sleep(3)
    Reset()

def ErrorToken():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Token !", reset)
    logger.warning("Invalid token provided")
    time.sleep(3)
    Reset()
    
def ErrorNumber():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Number !", reset)
    logger.warning("Invalid number provided")
    time.sleep(3)
    Reset()

def ErrorWebhook():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Webhook !", reset)
    logger.warning("Invalid webhook provided")
    time.sleep(3)
    Reset()

def ErrorCookie():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Cookie !", reset)
    logger.warning("Invalid cookie provided")
    time.sleep(3)
    Reset()

def ErrorUsername():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Username !", reset)
    logger.warning("Invalid username provided")
    time.sleep(3)
    Reset()

def ErrorModule(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error Module (Restart Setup.bat): {white}{e}", reset)
    logger.error(f"Module error: {e}")
    Continue()
    Reset()

def OnlyWindows():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} This function is only available on Windows 10/11 !", reset)
    logger.warning("Windows-only function called on non-Windows system")
    Continue()
    Reset()

def OnlyLinux():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} This function is only available on Linux !", reset)
    logger.warning("Linux-only function called on non-Linux system")
    Continue()
    Reset()

def check_admin_privileges():
    """Check if running with administrator/root privileges"""
    try:
        if sys.platform.startswith("win"):
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def require_admin():
    """Require administrator privileges for certain operations"""
    if not check_admin_privileges():
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Administrator privileges required for this operation")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Please run as administrator/root")
        Continue()
        Reset()
        return False
    return True

def MainColor(text):
    start_color = (168, 5, 5)  
    end_color = (255, 118, 118)

    num_steps = 9

    colors = []
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))  
    
    gradient_chars = '┴┼┘┤└┐─┬├┌└│]░▒░▒█▓▄▌▀()'
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
       
    lines = text.split('\n')
    num_colors = len(colors)
    
    result = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in gradient_chars:
                color_index = (i + j) % num_colors
                color = colors[color_index]
                result.append(text_color(*color) + char + "\033[0m")
            else:
                result.append(char)
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)

def MainColor2(text):
    start_color = (168, 5, 5)  
    end_color = (255, 118, 118)

    num_steps = 9

    colors = []
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))  
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
       
    lines = text.split('\n')
    num_colors = len(colors)
    
    result = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            color_index = (i + j) % num_colors
            color = colors[color_index]
            result.append(text_color(*color) + char + "\033[0m")
        
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)

def CheckWebhook(webhook):
    """Enhanced webhook validation"""
    if not webhook or not isinstance(webhook, str):
        ErrorWebhook()
        return
    
    webhook = webhook.strip()
    
    # Validate webhook URL format
    valid_prefixes = [
        "https://discord.com/api/webhooks",
        "http://discord.com/api/webhooks",
        "https://canary.discord.com/api/webhooks",
        "http://canary.discord.com/api/webhooks",
        "https://discordapp.com/api/webhooks",
        "http://discordapp.com/api/webhooks"
    ]
    
    is_valid = any(webhook.lower().startswith(prefix) for prefix in valid_prefixes)
    
    if not is_valid:
        ErrorWebhook()
        return
    
    # Test webhook connectivity
    try:
        response = requests.head(webhook, timeout=5)
        if response.status_code not in [200, 204]:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Webhook test failed: HTTP {response.status_code}")
            ErrorWebhook()
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Webhook connectivity test failed: {white}{e}")
        ErrorWebhook()

def ChoiceMultiChannelDiscord():
    """Enhanced multi-channel selection with validation"""
    try:
        num_channels = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} How many spam channels -> {reset}"))
        if num_channels <= 0 or num_channels > 50:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid number of channels (1-50)")
            ErrorNumber()
    except:
        ErrorNumber()
    
    selected_channels = [] 
    number = 0
    for _ in range(num_channels):
        try:
            number += 1
            selected_channel_number = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Channel Id {number}/{num_channels} -> {reset}")
            
            # Validate channel ID format (Discord channel IDs are 17-19 digits)
            if not selected_channel_number.isdigit() or len(selected_channel_number) < 17:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid channel ID format")
                ErrorId()
            
            selected_channels.append(selected_channel_number)
        except:
            ErrorId()

    return selected_channels


def ChoiceMultiTokenDisord():
    """Enhanced multi-token selection with improved validation"""

    def CheckToken(token_number, token):
        try:
            response = safe_request('https://discord.com/api/v9/users/@me', 
                                  headers={'Authorization': token, 'Content-Type': 'application/json'}, 
                                  timeout=5)
        
            if response and response.status_code == 200:
                user_data = response.json()
                username_discord = user_data.get('username', 'Unknown')
                discriminator = user_data.get('discriminator', '0000')
                token_censored = token[:20] + '...' + token[-5:] if len(token) > 25 else token[:10] + '...'
                print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Valid{red} | User: {white}{username_discord}#{discriminator}{red} | Token: {white}{token_censored}")
                return True
            else:
                print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Invalid{red} | Token: {white}{token[:20]}...")
                return False
        except Exception as e:
            print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Error{red} | Error: {white}{e}")
            return False

    file_token_discord_relative = "\\2-Input\\TokenDisc\\TokenDisc.txt"
    file_token_discord = os.path.join(tool_path, "2-Input", "TokenDisc", "TokenDisc.txt")
    
    # Ensure token file exists
    os.makedirs(os.path.dirname(file_token_discord), exist_ok=True)
    if not os.path.exists(file_token_discord):
        with open(file_token_discord, 'w', encoding='utf-8') as f:
            f.write("# Discord Tokens\n# Add your Discord tokens here, one per line\n\n")
    
    tokens = {}
    token_discord_number = 0

    with open(file_token_discord, 'r') as file_token:
        for line in file_token:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            token_discord_number += 1
        
        if token_discord_number == 0:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No Token Discord in file: {white}{file_token_discord_relative}{red} Please add tokens to the file.")
            Continue()
            Reset()
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {white}{token_discord_number}{red} Token Discord found ({white}{file_token_discord_relative}{red})")
    
    try:
        num_tokens = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} How many token (max {token_discord_number}) -> {reset}"))
        if num_tokens <= 0 or num_tokens > token_discord_number:
            ErrorNumber()
    except:
        ErrorNumber()

    token_discord_number = 0
    valid_tokens = {}
    with open(file_token_discord, 'r') as file_token:
        print()
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Token Discord ({white}{file_token_discord}{red}):\n")
        for line in file_token:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            token_discord_number += 1
            if CheckToken(token_discord_number, line):
                valid_tokens[token_discord_number] = line
            tokens[token_discord_number] = line

    number = 0
    selected_tokens = []
    print()
    for _ in range(num_tokens):
        try:
            number += 1
            selected_token_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token Number {number}/{num_tokens} -> {reset}"))
            
            if selected_token_number not in tokens:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Token number {selected_token_number} not found")
                ErrorNumber()
        except:
            ErrorNumber()
        
        selected_token = tokens.get(selected_token_number)
        if selected_token:
            # Verify token is still valid before adding
            if selected_token_number in valid_tokens:
                selected_tokens.append(selected_token)
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Selected token is invalid")
                ErrorToken()
        else:
            ErrorNumber()
    return selected_tokens


def Choice1TokenDiscord():
    """Enhanced single token selection with improved validation"""
    def CheckToken(token_number, token):
        try:
            response = safe_request('https://discord.com/api/v9/users/@me', 
                                  headers={'Authorization': token, 'Content-Type': 'application/json'}, 
                                  timeout=5)
        
            if response and response.status_code == 200:
                user_data = response.json()
                username_discord = user_data.get('username', 'Unknown')
                discriminator = user_data.get('discriminator', '0000')
                token_censored = token[:20] + '...' + token[-5:] if len(token) > 25 else token[:10] + '...'
                print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Valid{red} | User: {white}{username_discord}#{discriminator}{red} | Token: {white}{token_censored}")
                return True
            else:
                print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Invalid{red} | Token: {white}{token[:20]}...")
                return False
        except Exception as e:
            print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Error{red} | Error: {white}{e}")
            return False

    file_token_discord_relative = "\\2-Input\\TokenDisc\\TokenDisc.txt"
    file_token_discord = os.path.join(tool_path, "2-Input", "TokenDisc", "TokenDisc.txt")

    # Ensure token file exists
    os.makedirs(os.path.dirname(file_token_discord), exist_ok=True)
    if not os.path.exists(file_token_discord):
        with open(file_token_discord, 'w', encoding='utf-8') as f:
            f.write("# Discord Tokens\n# Add your Discord tokens here, one per line\n\n")

    tokens = {}
    token_discord_number = 0

    with open(file_token_discord, 'r') as file_token:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Token Discord ({white}{file_token_discord_relative}{red}):\n")
        for line in file_token:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
    
            token_discord_number += 1
            tokens[token_discord_number] = line
            CheckToken(token_discord_number, line)

    if not tokens:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No Token Discord in file: {white}{file_token_discord_relative}{red} Please add tokens to the file.")
        Continue()
        Reset()
        return None

    try:
        selected_token_number = int(input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Token Number -> {reset}"))
        if selected_token_number not in tokens:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Token number not found")
            ErrorChoice()
    except:
        ErrorChoice()

    selected_token = tokens.get(selected_token_number)
    if selected_token:
        # Verify token one more time before returning
        response = safe_request('https://discord.com/api/v9/users/@me', 
                              headers={'Authorization': selected_token, 'Content-Type': 'application/json'}, 
                              timeout=5)
        if response and response.status_code == 200:
            logger.info(f"Valid Discord token selected: {selected_token[:20]}...")
            return selected_token
        else:
            ErrorToken()
    else:
        ErrorChoice()

# Initialize output directories on import
try:
    create_output_directories()
except Exception as e:
    logger.error(f"Error creating output directories: {e}")
tor_banner = MainColor2(r"""
                                                                       ..                                   
                                                                     .:@ :...                               
                .:::::::::::::::::::::::::::::::::.             ....-@@@+..                                 
               .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.           .-@@@@@-.                                    
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.          .=@@@@-.                                      
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.          -@@@@-.                                       
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.      @@ :@@#:.                                         
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.       %  @%+:                                          
                ::::::::-*@@@@@@@@@@@@@@@*-::::::::        @@ #:@@@                           ..::::::::    
                         -@@@@@@@@@@@@@@@=                 @@ @+@@@@                      .::+@@@@@@@@@@:   
                         -@@@@@@@@@@@@@@@                @@@  @+@%%@@                    -*@@@@@@@@@@@@@:   
                         :@@@@@@@@@@@@@@@            @@@@    @@+.@@=:@@@@              :*@@@@@@@@@@@@@@@:   
                         :@@@@@@@@@@@@@@@          @@@    ..@:@@+ @@%=-:=@@@          :*@@@@@@@@@@@@@@@@:   
                         :@@@@@@@@@@@@@@@       @@@    .-@@@::@#@# @@#@%*-:@@@       .*@@@@@@@@@@@@@@@@@:   
                         :@@@@@@@@@@@@@@@     @@@   ..@@@+:--=@#.@% @#%@@@#=:@@      *@@@@@@@@@@@@@*-::.    
                         :@@@@@@@@@@@@@@@    @@@  :.@@..-++=@@@@. @ =@+@@@@@#:@@@   -@@@@@@@@@@@@@*:        
                         :@@@@@@@@@@@@@@@    @@  :*@.:-=-+@@%-@@@# @ @:@@@@@@#:@@   -@@@@@@@@@@@@@-         
                         :@@@@@@@@@@@@@@@    @@ .-@ -+=@@@=++=@.-@ @ @-@@@@@@@-@@@  -@@@@@@@@@@@@@.         
                         :@@@@@@@@@@@@@@@    @@ .@@ *@@@:*%=.@@@ @-@ @-%@@@@@@-@@@  -@@@@@@@@@@@@@.         
                         :@@@@@@@@@@@@@@@    @@   @ :@@.%@+-@ *@@ @@ @-@@@@@@#.@@   -@@@@@@@@@@@@@.         
                         :@@@@@@@@@@@@@@@     @@  @@ @@ %@.@ :@@@ @@@@-@@@@@*:@@@   -@@@@@@@@@@@@@.         
                         :@@@@@@@@@@@@@@@      @@   @ @-.* @ -%@@-@ @@*@@@#=:@@     -@@@@@@@@@@@@@.         
                         :@@@@@@@@@@@@@@@       @@@  -@@@  @@ .%* #@@-%#=:-@@@      -@@@@@@@@@@@@@.         
                         -@@@@@@@@@@@@@@%         @@@@   @.  @ =*@@@...-@@@@        -@@@@@@@@@@@@@.         
                          .:::::::::::::.             @@@@@@@@@@@@-*@@@@             ::::::::::::.  
""")

discord_banner = MainColor2(r"""
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                  
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                  
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                   
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                      
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@                           
""")

dox_banner = MainColor2(r"""                                            
                  .:+*#%%#####*++++-.             
                :#%%*+*+-.....                    
             .=%%+++:..                           
           .=%#++=.                               
          -%%+++.                                 
      .  =%%++-          ....                     
      #%+#%++=.        .:#%%%*:                   
      :#@%#+=          :*+:-*%#:                  
       .*@@#.         .-%*::-%%#.                 
        .-%@@%-.      .=%%--%%%-                  
          .:--=*+-:.:-#%%%%%%%%*.                      ██████╗   ██████╗  ██╗  ██╗
               .:-*#%%%%%%%%%%%%%-                     ██╔══██╗ ██╔═══██╗ ╚██╗██╔╝
                  .+%%%*+*%%%%%%%%+...                 ██║  ██║ ██║   ██║  ╚███╔╝ 
                  .+%@@%%%%*#%%%%%%%%%*-.              ██║  ██║ ██║   ██║  ██╔██╗
                   .*%@%%%%%%%%%%%%%%%%%#-.            ██████╔╝ ╚██████╔╝ ██╔╝ ██╗
                   .*%%%%%%%%%%%+#%%%%%%%%%*-.         ╚═════╝   ╚═════╝  ╚═╝  ╚═╝
                  .=%%%%%%%%%%%%@%*%%%%%####=-==  
                  :*%%%%%%%%%%%%%%%*#%%%%#+=-==+  
                 .+=*%#%%%%%%%%%%%%%**%%#+**+-:-  
                .-=::*-%%%%%%%%%%%%###*-*%###+:   
                ...:..%%%%%%%%%%%%%%#:=*+-:.      
                     *%%%%%%%%%%%%%%%%.           
                    :#%%%%%%%%%%%%%%%%+           
                   .*%%%%%%%%%%%%%%%%%#.          
                  .=%%%%%%%%%%%%%%%%%%#:          
                  .+%%%%%%%%%%%%%%%%%%%*.         
                    :+*#%%%@%%%%%%%%%%%%#:.       
                      ..:==+*#%#*=-:.:-+***:.""")


osint_banner = MainColor2(r"""                                                                                                
                                          ...:----:...                                              
                                     .:=#@@@@@@@@@@@@@@%*-..                                        
                                  .:#@@@@@@@%#*****#%@@@@@@@+..                                     
                               ..-@@@@@%-...... ........+@@@@@@..                                   
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.                                  
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.                                
                            .#@@@%.                 .=@@@@@=. .@@@@-.                               
                           .=@@@#.                    .:%@@@*. -@@@%:.                              
                           .%@@@-                       .*@@*. .+@@@=.                              
                           :@@@#.                              .-@@@#.                              
                           -@@@#                                :%@@@.                              
                           :@@@#.                              .-@@@#.                              
                           .%@@@-.                             .+@@@=.                              
                           .+@@@#.                             -@@@%:.                              
                            .*@@@%.                          .:@@@@-.                               
                             .+@@@@=..                     ..*@@@@:.                                
                               :%@@@@-..                ...+@@@@*.                                  
                               ..-@@@@@%=...         ...*@@@@@@@@#.                                 
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.                              
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.                            
                                        .....:::::::....       ...+@@@@%:                           
                                                                  ..+@@@@%-.                        
                                                                    ..=@@@@%-.                      
                                                                      ..=@@@@@=.                    
                                                                         .=%@@@@=.                  
                                                                          ..-%@@@-.                 
                                                                             ....""")

wifi_banner = MainColor2(r"""
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@                                       
""")


phishing_banner = MainColor2(r"""
                                                         .+#%@@%#+.                                     
                                                    .#@@@@@@@@@@@@@@@@#.                                
                                                  +@@@@@@@@@@@@@@@@@@@@@@*                              
                                                .%@@@@@@@@@@@@@@@@@@@@@@@@%.                            
                                                %@@@@@@@@@@@@@@@@@@@@@@@@@@%                            

                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                          
                                                -..........................-.                           
                                                %@@@@@@%%@@@@@@@@@@@%@@@@@@%                            
                                                %@@@#     .%@@@@%.     *@@@%                            
                                                . :+%%+--+%@#::#@%*--+%%+: .                            
                                                                           .                            
                                                 :                        :                             
                                                  -                      =                              
                                                    -                  -                                
                                                       -=          --                                   
                                               -+#%@@@@@@=        =@@@@@@%#+-                           
                                            *@@@@@@@@@@@@=        =@@@@@@@@@@@@*                        
                                          *@@@@@@@@@@@@@@+        +@@@@@@@@@@@@@@#                      
                                         *@@@@@@@@@@@@@@@@%=    -%@@@@@@@@@@@@@@@@#                     
                                        -@@@@@@@@@@@@@@@@@@@%#*%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-  """)

decrypted_banner = MainColor2(r"""
                                         ^M@@@@@@@@@v                                    
                                      v@@@@@@@@@@@@@@@@@                                 
                                    _@@@@@@@}    ;a@@@@@@@                               
                                   M@@@@@            @@@@@@                              
                                  ;@@@@@              O@@@@@                             
                                  @@@@@v               @@@@@                             
                                  @@@@@;               @@@@@                             
                                  @@@@@;                                                 
                                  @@@@@;        v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@j     @@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@v       @@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@_   @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|      
                                               ^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@O  """)


encrypted_banner = MainColor2(r"""
                                                       j@@@@@^                                 
                           _@v   p@@@@j           j@@@@@@@@@@@@@@@;          |@@@@M   v@}      
                          @@@@@} >@@@@    v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@p    @@@@_ _@@@@@     
                          >@@@v    @@     v@@@@@@@@@@@@      p@@@@@@@@@@@a     @@    j@@@_     
                           ^@@     @@@@   |@@@@@@@@@@^ @@@@@@; @@@@@@@@@@p   p@@@     M@;      
                           ^@@            >@@@@@@@@@@ p@@@@@@@ M@@@@@@@@@j            M@;      
                           ^@@@@@@@@@@@}   @@@@@@@@|            >@@@@@@@@;   @@@@@@@@@@@;      
                                           }@@@@@@@|    O@@@    >@@@@@@@M                      
                          |@@@@             @@@@@@@|     M@     >@@@@@@@^            @@@@j     
                          @@@@@@@@@@@@@@@>   @@@@@@|    O@@@    >@@@@@@    @@@@@@@@@@@@@@@     
                            ^                 @@@@@v            }@@@@@^                ^       
                                 p@@@@@@@@@^   M@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@p            
                                 p@_            ^@@@@@@@@@@@@@@@@@@>            >@a            
                                @@@@O              @@@@@@@@@@@@@@              J@@@@           
                               ;@@@@@                 J@@@@@@p                 @@@@@>          
                                  ;              p@              p@>  M@@_       ;             
                                          @@@@p  p@_  ;      j_  a@@@@@@@@j                    
                                         ^@@@@@@@@@   v@_   O@}       M@@_                     
                                            ;         p@|   O@}      }}                        
                                                    >@@@@@  O@@@@@@@@@@@J                      
                                                     p@@@j         ;@@@@^                      """)


scan_banner = MainColor2(r"""
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                              >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@| 
""")



sql_banner = MainColor2(r"""
                                                                                   ^                      
                                                                                 J@@M                     
                                                                        ^         @@@@^                   
                                                                     ;@@@>         J@@@                   
                                                                      ;@@@J      ;j j@@@}                 
                                                                       ^@@@O  ^J@@@@^;@@@}                
                                                                   >@@@; @@@@^;@@@@@> ;@@@O               
                                                                >j _@@@@j p@@@^;@|      @@@>              
                                                              }@@@@  @@@@j J@@@>                          
                                                          ^a@@ _@@@@;_@@@@a }@@@>                         
                                                       ^} v@@@@^;@@@@@@@@@@@ >@@@v                        
                                                     |@@@@ ^@@@@J@@@@@@@@@@@@;^@@@J                       
                                                  J@M }@@@@ _@@@@@@@@@@@@@@j    @@j                       
                                               ; v@@@@ >@@@@@@@@@@@@@@@@j                                 
                                            ^@@@@ ;@@@@v@@@@@@@@@@@@@j^                                   
                                            a@@@@@ >@@@@@@@@@@@@@@a                                       
                                            |@@@@@@@@@@@@@@@@@@J                                          
                                          |a ;@@@@@@@@@@@@@@a;                                            
                                         @@@@ ;@@@@@@@@@@@;                                               
                                        |@@@@@> @@@@@@@>                                                  
                                     }@@@pO@MJ   >pp_                                                     
                                  ;@@@a                                                                   
                               ;@@@p;                                                                     
                            >p@@M>                                                                        
                           }@@>                                                                           
""")



map_banner = MainColor2(r"""
                                      :**+ :::+*@@.                                                         
                              +: @ = =.  :#@@@@@@@@                 :     .=*@@#     -                      
                 @@@@-. :=: +@@.:% *=@@:   @@@@@@          :#=::     .:@=@@@@@@@@@@@@@@@@@@@@--.-:          
             .#@@@@@@@@@@@@@@@@@@:# .@@   #@@    :@-     +@@:@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*        
             #*   :%@@@@@@@@@@:   .@@#*              ..  ##@ *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:- %=         
                   *@@@@@@@@@@@@%@@@@@@@            = @=+@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   #.        
                   #@@@@@@@@@##@@@@@= =#              #@@@#@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=            
                  @@@@@@@@@@@#+#@@=                 :@@@-.#-*#@.  .@@.=%@@@@%@@@@@@@@@@@@@@@@@=  +          
                 :@@@@@@@@@@@@@@:                   :@@    # - @@@@@@@ =@@@*#*@@@@@@@@@@@@@=.=-  #:         
                  :@@@@@@@@@@@+                     @@@@@@@: :    @@@@@@@@@@@@@@@@@@@@@@@@@@@               
                   #@@@@@    @                     #%@@@@@@@@@@@@@@@@@:@@@@@@@@@@@@#@@@@@@@@@:              
                     @@@     .                    @@@@@@@@@@@@@@@@-%@@@%@#   @@@@@@#=@#@@@@@==              
                     =@@##@   =:*.                @@@@@@*@@@@@@@@@@-=@@@@.    +@@@:  %#@@#=   :             
                         .=@.                     #@@@@@@@@#@@@@@@@@+#:        %@      *%@=                 
                            . @@@@@@               @#@@*@@@@@@@@@@@@@@@=        :-     -       =.           
                             :@@@@@@@#=                   @@@@@@@@@@@@-               :+%  .@=              
                            -@@@@@@@@@@@@                 @+@@@@*+@@#                   @. @@.#   # :       
                             @@@@@@@@@@@@@@@               @@@@@*@@@                     :=.        @@@.    
                              @@@@@@@@@@@@@                #@@@@@@%@.                             :  :      
                               *@@@@@@@@@@%               :@@@@@@@@@ @@.                      .@@@@=:@      
                                :@@@@@@@@@                 #@@@@@@   @:                    .#@@@@@@@@@@     
                                :@@@@%@@                   .@@@@@-   .                     @@@@@@@@@@@@*    
                                :@@@@@@.                    *@@@-                          @@@@#@@@@@@@     
                                .@@@@@                                                           =@@@:    @=
                                 =@@                                                              =    #+   
                                  @%                                                                        
""")



virus_banner = MainColor2(r"""
                                                         ...                                       
                                                  +%@@@@@@@@@@@@@*.                                
                                               #@@@@@@@@@@@@@@@@@@@@@:                             
                                             %@@@@@@@@@@@@@@@@@@@@@@@@@:                           
                                           .@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                          
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                          
                                           =@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                          
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@*                          
                                            #@@@%.     .@@@@+      #@@@%                           
                                             +@@=      .@@@@=      .@@#                            
                                              @@@@%%%@@@@%*@@@@%%%@@@@=                            
                                             .@@@@@@@@@@*  -@@@@@@@@@@=                            
                                           .    .::-@@@@@@@@@@@@+::.    .                          
                                         *@@@@#     @@@@@@@@@@@@-    +@@@@@.                       
                                         #@@@@@%    -%@@@@@@@@%=.   *@@@@@@:                       
                                       @@@@@@@@@@@@:            .#@@@@@@@@@@@-                     
                                       +@@@@@*#@@@@@@@@*:  .+@@@@@@@@%*%@@@@#                      
                                                    *@@@@@@@@@@%.                                  
                                        .==.    .+%@@@@@@@%@@@@@@@+:     :=:                       
                                       @@@@@@@@@@@@@@*.       :@@@@@@@@@@@@@@=                     
                                       -@@@@@@@@%=                :#@@@@@@@@*                      
                                         *@@@@@:                     %@@@@@:                       
                                         :%@@%.                       *@@@=                       
""")



logo_banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡠⠶⡶⠀⠉⠉⠋⠛⠒⠉⠈⠀⠈⠉⠉⠋⠉⠉⠀⠒⠂⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠠⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢤⡲⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⡀⠠⢀⠀⠠⠀⠄⡀⢂⠀⡀⠁⡐⡂⢀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡾⠞⠁⠀⠀⠀⢀⠀⢀⡈⠠⣤⡴⢷⣴⠾⣴⣫⡾⠽⠮⠿⠾⠶⡍⣶⣶⣄⣹⣀⡇⣤⡘⣖⣞⣢⢸⣌⡀⠢⠄⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⡶⠛⢁⠀⠀⠀⠀⠀⡀⠀⣀⠈⡁⠄⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠈⠉⠉⠉⠀⠒⠒⠒⠫⠭⠍⢙⣛⡚⠯⠷⢯⣻⣦⠻⡴⣆⡀⢒⠀⠙⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣺⡼⢀⣪⡤⠴⠛⠊⠩⠐⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠐⠂⠭⠭⠓⡛⠧⢗⣄⠄⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⣝⡞⠋⣉⡀⠠⣤⡠⣤⠤⢤⣤⣀⣀⣀⣀⠀⠀⠀⠀⢀⣀⣀⣀⣀⢀⣀⣀⣀⡀⠀⠀⡀⠠⠀⠤⠤⠤⠤⠂⠐⠦⠒⣒⣢⣤⣤⣀⣠⢍⢐⣒⠉⢀⠨⡢⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠝⣿⢾⣻⣭⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣴⣲⣤⣰⣒⢢⣤⣀⡀⠀⠌⠙⠁⠢⠙⠭⢿⣯⡿⣶⣄⡙⠵⡀⢀⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢿⣿⣷⣿⣾⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣷⣾⣿⣿⣾⣾⣷⣾⣧⣤⣴⣤⣭⣍⣁⠛⢛⣿⣷⠏⢹⠦⠡⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡿⠛⠉⠙⣿⣿⣿⣷⣿⣾⣻⢷⣯⣷⢿⣻⢿⣻⢿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⠃⢀⣀⠻⠲⣧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠟⠉⠀⢀⠀⣀⠶⣫⣽⣿⣾⣷⣿⣻⣽⣾⣿⣻⣿⣽⣿⣳⣯⣟⣯⣷⢿⣽⣾⣿⣻⣟⣿⣿⣻⣿⡿⣿⢿⡿⣿⢿⣿⣻⢿⣟⣿⣻⣽⣿⣿⣟⣿⣻⠟⡿⠹⠉⠁⠻⣿⣿⣟⠻⣧⡜⠂⢠⡖⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠿⠋⠀⠀⢠⣑⠶⣾⣹⠿⣳⠧⡹⠓⢯⢷⠟⠼⢻⡝⣿⣛⡾⣽⢯⡿⣽⣿⣾⡿⣟⣾⢷⡿⣽⣾⣳⣿⣳⣿⢿⣻⢿⣟⡿⣞⣿⣻⢾⣟⣯⠿⣽⣻⡏⢾⠗⣣⣊⠡⠀⠀⠀⠸⢿⣿⣷⣼⡟⣉⠙⣠⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠡⢀⢠⠖⡷⢻⣏⡷⡩⣈⠩⠗⠋⠙⠈⠀⠐⡜⠆⡋⣝⡓⡿⣝⡞⡿⣽⣟⣾⡷⣿⣿⣯⣿⣿⣽⣷⣻⣽⣻⢾⣻⣟⢯⡿⡽⣛⠬⡍⢯⡈⠥⠚⠴⠱⡼⣈⠶⡄⢞⣡⠆⡐⡂⠀⠀⠙⠛⠻⡧⡄⡀⠸⡄
⠀⠀⠀⠀⠀⠀⠀⢀⣾⡿⠯⡐⣤⣶⡿⣙⡟⠋⠫⠕⠀⠁⠀⠀⠀⠀⠀⠀⠑⠈⠸⡈⠛⡿⣟⡎⢿⢽⣳⢿⣻⣿⣷⣿⣾⣿⣾⣟⣯⣿⣶⣟⣯⢷⣻⣎⠷⡱⣌⠲⠈⢢⡑⡄⢘⠂⢋⣵⢊⠶⣉⡞⡴⢛⠥⣍⡐⠀⢀⠀⠀⠠⢊⠙⠋⠀⡇
⠀⠀⠀⠀⠀⠀⣰⣿⣯⣧⣷⣿⢿⢟⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⢢⢁⣿⡟⣭⣾⣻⣾⣯⣿⣟⣾⣿⡿⣟⣷⡿⣟⣾⣽⣾⢯⣿⣳⡾⢧⡳⣌⡙⣓⡢⢡⠘⡌⠏⠷⣎⣛⣞⡱⡞⣵⣫⠗⣬⡓⡯⣌⠰⢌⠒⣡⠖⠂⠀⠒
⠀⠀⠀⠀⢀⣾⡿⣿⣽⣾⢿⢿⠏⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡻⠀⡟⣞⢯⡷⣿⣟⣿⣿⢿⣿⣾⣿⣿⣿⣿⣟⣿⣿⢿⣽⣾⢿⡿⣽⡿⣽⡽⣳⣛⢦⡥⡢⠴⠞⡽⣫⠽⣓⣾⣹⡽⣎⡷⣋⢖⣹⠸⣅⢋⠀⡙⡠⠀⠀⠀⠀
⠀⠀⠀⠠⣻⡿⣿⣿⣟⡿⡻⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢈⡆⣔⠷⢱⡞⣟⣾⣟⣿⣾⣿⣿⡿⣿⣿⣯⣿⣷⣿⣯⣷⣿⣿⣻⢾⣿⣿⣻⣿⣯⣟⣷⣻⣞⡷⣯⡷⣾⠵⣷⣛⡷⣞⢧⡟⣵⡛⣬⢣⠜⣤⠃⠼⠂⢁⠀⠀⠀⠀⡄
⠀⠀⢀⣿⢿⣿⡿⢿⣽⡝⠃⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⢾⢺⣯⣿⣿⢿⡿⣾⣿⣿⣻⣟⣷⣿⡿⣷⣯⡿⣿⣷⣿⡷⣿⢯⣿⢿⣽⡿⣞⣿⣯⣷⣟⣿⣽⣿⣞⣿⡷⣯⣟⣾⣛⣞⣧⡝⣇⢣⡃⠏⠀⠀⠀⠄⠀⠀⠀⠀⣄
⠀⢀⢪⣿⣟⣾⣟⡟⢩⡄⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠠⢀⡀⢟⣿⣽⢾⣹⡿⣿⢯⣽⣿⡷⣿⣯⣿⣯⣿⢿⣿⣻⣽⣷⣿⣿⣽⣿⣿⢿⣻⣾⣿⣟⣿⣽⣷⣿⣯⣿⣷⡿⣿⣾⢷⣯⢷⣻⣼⠳⣌⡷⢉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿
⠀⡌⣮⣹⠚⡯⢦⠓⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⢴⡑⣋⢷⣫⡷⢾⢿⢷⣏⣷⢻⣎⣷⣿⢿⣯⣿⣟⣯⣿⣿⣯⣷⣿⣿⣞⣿⣿⣽⣿⡿⣷⣿⣾⡿⣿⣽⣿⣷⡿⣽⣿⣻⣞⣯⢷⣛⢮⡵⠋⢤⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠁
⣸⢙⠄⠇⠛⠖⠣⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⡳⣤⢛⢡⢏⠴⣣⠻⣯⢟⡿⣺⡜⣷⡽⣾⢽⣿⣻⢿⡿⣿⣿⣿⣾⣿⣟⣯⣿⣿⣯⣿⢿⣿⡿⣽⡾⣟⣿⣽⣿⣞⡿⣟⣷⡛⢮⡝⠺⢉⠢⠄⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⠀
⡀⠃⠀⠀⣀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢠⢐⠻⢡⢎⠾⣘⢋⡞⡽⣌⢯⣳⢳⣻⡵⣻⠽⣏⣷⢯⣟⣻⠷⣯⣟⠿⣞⣿⣿⣽⣞⡷⣽⡻⣞⡽⣷⣻⡽⣯⢟⡳⢯⠽⡙⠦⢙⠣⠬⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⢠⠃⠀
⡇⠀⠀⠀⠈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⢡⠋⢼⡉⠿⣖⣈⢆⡛⠶⡭⡚⠯⢳⡍⢷⣎⡿⣜⡺⣹⣎⠟⣛⠷⣼⣟⣳⢮⡵⢻⠷⣻⡽⡽⢾⡝⡣⢏⠹⠜⣋⠙⠆⢃⡘⠄⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠀⠀
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢈⠋⢂⠑⠂⢂⠠⠈⡐⠁⢆⠑⡊⠵⢘⠘⡌⠶⠩⢌⠁⡈⠙⡤⢋⠤⢘⢂⠣⡘⠡⠋⠜⡁⢉⠃⡘⠁⠂⠜⠐⡀⠈⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀
⢳⠀⡀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠄⠀⠁⠐⠈⡀⠢⢉⠂⠤⠈⠒⡠⠣⠘⡀⠘⡌⠱⠀⠌⢀⠣⠐⠡⢂⡐⠌⠰⢀⠓⠈⠢⠐⠠⠘⠀⠉⠒⠈⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⡜⠀⠀⠀⠀
⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠁⠀⠐⠄⠠⢀⠂⢀⠁⠐⠀⠄⠁⠌⡀⠰⠀⠑⠀⠀⠐⠉⠐⠠⠐⠈⠀⠂⠘⠀⠒⠂⠁⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⠁⠀⠀⠀⠀
⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠐⠀⠀⢀⡀⠀⠄⠠⠀⠁⠄⠀⠀⠁⠀⠠⠀⠀⠀⠀⠀⠊⠐⠀⡀⠄⡈⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠴⠚⠀⠀⠀⠀⠀⠀
⠀⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡲⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠢⠀⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠑⢄⠀⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠢⡀⠐⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠊⠄⡂⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⢀⡠⣤⠆⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠂⠥⠤⠄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⡀⠀⡀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡴⠾⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠐⠂⠒⠒⠒⠰⠦⠤⠤⠤⠤⠤⠄⠀⠠⢀⡀⣃⣄⣠⣀⣄⣄⣀⣘⣠⣄⣠⣄⣠⠤⠬⠰⠄⠾⠟⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                      
"""