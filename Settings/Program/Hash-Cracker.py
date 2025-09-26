from Config.Util import *
from Config.Config import *
try:
    import hashlib
    import threading
    import time
    import requests
except Exception as e:
    ErrorModule(e)

Title("Hash Cracker")

try:
    def identify_hash_type(hash_string):
        hash_length = len(hash_string)
        if hash_length == 32:
            return "MD5"
        elif hash_length == 40:
            return "SHA1"
        elif hash_length == 64:
            return "SHA256"
        elif hash_length == 128:
            return "SHA512"
        elif hash_string.startswith('$2b$') or hash_string.startswith('$2a$'):
            return "BCRYPT"
        elif hash_string.startswith('$6$'):
            return "SHA512CRYPT"
        elif hash_string.startswith('$5$'):
            return "SHA256CRYPT"
        elif hash_string.startswith('$1$'):
            return "MD5CRYPT"
        else:
            return "UNKNOWN"

    def crack_with_wordlist(hash_to_crack, hash_type, wordlist_url):
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Downloading wordlist...")
            response = requests.get(wordlist_url, timeout=30)
            wordlist = response.text.splitlines()
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loaded {white}{len(wordlist)}{red} passwords from wordlist")
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to download wordlist, using common passwords")
            wordlist = [
                'password', '123456', 'password123', 'admin', 'letmein', 'welcome',
                'monkey', '1234567890', 'qwerty', 'abc123', 'Password1', 'password1',
                'admin123', 'root', 'toor', 'pass', 'test', 'guest', 'info', 'adm',
                'mysql', 'user', 'administrator', 'oracle', 'ftp', 'pi', 'puppet',
                'ansible', 'ec2-user', 'vagrant', 'azureuser', 'postgres', 'jenkins'
            ]

        found = False
        attempts = 0
        
        for password in wordlist:
            if found:
                break
                
            attempts += 1
            if attempts % 1000 == 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Tested {white}{attempts}{red} passwords...")
            
            try:
                if hash_type == "MD5":
                    test_hash = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "SHA1":
                    test_hash = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "SHA256":
                    test_hash = hashlib.sha256(password.encode()).hexdigest()
                elif hash_type == "SHA512":
                    test_hash = hashlib.sha512(password.encode()).hexdigest()
                else:
                    continue
                
                if test_hash.lower() == hash_to_crack.lower():
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} CRACKED! Password: {white}{password}{green}")
                    found = True
                    break
            except:
                continue
        
        if not found:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Hash not cracked with wordlist attack")
        
        return found

    def online_hash_lookup(hash_to_crack):
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Checking online hash databases...")
        
        # Multiple hash lookup services
        services = [
            f"https://md5decrypt.net/Api/api.php?hash={hash_to_crack}&hash_type=md5&email=decodeit@gmail.com&code=1152464b80a61728",
            f"https://hashtoolkit.com/reverse-hash/?hash={hash_to_crack}",
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200 and response.text and response.text != "NOT FOUND":
                    if len(response.text) < 100:  # Reasonable password length
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} CRACKED! Password: {white}{response.text.strip()}{green}")
                        return True
            except:
                continue
        
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Hash not found in online databases")
        return False

    Slow(f"""{decrypted_banner}
 {BEFORE}01{AFTER}{white} Auto-detect hash type
 {BEFORE}02{AFTER}{white} Manual hash type selection
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Detection mode -> {reset}")
    
    hash_to_crack = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Hash to crack -> {reset}")
    
    if choice in ['1', '01']:
        hash_type = identify_hash_type(hash_to_crack)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Detected hash type: {white}{hash_type}{red}")
    else:
        print(f"""
 {BEFORE}01{AFTER}{white} MD5
 {BEFORE}02{AFTER}{white} SHA1  
 {BEFORE}03{AFTER}{white} SHA256
 {BEFORE}04{AFTER}{white} SHA512
        """)
        type_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Hash type -> {reset}")
        
        if type_choice in ['1', '01']:
            hash_type = "MD5"
        elif type_choice in ['2', '02']:
            hash_type = "SHA1"
        elif type_choice in ['3', '03']:
            hash_type = "SHA256"
        elif type_choice in ['4', '04']:
            hash_type = "SHA512"
        else:
            ErrorChoice()

    print(f"""
 {BEFORE}01{AFTER}{white} Online hash lookup
 {BEFORE}02{AFTER}{white} Wordlist attack
 {BEFORE}03{AFTER}{white} Both methods
    """)
    
    method = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Cracking method -> {reset}")
    
    if method in ['1', '01', '3', '03']:
        if online_hash_lookup(hash_to_crack):
            Continue()
            Reset()
    
    if method in ['2', '02', '3', '03']:
        wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt"
        crack_with_wordlist(hash_to_crack, hash_type, wordlist_url)

    Continue()
    Reset()
except Exception as e:
    Error(e)