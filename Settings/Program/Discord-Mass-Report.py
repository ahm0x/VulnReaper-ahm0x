from Config.Util import *
from Config.Config import *
try:
    import requests
    import threading
    import time
    import json
    import random
except Exception as e:
    ErrorModule(e)

Title("Discord Mass Report")

try:
    Slow(discord_banner)
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Mass Reporting Tool - Educational purposes only")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {red}Warning: Misuse can result in account suspension")
    
    def report_user(token, user_id, guild_id, channel_id, message_id, reason):
        """Report a user to Discord"""
        try:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            report_data = {
                'version': '1.0',
                'variant': '3',
                'language': 'en',
                'breadcrumbs': [
                    guild_id,
                    channel_id,
                    message_id,
                    user_id
                ],
                'elements': {},
                'name': reason,
                'channel_id': channel_id,
                'message_id': message_id,
                'guild_id': guild_id
            }
            
            response = requests.post(
                'https://discord.com/api/v9/reporting/menu',
                headers=headers,
                json=report_data,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Success"
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)

    def get_user_messages(token, channel_id, user_id, limit=50):
        """Get recent messages from a user in a channel"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            
            params = {
                'author_id': user_id,
                'limit': limit
            }
            
            response = requests.get(
                f'https://discord.com/api/v9/channels/{channel_id}/messages/search',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                messages = []
                
                for message_group in data.get('messages', []):
                    for message in message_group:
                        if message['author']['id'] == user_id:
                            messages.append({
                                'id': message['id'],
                                'content': message['content'][:100],
                                'timestamp': message['timestamp']
                            })
                
                return messages
            else:
                return []
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error getting messages: {white}{e}")
            return []

    def mass_report_execution(tokens, target_user_id, guild_id, channel_id, message_id, reason):
        """Execute mass report with multiple tokens"""
        def report_with_token(token):
            try:
                success, result = report_user(token, target_user_id, guild_id, channel_id, message_id, reason)
                
                if success:
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Report sent: {white}{token[:20]}...{green} Reason: {white}{reason}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Report failed: {white}{token[:20]}...{red} Error: {white}{result}")
                
                # Random delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Token error: {white}{e}")
        
        threads = []
        for token in tokens:
            thread = threading.Thread(target=report_with_token, args=(token,))
            threads.append(thread)
            thread.start()
            time.sleep(0.5)  # Stagger requests
        
        for thread in threads:
            thread.join()

    print(f"""
 {BEFORE}01{AFTER}{white} Report specific message
 {BEFORE}02{AFTER}{white} Report user profile
 {BEFORE}03{AFTER}{white} Analyze user messages
 {BEFORE}04{AFTER}{white} Mass report with multiple tokens
    """)
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Report type -> {reset}")
    
    if choice in ['1', '01']:
        guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Server ID -> {reset}")
        channel_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Channel ID -> {reset}")
        message_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Message ID -> {reset}")
        user_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} User ID to report -> {reset}")
        
        print(f"""
 {BEFORE}01{AFTER}{white} Harassment
 {BEFORE}02{AFTER}{white} Spam
 {BEFORE}03{AFTER}{white} Inappropriate content
 {BEFORE}04{AFTER}{white} Hate speech
 {BEFORE}05{AFTER}{white} Doxxing/Personal info
        """)
        
        reason_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Report reason -> {reset}")
        reason_map = {
            '1': 'harassment', '01': 'harassment',
            '2': 'spam', '02': 'spam',
            '3': 'inappropriate_content', '03': 'inappropriate_content',
            '4': 'hate_speech', '04': 'hate_speech',
            '5': 'doxxing', '05': 'doxxing'
        }
        
        reason = reason_map.get(reason_choice, 'harassment')
        
        success, result = report_user(token, user_id, guild_id, channel_id, message_id, reason)
        
        if success:
            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Report submitted successfully")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Report failed: {white}{result}")
    
    elif choice in ['2', '02']:
        user_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} User ID to report -> {reset}")
        
        # Get user info
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            response = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} Target User:
    Username: {white}{user_data['username']}#{user_data['discriminator']}
    ID: {white}{user_data['id']}
    Created: {white}{user_data.get('created_at', 'Unknown')}""")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} User not found")
        except:
            pass
    
    elif choice in ['3', '03']:
        channel_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Channel ID -> {reset}")
        user_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} User ID to analyze -> {reset}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Analyzing user messages...")
        messages = get_user_messages(token, channel_id, user_id)
        
        if messages:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(messages)}{red} recent messages:")
            for i, msg in enumerate(messages[:10]):
                print(f"  {white}{i+1}.{red} {msg['content']} (ID: {msg['id']})")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No messages found")
    
    elif choice in ['4', '04']:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {red}WARNING: This can result in account suspensions")
        confirm = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Continue? (y/n) -> {reset}")
        
        if confirm.lower() not in ['y', 'yes']:
            Continue()
            Reset()
        
        tokens = ChoiceMultiTokenDisord()
        guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Server ID -> {reset}")
        channel_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Channel ID -> {reset}")
        message_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Message ID -> {reset}")
        user_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} User ID to report -> {reset}")
        
        print(f"""
 {BEFORE}01{AFTER}{white} Harassment
 {BEFORE}02{AFTER}{white} Spam
 {BEFORE}03{AFTER}{white} Inappropriate content
 {BEFORE}04{AFTER}{white} Hate speech
        """)
        
        reason_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Report reason -> {reset}")
        reason_map = {
            '1': 'harassment', '01': 'harassment',
            '2': 'spam', '02': 'spam',
            '3': 'inappropriate_content', '03': 'inappropriate_content',
            '4': 'hate_speech', '04': 'hate_speech'
        }
        
        reason = reason_map.get(reason_choice, 'harassment')
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Executing mass report with {white}{len(tokens)}{red} tokens...")
        mass_report_execution(tokens, user_id, guild_id, channel_id, message_id, reason)
    
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)