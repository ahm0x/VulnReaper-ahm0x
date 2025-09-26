from Config.Util import *
from Config.Config import *
try:
    import requests
    import threading
    import dns.resolver
    import socket
    import ssl
    from urllib.parse import urlparse
except Exception as e:
    ErrorModule(e)

Title("Subdomain Enumeration")

try:
    def check_subdomain(subdomain, domain, results):
        full_domain = f"{subdomain}.{domain}"
        try:
            # DNS resolution check
            socket.gethostbyname(full_domain)
            
            # HTTP check
            for protocol in ['https', 'http']:
                try:
                    url = f"{protocol}://{full_domain}"
                    response = requests.get(url, timeout=3, verify=False)
                    status = response.status_code
                    title = "No Title"
                    
                    # Extract title
                    if 'text/html' in response.headers.get('content-type', ''):
                        try:
                            title_start = response.text.find('<title>')
                            title_end = response.text.find('</title>')
                            if title_start != -1 and title_end != -1:
                                title = response.text[title_start+7:title_end].strip()
                        except:
                            pass
                    
                    results.append({
                        'subdomain': full_domain,
                        'url': url,
                        'status': status,
                        'title': title[:50] + '...' if len(title) > 50 else title
                    })
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Found: {white}{full_domain}{green} [{status}] {title}")
                    break
                except:
                    continue
        except:
            pass

    Slow(scan_banner)
    domain = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target Domain -> {reset}")
    Censored(domain)
    
    try:
        threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 50) -> {reset}"))
    except:
        threads_number = 50

    # Common subdomains wordlist
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2',
        'cpanel', 'whm', 'autodiscover', 'autoconfig', 'ns3', 'm', 'imap', 'test', 'ns', 'blog',
        'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns4', 'email', 'webmaster',
        'beta', 'api', 'wap', 'mobile', 'img', 'video', 'shop', 'secure', 'support', 'web',
        'bbs', 'ww1', 'chat', 'demo', 'music', 'video', 'www1', 'my', 'store', 'photo',
        'search', 'cdn', 'media', 'static', 'download', 'en', 'it', 'fr', 'de', 'es',
        'pt', 'ru', 'pl', 'nl', 'jp', 'kr', 'cn', 'tw', 'hk', 'sg', 'au', 'ca',
        'staging', 'production', 'testing', 'sandbox', 'internal', 'intranet', 'extranet',
        'portal', 'gateway', 'proxy', 'firewall', 'router', 'switch', 'backup', 'mirror',
        'old', 'new', 'temp', 'tmp', 'archive', 'files', 'docs', 'help', 'wiki',
        'kb', 'support', 'ticket', 'bug', 'issues', 'git', 'svn', 'repo', 'code',
        'build', 'ci', 'jenkins', 'bamboo', 'teamcity', 'travis', 'gitlab', 'github',
        'bitbucket', 'jira', 'confluence', 'slack', 'teams', 'zoom', 'meet', 'webex',
        'vpn', 'ssh', 'sftp', 'rdp', 'vnc', 'telnet', 'snmp', 'ntp', 'dns', 'dhcp'
    ]

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Enumerating subdomains for {white}{domain}{red}...")
    
    results = []
    threads = []
    
    for subdomain in subdomains:
        thread = threading.Thread(target=check_subdomain, args=(subdomain, domain, results))
        threads.append(thread)
        thread.start()
        
        if len(threads) >= threads_number:
            for t in threads:
                t.join()
            threads = []

    # Wait for remaining threads
    for t in threads:
        t.join()

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Enumeration completed. Found {white}{len(results)}{red} subdomains.")
    
    if results:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Summary:")
        for result in results:
            print(f"  {white}{result['subdomain']}{red} -> {white}{result['url']}{red} [{result['status']}]")

    Continue()
    Reset()
except Exception as e:
    Error(e)