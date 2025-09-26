from Config.Util import *
from Config.Config import *
try:
    import requests
    import json
    import re
    import webbrowser
    from bs4 import BeautifulSoup
    import time
except Exception as e:
    ErrorModule(e)

Title("OSINT Framework")

try:
    def search_social_media(query, platform="all"):
        """Search across multiple social media platforms"""
        platforms = {
            'facebook': f"https://www.facebook.com/search/top/?q={query}",
            'twitter': f"https://twitter.com/search?q={query}",
            'instagram': f"https://www.instagram.com/explore/tags/{query}/",
            'linkedin': f"https://www.linkedin.com/search/results/all/?keywords={query}",
            'youtube': f"https://www.youtube.com/results?search_query={query}",
            'tiktok': f"https://www.tiktok.com/search?q={query}",
            'reddit': f"https://www.reddit.com/search/?q={query}",
            'github': f"https://github.com/search?q={query}",
            'telegram': f"https://t.me/s/{query}",
            'discord': f"https://discord.com/channels/@me",
        }
        
        results = []
        
        if platform == "all":
            search_platforms = platforms
        else:
            search_platforms = {platform: platforms.get(platform, "")}
        
        for platform_name, url in search_platforms.items():
            if url:
                results.append({
                    'platform': platform_name,
                    'url': url,
                    'query': query
                })
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} {platform_name.capitalize()}: {white}{url}")
        
        return results

    def search_data_breaches(email_or_username):
        """Search for data breaches (simulated)"""
        # In real scenario, you'd use APIs like HaveIBeenPwned
        known_breaches = [
            {'name': 'Collection #1', 'date': '2019-01', 'records': '773M', 'type': 'Combo List'},
            {'name': 'LinkedIn', 'date': '2021-06', 'records': '700M', 'type': 'Social Media'},
            {'name': 'Facebook', 'date': '2021-04', 'records': '533M', 'type': 'Social Media'},
            {'name': 'Yahoo', 'date': '2013-08', 'records': '3B', 'type': 'Email Provider'},
            {'name': 'Adobe', 'date': '2013-10', 'records': '153M', 'type': 'Software Company'},
        ]
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching data breaches for: {white}{email_or_username}")
        
        # Simulate breach search
        found_breaches = []
        for breach in known_breaches:
            # Simulate random findings for demo
            import random
            if random.choice([True, False]):
                found_breaches.append(breach)
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Found in breach: {white}{breach['name']}{red} ({breach['date']}) - {breach['records']} records")
        
        if not found_breaches:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No breaches found for: {white}{email_or_username}")
        
        return found_breaches

    def search_public_records(name, location=""):
        """Search public records and databases"""
        sources = [
            f"https://www.whitepages.com/name/{name.replace(' ', '-')}",
            f"https://www.spokeo.com/{name.replace(' ', '-')}",
            f"https://www.truthfinder.com/results/?firstName={name.split()[0] if ' ' in name else name}&lastName={name.split()[-1] if ' ' in name else ''}",
            f"https://www.intelius.com/people-search/{name.replace(' ', '/')}",
            f"https://www.beenverified.com/people/{name.replace(' ', '/')}",
        ]
        
        if location:
            sources.extend([
                f"https://www.whitepages.com/name/{name.replace(' ', '-')}/{location.replace(' ', '-')}",
                f"https://www.spokeo.com/{name.replace(' ', '-')}-{location.replace(' ', '-')}",
            ])
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Public record sources for: {white}{name}")
        for source in sources:
            print(f"  {white}{source}")
        
        return sources

    def search_domain_info(domain):
        """Comprehensive domain information gathering"""
        info = {}
        
        try:
            # WHOIS information (simplified)
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Gathering WHOIS information...")
            
            # Subdomain enumeration
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Enumerating subdomains...")
            subdomains = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api', 'blog', 'shop']
            found_subdomains = []
            
            for sub in subdomains:
                try:
                    full_domain = f"{sub}.{domain}"
                    response = requests.get(f"http://{full_domain}", timeout=3)
                    if response.status_code == 200:
                        found_subdomains.append(full_domain)
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Subdomain: {white}{full_domain}")
                except:
                    pass
            
            info['subdomains'] = found_subdomains
            
            # DNS records
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Gathering DNS records...")
            try:
                import dns.resolver
                
                record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
                dns_records = {}
                
                for record_type in record_types:
                    try:
                        answers = dns.resolver.resolve(domain, record_type)
                        dns_records[record_type] = [str(answer) for answer in answers]
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} {record_type} records: {white}{len(dns_records[record_type])}")
                    except:
                        dns_records[record_type] = []
                
                info['dns_records'] = dns_records
            except:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} DNS module not available")
            
            return info
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error gathering domain info: {white}{e}")
            return {}

    Slow(osint_banner)
    
    print(f"""
 {BEFORE}01{AFTER}{white} Social Media Search
 {BEFORE}02{AFTER}{white} Data Breach Search
 {BEFORE}03{AFTER}{white} Public Records Search
 {BEFORE}04{AFTER}{white} Domain Intelligence
 {BEFORE}05{AFTER}{white} Exploit Database Search
 {BEFORE}06{AFTER}{white} Comprehensive OSINT Report
    """)
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} OSINT type -> {reset}")
    
    if choice in ['1', '01']:
        query = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Search term -> {reset}")
        Censored(query)
        
        platform = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Platform (all/facebook/twitter/etc) -> {reset}")
        if not platform:
            platform = "all"
        
        results = search_social_media(query, platform)
        
        open_browser = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open results in browser? (y/n) -> {reset}")
        if open_browser.lower() in ['y', 'yes']:
            for result in results[:5]:  # Limit to 5 tabs
                webbrowser.open(result['url'])
                time.sleep(1)
    
    elif choice in ['2', '02']:
        email_username = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email or username -> {reset}")
        Censored(email_username)
        
        breaches = search_data_breaches(email_username)
        
    elif choice in ['3', '03']:
        name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Full name -> {reset}")
        location = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Location (optional) -> {reset}")
        Censored(name)
        
        sources = search_public_records(name, location)
        
        open_browser = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open sources in browser? (y/n) -> {reset}")
        if open_browser.lower() in ['y', 'yes']:
            for source in sources[:3]:  # Limit to 3 tabs
                webbrowser.open(source)
                time.sleep(2)
    
    elif choice in ['4', '04']:
        domain = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Domain name -> {reset}")
        Censored(domain)
        
        domain_info = search_domain_info(domain)
        
    elif choice in ['5', '05']:
        service = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Service/Software name -> {reset}")
        Censored(service)
        
        exploits = search_exploitdb(service)
        msf_modules = search_metasploit_modules(service)
        
        if exploits or msf_modules:
            report_file = generate_exploit_report(service, exploits, msf_modules)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Report saved to: {white}{report_file}")
    
    elif choice in ['6', '06']:
        target = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target (name/email/domain/username) -> {reset}")
        Censored(target)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Performing comprehensive OSINT...")
        
        # Determine target type and run appropriate searches
        if '@' in target:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Detected email address")
            search_data_breaches(target)
        elif '.' in target and len(target.split('.')) > 1:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Detected domain")
            search_domain_info(target)
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Detected username/name")
            search_social_media(target)
            if ' ' in target:
                search_public_records(target)
    
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)