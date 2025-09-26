from Config.Util import *
from Config.Config import *
try:
    import requests
    import threading
    from urllib.parse import urljoin
    import os
    import itertools
except Exception as e:
    ErrorModule(e)

Title("Directory Bruteforce")

try:
    def check_directory(base_url, directory, results):
        url = urljoin(base_url, directory)
        try:
            response = requests.get(url, timeout=5, allow_redirects=False)
            if response.status_code in [200, 301, 302, 403]:
                size = len(response.content)
                results.append({
                    'url': url,
                    'status': response.status_code,
                    'size': size
                })
                
                status_color = green if response.status_code == 200 else yellow if response.status_code in [301, 302] else red
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Found: {white}{url}{status_color} [{response.status_code}] {size} bytes")
        except:
            pass

    def generate_custom_wordlist(keywords):
        """Generate custom directory wordlist from keywords"""
        combinations = []
        
        # Single words
        combinations.extend(keywords)
        
        # Common directory prefixes/suffixes
        prefixes = ['admin', 'test', 'dev', 'old', 'new', 'backup', 'temp', 'private']
        suffixes = ['admin', 'panel', 'login', 'test', 'old', 'new', 'backup', 'bak', '2024', '2023']
        
        # Add prefixes and suffixes
        for keyword in keywords:
            for prefix in prefixes:
                combinations.append(f"{prefix}_{keyword}")
                combinations.append(f"{prefix}-{keyword}")
                combinations.append(f"{prefix}{keyword}")
            
            for suffix in suffixes:
                combinations.append(f"{keyword}_{suffix}")
                combinations.append(f"{keyword}-{suffix}")
                combinations.append(f"{keyword}{suffix}")
        
        # Combinations of keywords
        for combo in itertools.combinations(keywords, 2):
            combinations.append('_'.join(combo))
            combinations.append('-'.join(combo))
            combinations.append(''.join(combo))
        
        # Add common variations
        variations = []
        for word in combinations:
            variations.append(word)
            variations.append(word.upper())
            variations.append(word.lower())
            variations.append(word.capitalize())
            
            # Add numbers
            for num in ['1', '2', '3', '01', '02', '03', '2024', '2025']:
                variations.append(word + num)
                variations.append(num + word)
        
        return list(set(variations))

    def download_directory_wordlists():
        """Download directory wordlists from SecLists"""
        wordlists = {
            'common': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt',
            'big': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt',
            'directory_list_2.3_medium': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt'
        }
        
        all_directories = []
        
        for name, url in wordlists.items():
            try:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Downloading {white}{name}{red} wordlist...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    directories = response.text.splitlines()
                    directories = [d.strip() for d in directories if d.strip() and not d.startswith('#')]
                    all_directories.extend(directories[:2000])  # Limit per wordlist
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Downloaded {white}{len(directories)}{red} directories from {name}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to download {name}")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error downloading {name}: {white}{e}")
        
        return list(set(all_directories))

    Slow(f"""{scan_banner}
 {BEFORE}01{AFTER}{white} Standard directory scan
 {BEFORE}02{AFTER}{white} Custom wordlist scan
 {BEFORE}03{AFTER}{white} Generate custom wordlist
 {BEFORE}04{AFTER}{white} Comprehensive scan (all methods)
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    target_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target URL -> {reset}")
    Censored(target_url)
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    if not target_url.endswith('/'):
        target_url += '/'

    if choice in ['1', '01', '4', '04']:
        # Standard scan
        try:
            threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 20) -> {reset}"))
        except:
            threads_number = 20

        # Extended common directories wordlist
        directories = [
            'admin', 'administrator', 'login', 'panel', 'cpanel', 'wp-admin', 'phpmyadmin',
            'backup', 'backups', 'bak', 'old', 'temp', 'tmp', 'test', 'testing', 'dev',
            'development', 'staging', 'prod', 'production', 'api', 'v1', 'v2', 'rest',
            'config', 'configuration', 'settings', 'setup', 'install', 'installation',
            'uploads', 'upload', 'files', 'file', 'documents', 'docs', 'download', 'downloads',
            'images', 'img', 'pics', 'pictures', 'photo', 'photos', 'media', 'assets',
            'css', 'js', 'javascript', 'scripts', 'style', 'styles', 'fonts', 'font',
            'includes', 'inc', 'lib', 'library', 'libraries', 'vendor', 'vendors',
            'cache', 'logs', 'log', 'debug', 'error', 'errors', 'trace', 'traces',
            'database', 'db', 'sql', 'mysql', 'postgres', 'sqlite', 'data',
            'private', 'secret', 'hidden', 'internal', 'secure', 'protected',
            'user', 'users', 'account', 'accounts', 'profile', 'profiles',
            'dashboard', 'control', 'manage', 'management', 'monitor', 'monitoring',
            'stats', 'statistics', 'analytics', 'reports', 'report', 'status',
            'help', 'support', 'contact', 'about', 'info', 'information',
            'search', 'find', 'lookup', 'browse', 'explorer', 'directory',
            'mail', 'email', 'webmail', 'smtp', 'pop3', 'imap',
            'ftp', 'sftp', 'ssh', 'telnet', 'rdp', 'vnc',
            'git', 'svn', 'cvs', 'mercurial', 'bzr', 'repository', 'repo',
            'jenkins', 'bamboo', 'teamcity', 'travis', 'circleci', 'gitlab-ci',
            'docker', 'kubernetes', 'k8s', 'helm', 'terraform', 'ansible',
            'prometheus', 'grafana', 'kibana', 'elasticsearch', 'logstash',
            'redis', 'memcached', 'mongodb', 'cassandra', 'couchdb',
            'nginx', 'apache', 'httpd', 'tomcat', 'jetty', 'websphere',
            'jboss', 'wildfly', 'glassfish', 'weblogic', 'iis',
            # Additional security-focused directories
            '.git', '.svn', '.env', '.htaccess', '.htpasswd', 'robots.txt', 'sitemap.xml',
            'crossdomain.xml', 'clientaccesspolicy.xml', 'web.config', '.DS_Store',
            'thumbs.db', 'desktop.ini', '.bash_history', '.mysql_history',
            'server-status', 'server-info', 'phpinfo.php', 'info.php', 'test.php'
        ]

        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Bruteforcing directories on {white}{target_url}{red}...")
        
        results = []
        threads = []
        
        for directory in directories:
            thread = threading.Thread(target=check_directory, args=(target_url, directory, results))
            threads.append(thread)
            thread.start()
            
            if len(threads) >= threads_number:
                for t in threads:
                    t.join()
                threads = []

        # Wait for remaining threads
        for t in threads:
            t.join()

        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Standard scan completed. Found {white}{len(results)}{red} directories.")
    
    if choice in ['2', '02', '4', '04']:
        # Custom wordlist scan
        wordlist_file = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Wordlist file path -> {reset}")
        
        if not os.path.exists(wordlist_file):
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Wordlist file not found")
            Continue()
            Reset()
        
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                custom_directories = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error reading wordlist: {white}{e}")
            Continue()
            Reset()
        
        try:
            threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 20) -> {reset}"))
        except:
            threads_number = 20
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning with custom wordlist ({white}{len(custom_directories)}{red} entries)...")
        
        custom_results = []
        threads = []
        
        for directory in custom_directories:
            thread = threading.Thread(target=check_directory, args=(target_url, directory, custom_results))
            threads.append(thread)
            thread.start()
            
            if len(threads) >= threads_number:
                for t in threads:
                    t.join()
                threads = []

        for t in threads:
            t.join()
        
        if 'results' not in locals():
            results = []
        results.extend(custom_results)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Custom wordlist scan completed. Found {white}{len(custom_results)}{red} additional directories.")
    
    if choice in ['3', '03']:
        # Generate custom wordlist
        keywords_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Keywords (space separated) -> {reset}")
        keywords = [word.strip() for word in keywords_input.split() if word.strip()]
        
        if not keywords:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No keywords provided")
            Continue()
            Reset()
        
        custom_dirs = generate_custom_wordlist(keywords)
        
        # Option to merge with external wordlists
        merge_external = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Merge with external wordlists? (y/n) -> {reset}")
        if merge_external.lower() in ['y', 'yes']:
            external_dirs = download_directory_wordlists()
            custom_dirs.extend(external_dirs)
            custom_dirs = list(set(custom_dirs))  # Remove duplicates
        
        # Save wordlist
        wordlist_file = os.path.join(tool_path, "1-Output", "Wordlists", f"directory_wordlist_{int(time.time())}.txt")
        os.makedirs(os.path.dirname(wordlist_file), exist_ok=True)
        
        with open(wordlist_file, 'w', encoding='utf-8') as f:
            f.write(f"# Custom Directory Wordlist\n")
            f.write(f"# Keywords: {', '.join(keywords)}\n")
            f.write(f"# External wordlists: {'Yes' if merge_external.lower() in ['y', 'yes'] else 'No'}\n")
            f.write(f"# Generated: {current_time_day_hour()}\n\n")
            for directory in custom_dirs:
                f.write(directory + '\n')
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Generated {white}{len(custom_dirs)}{red} directory combinations")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Wordlist saved to: {white}{wordlist_file}")
        
        # Option to scan with generated wordlist
        scan_now = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan with generated wordlist? (y/n) -> {reset}")
        if scan_now.lower() in ['y', 'yes']:
            try:
                threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 20) -> {reset}"))
            except:
                threads_number = 20
            
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning with generated wordlist...")
            
            results = []
            threads = []
            
            for directory in custom_dirs:
                thread = threading.Thread(target=check_directory, args=(target_url, directory, results))
                threads.append(thread)
                thread.start()
                
                if len(threads) >= threads_number:
                    for t in threads:
                        t.join()
                    threads = []

            for t in threads:
                t.join()
        else:
            Continue()
            Reset()
    
    if 'results' in locals() and results:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Total directories found: {white}{len(results)}")
        
        # Categorize results by status code
        status_categories = {}
        for result in results:
            status = result['status']
            if status not in status_categories:
                status_categories[status] = []
            status_categories[status].append(result)
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Results by status code:")
        for status, status_results in sorted(status_categories.items()):
            color_code = green if status == 200 else yellow if status in [301, 302] else red
            print(f"  {color_code}[{status}]{red}: {white}{len(status_results)}{red} directories")
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Detailed results:")
        for result in sorted(results, key=lambda x: x['status']):
            status_color = green if result['status'] == 200 else yellow if result['status'] in [301, 302] else red
            print(f"  {white}{result['url']}{red} {status_color}[{result['status']}]{red} {result['size']} bytes")
        
        # Save results
        report_file = os.path.join(tool_path, "1-Output", "DirectoryBruteforce", f"directory_scan_{int(time.time())}.txt")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Directory Bruteforce Report\n")
            f.write(f"# Target: {target_url}\n")
            f.write(f"# Date: {current_time_day_hour()}\n")
            f.write(f"# Total Found: {len(results)}\n\n")
            
            for result in sorted(results, key=lambda x: x['status']):
                f.write(f"{result['url']} [{result['status']}] {result['size']} bytes\n")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Results saved to: {white}{report_file}")

    Continue()
    Reset()
except Exception as e:
    Error(e)