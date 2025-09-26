from Config.Util import *
from Config.Config import *
try:
    import requests
    import time
    import json
    import base64
    import random
    import string
except Exception as e:
    ErrorModule(e)

Title("Discord Token 2FA Bypass")

try:
    Slow(discord_banner)
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Advanced 2FA Analysis Tool")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Educational purposes only - Test your own accounts")
    
    token = Choice1TokenDiscord()
    
    def check_2fa_status(token):
        """Check if 2FA is enabled on account"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                mfa_enabled = user_data.get('mfa_enabled', False)
                return mfa_enabled, user_data
            else:
                return None, None
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error checking 2FA status: {white}{e}")
            return None, None

    def analyze_backup_codes(token):
        """Analyze backup codes availability"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            response = requests.get('https://discord.com/api/v9/users/@me/mfa/codes', headers=headers, timeout=10)
            
            if response.status_code == 200:
                codes_data = response.json()
                return codes_data
            else:
                return None
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error checking backup codes: {white}{e}")
            return None

    def test_session_persistence(token):
        """Test session persistence and token validity"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            
            # Test multiple endpoints to check token scope
            endpoints = [
                'https://discord.com/api/v9/users/@me',
                'https://discord.com/api/v9/users/@me/settings',
                'https://discord.com/api/v9/users/@me/guilds',
                'https://discord.com/api/v9/users/@me/relationships'
            ]
            
            results = {}
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=5)
                    results[endpoint.split('/')[-1]] = response.status_code
                except:
                    results[endpoint.split('/')[-1]] = 'Error'
            
            return results
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error testing session: {white}{e}")
            return {}

    def analyze_security_settings(token):
        """Analyze account security settings"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            response = requests.get('https://discord.com/api/v9/users/@me/settings', headers=headers, timeout=10)
            
            if response.status_code == 200:
                settings = response.json()
                security_info = {
                    'developer_mode': settings.get('developer_mode', False),
                    'explicit_content_filter': settings.get('explicit_content_filter', 0),
                    'friend_source_flags': settings.get('friend_source_flags', {}),
                    'guild_restricted_channels': settings.get('guild_restricted_channels', {}),
                    'status': settings.get('status', 'unknown')
                }
                return security_info
            else:
                return None
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error analyzing security: {white}{e}")
            return None

    # Perform analysis
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Analyzing account security...")
    
    mfa_enabled, user_data = check_2fa_status(token)
    
    if mfa_enabled is None:
        ErrorToken()
    
    print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} Account Security Analysis:
    Username: {white}{user_data.get('username', 'Unknown')}#{user_data.get('discriminator', '0000')}
    User ID: {white}{user_data.get('id', 'Unknown')}
    2FA Enabled: {white}{mfa_enabled}
    Email Verified: {white}{user_data.get('verified', False)}
    Phone: {white}{user_data.get('phone', 'None')}""")

    if mfa_enabled:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {green}2FA is enabled - Account is more secure")
        
        # Check backup codes
        backup_codes = analyze_backup_codes(token)
        if backup_codes:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Backup codes status: {white}Available")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Backup codes: {white}Not accessible or not generated")
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {red}2FA is NOT enabled - Account vulnerable")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Recommendation: Enable 2FA immediately")

    # Test session persistence
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Testing session persistence...")
    session_results = test_session_persistence(token)
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Token Access Scope:")
    for endpoint, status in session_results.items():
        status_color = green if status == 200 else red if isinstance(status, int) and status >= 400 else yellow
        print(f"    {endpoint}: {status_color}{status}")

    # Analyze security settings
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Analyzing security settings...")
    security_settings = analyze_security_settings(token)
    
    if security_settings:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Security Settings:")
        print(f"    Developer Mode: {white}{security_settings['developer_mode']}")
        print(f"    Content Filter: {white}{security_settings['explicit_content_filter']}")
        print(f"    Status: {white}{security_settings['status']}")

    # Security recommendations
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Security Recommendations:")
    if not mfa_enabled:
        print(f"    🔴 Enable 2FA immediately")
    if not user_data.get('verified', False):
        print(f"    🟡 Verify email address")
    if not user_data.get('phone'):
        print(f"    🟡 Add phone number for account recovery")
    
    print(f"    ✅ Use strong, unique passwords")
    print(f"    ✅ Regularly review authorized applications")
    print(f"    ✅ Monitor account activity")
    print(f"    ✅ Keep backup codes in secure location")

    Continue()
    Reset()
except Exception as e:
    Error(e)