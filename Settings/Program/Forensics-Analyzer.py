from Config.Util import *
from Config.Config import *
try:
    import hashlib
    import os
    import time
    import binascii
    import struct
    from datetime import datetime
except Exception as e:
    ErrorModule(e)

Title("Digital Forensics Analyzer")

try:
    def calculate_file_hashes(file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            md5_hash = hashlib.md5(content).hexdigest()
            sha1_hash = hashlib.sha1(content).hexdigest()
            sha256_hash = hashlib.sha256(content).hexdigest()
            
            return {
                'md5': md5_hash,
                'sha1': sha1_hash,
                'sha256': sha256_hash,
                'size': len(content)
            }
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error calculating hashes: {white}{e}")
            return None

    def analyze_file_metadata(file_path):
        try:
            stat = os.stat(file_path)
            
            metadata = {
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'permissions': oct(stat.st_mode)[-3:]
            }
            
            return metadata
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error analyzing metadata: {white}{e}")
            return None

    def detect_file_type(file_path):
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
            
            # File signatures
            signatures = {
                b'\x89PNG\r\n\x1a\n': 'PNG Image',
                b'\xff\xd8\xff': 'JPEG Image',
                b'GIF87a': 'GIF Image',
                b'GIF89a': 'GIF Image',
                b'%PDF': 'PDF Document',
                b'PK\x03\x04': 'ZIP Archive',
                b'Rar!\x1a\x07\x00': 'RAR Archive',
                b'\x7fELF': 'ELF Executable',
                b'MZ': 'Windows Executable',
                b'\xca\xfe\xba\xbe': 'Java Class File',
                b'\xfe\xed\xfa': 'Mach-O Executable',
            }
            
            for sig, file_type in signatures.items():
                if header.startswith(sig):
                    return file_type
            
            return 'Unknown'
        except:
            return 'Unknown'

    def search_strings(file_path, min_length=4):
        try:
            strings_found = []
            with open(file_path, 'rb') as f:
                content = f.read()
            
            current_string = ""
            for byte in content:
                if 32 <= byte <= 126:  # Printable ASCII
                    current_string += chr(byte)
                else:
                    if len(current_string) >= min_length:
                        strings_found.append(current_string)
                    current_string = ""
            
            # Don't forget the last string
            if len(current_string) >= min_length:
                strings_found.append(current_string)
            
            return strings_found
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error extracting strings: {white}{e}")
            return []

    def analyze_network_artifacts():
        if not sys.platform.startswith("win"):
            OnlyWindows()
            return
        
        try:
            # Get network connections
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            connections = []
            
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line or 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        connections.append({
                            'protocol': parts[0],
                            'local': parts[1],
                            'remote': parts[2],
                            'state': parts[3] if len(parts) > 3 else 'N/A'
                        })
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Active network connections:")
            for conn in connections[:20]:  # Limit output
                print(f"  {white}{conn['protocol']}{red} {conn['local']} -> {conn['remote']} [{conn['state']}]")
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error analyzing network: {white}{e}")

    Slow(f"""{scan_banner}
 {BEFORE}01{AFTER}{white} File hash analysis
 {BEFORE}02{AFTER}{white} File metadata analysis
 {BEFORE}03{AFTER}{white} File type detection
 {BEFORE}04{AFTER}{white} String extraction
 {BEFORE}05{AFTER}{white} Network artifacts analysis
 {BEFORE}06{AFTER}{white} Complete file analysis
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Analysis type -> {reset}")
    
    if choice in ['1', '01', '6', '06']:
        file_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} File path -> {reset}")
        if not os.path.exists(file_path):
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File not found")
            Continue()
            Reset()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Calculating file hashes...")
        hashes = calculate_file_hashes(file_path)
        if hashes:
            print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} File Hashes:
    MD5:    {white}{hashes['md5']}{red}
    SHA1:   {white}{hashes['sha1']}{red}
    SHA256: {white}{hashes['sha256']}{red}
    Size:   {white}{hashes['size']} bytes{red}""")

    if choice in ['2', '02', '6', '06']:
        if 'file_path' not in locals():
            file_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} File path -> {reset}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Analyzing file metadata...")
        metadata = analyze_file_metadata(file_path)
        if metadata:
            print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} File Metadata:
    Size:        {white}{metadata['size']} bytes{red}
    Created:     {white}{metadata['created']}{red}
    Modified:    {white}{metadata['modified']}{red}
    Accessed:    {white}{metadata['accessed']}{red}
    Permissions: {white}{metadata['permissions']}{red}""")

    if choice in ['3', '03', '6', '06']:
        if 'file_path' not in locals():
            file_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} File path -> {reset}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Detecting file type...")
        file_type = detect_file_type(file_path)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File Type: {white}{file_type}")

    if choice in ['4', '04', '6', '06']:
        if 'file_path' not in locals():
            file_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} File path -> {reset}")
        
        try:
            min_length = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Minimum string length (default: 4) -> {reset}") or "4")
        except:
            min_length = 4
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Extracting strings...")
        strings = search_strings(file_path, min_length)
        
        if strings:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(strings)}{red} strings")
            
            # Save strings to file
            output_file = os.path.join(tool_path, "1-Output", "Forensics", f"strings_{os.path.basename(file_path)}.txt")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for string in strings:
                    f.write(string + '\n')
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Strings saved to: {white}{output_file}")
            
            # Show first 20 strings
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} First 20 strings:")
            for i, string in enumerate(strings[:20]):
                print(f"  {white}{string[:80]}{'...' if len(string) > 80 else ''}")

    if choice in ['5', '05']:
        analyze_network_artifacts()

    Continue()
    Reset()
except Exception as e:
    Error(e)