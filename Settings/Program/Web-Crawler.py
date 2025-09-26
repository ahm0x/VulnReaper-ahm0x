from Config.Util import *
from Config.Config import *
try:
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse
    import re
    import threading
    import time
    from collections import deque
except Exception as e:
    ErrorModule(e)

Title("Advanced Web Crawler")

try:
    def extract_links(url, html_content, domain_filter=None):
        """Extract all links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        # Extract from various tags
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'form']):
            for attr in ['href', 'src', 'action']:
                link = tag.get(attr)
                if link:
                    full_url = urljoin(url, link)
                    if domain_filter and domain_filter not in full_url:
                        continue
                    links.add(full_url)
        
        # Extract from JavaScript
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for URLs in JavaScript
                js_urls = re.findall(r'["\']https?://[^"\']+["\']', script.string)
                for js_url in js_urls:
                    clean_url = js_url.strip('"\'')
                    if domain_filter and domain_filter not in clean_url:
                        continue
                    links.add(clean_url)
        
        return links

    def extract_sensitive_data(html_content, url):
        """Extract potentially sensitive information"""
        sensitive_data = {
            'emails': set(),
            'phone_numbers': set(),
            'api_keys': set(),
            'comments': set(),
            'forms': [],
            'javascript_vars': set()
        }
        
        # Email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html_content)
        sensitive_data['emails'].update(emails)
        
        # Phone numbers
        phones = re.findall(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', html_content)
        sensitive_data['phone_numbers'].update(phones)
        
        # API keys patterns
        api_patterns = [
            r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'secret[_-]?key["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'access[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'auth[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            sensitive_data['api_keys'].update(matches)
        
        # HTML comments
        soup = BeautifulSoup(html_content, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--'))
        sensitive_data['comments'].update([comment.strip() for comment in comments])
        
        # Forms
        forms = soup.find_all('form')
        for form in forms:
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET'),
                'inputs': []
            }
            
            inputs = form.find_all(['input', 'textarea', 'select'])
            for inp in inputs:
                form_data['inputs'].append({
                    'name': inp.get('name', ''),
                    'type': inp.get('type', 'text'),
                    'value': inp.get('value', '')
                })
            
            sensitive_data['forms'].append(form_data)
        
        # JavaScript variables
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for variable declarations
                js_vars = re.findall(r'var\s+(\w+)\s*=\s*["\']([^"\']+)["\']', script.string)
                for var_name, var_value in js_vars:
                    if any(keyword in var_name.lower() for keyword in ['key', 'token', 'secret', 'pass']):
                        sensitive_data['javascript_vars'].add(f"{var_name}: {var_value}")
        
        return sensitive_data

    def crawl_website(start_url, max_depth=3, max_pages=100, same_domain_only=True):
        """Crawl website and extract information"""
        visited = set()
        to_visit = deque([(start_url, 0)])  # (url, depth)
        results = {
            'pages': [],
            'sensitive_data': {
                'emails': set(),
                'phone_numbers': set(),
                'api_keys': set(),
                'comments': set(),
                'forms': [],
                'javascript_vars': set()
            },
            'external_links': set(),
            'broken_links': set()
        }
        
        domain = urlparse(start_url).netloc
        pages_crawled = 0
        
        while to_visit and pages_crawled < max_pages:
            current_url, depth = to_visit.popleft()
            
            if current_url in visited or depth > max_depth:
                continue
            
            try:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Crawling: {white}{current_url}{red} (depth: {depth})")
                
                response = requests.get(current_url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200:
                    visited.add(current_url)
                    pages_crawled += 1
                    
                    # Extract sensitive data
                    page_sensitive = extract_sensitive_data(response.text, current_url)
                    
                    # Merge sensitive data
                    for key in results['sensitive_data']:
                        if isinstance(results['sensitive_data'][key], set):
                            results['sensitive_data'][key].update(page_sensitive[key])
                        elif isinstance(results['sensitive_data'][key], list):
                            results['sensitive_data'][key].extend(page_sensitive[key])
                    
                    # Extract links for further crawling
                    if depth < max_depth:
                        page_links = extract_links(current_url, response.text, domain if same_domain_only else None)
                        
                        for link in page_links:
                            if link not in visited:
                                link_domain = urlparse(link).netloc
                                if same_domain_only and link_domain != domain:
                                    results['external_links'].add(link)
                                else:
                                    to_visit.append((link, depth + 1))
                    
                    # Store page info
                    page_info = {
                        'url': current_url,
                        'title': BeautifulSoup(response.text, 'html.parser').title.string if BeautifulSoup(response.text, 'html.parser').title else 'No Title',
                        'status_code': response.status_code,
                        'size': len(response.content),
                        'depth': depth
                    }
                    results['pages'].append(page_info)
                    
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Crawled: {white}{current_url}{green} [{response.status_code}]")
                
                else:
                    results['broken_links'].add(current_url)
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Broken link: {white}{current_url}{red} [{response.status_code}]")
                
                time.sleep(0.1)  # Be respectful to the server
                
            except Exception as e:
                results['broken_links'].add(current_url)
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error crawling {white}{current_url}{red}: {e}")
        
        return results

    Slow(scan_banner)
    
    start_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target URL -> {reset}")
    Censored(start_url)
    
    if not start_url.startswith(('http://', 'https://')):
        start_url = 'https://' + start_url
    
    try:
        max_depth = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Max depth (recommended: 2-3) -> {reset}"))
    except:
        max_depth = 2
    
    try:
        max_pages = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Max pages (recommended: 50-200) -> {reset}"))
    except:
        max_pages = 100
    
    same_domain = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Stay on same domain? (y/n) -> {reset}")
    same_domain_only = same_domain.lower() in ['y', 'yes']
    
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting web crawl...")
    
    results = crawl_website(start_url, max_depth, max_pages, same_domain_only)
    
    # Generate report
    report_file = os.path.join(tool_path, "1-Output", "WebCrawler", f"crawl_report_{urlparse(start_url).netloc}_{int(time.time())}.txt")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# Web Crawler Report\n")
        f.write(f"# Target: {start_url}\n")
        f.write(f"# Date: {current_time_day_hour()}\n")
        f.write(f"# Pages Crawled: {len(results['pages'])}\n")
        f.write(f"# Max Depth: {max_depth}\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("CRAWLED PAGES\n")
        f.write("=" * 80 + "\n")
        for page in results['pages']:
            f.write(f"URL: {page['url']}\n")
            f.write(f"Title: {page['title']}\n")
            f.write(f"Status: {page['status_code']}\n")
            f.write(f"Size: {page['size']} bytes\n")
            f.write(f"Depth: {page['depth']}\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("SENSITIVE DATA FOUND\n")
        f.write("=" * 80 + "\n")
        
        if results['sensitive_data']['emails']:
            f.write("EMAILS:\n")
            for email in results['sensitive_data']['emails']:
                f.write(f"  - {email}\n")
            f.write("\n")
        
        if results['sensitive_data']['phone_numbers']:
            f.write("PHONE NUMBERS:\n")
            for phone in results['sensitive_data']['phone_numbers']:
                f.write(f"  - {phone}\n")
            f.write("\n")
        
        if results['sensitive_data']['api_keys']:
            f.write("POTENTIAL API KEYS:\n")
            for key in results['sensitive_data']['api_keys']:
                f.write(f"  - {key}\n")
            f.write("\n")
        
        if results['sensitive_data']['forms']:
            f.write("FORMS FOUND:\n")
            for i, form in enumerate(results['sensitive_data']['forms'], 1):
                f.write(f"  Form {i}:\n")
                f.write(f"    Action: {form['action']}\n")
                f.write(f"    Method: {form['method']}\n")
                f.write(f"    Inputs: {len(form['inputs'])}\n")
                for inp in form['inputs']:
                    f.write(f"      - {inp['name']} ({inp['type']})\n")
                f.write("\n")
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Crawl Summary:")
    print(f"  Pages crawled: {white}{len(results['pages'])}")
    print(f"  Emails found: {white}{len(results['sensitive_data']['emails'])}")
    print(f"  Phone numbers: {white}{len(results['sensitive_data']['phone_numbers'])}")
    print(f"  Potential API keys: {white}{len(results['sensitive_data']['api_keys'])}")
    print(f"  Forms found: {white}{len(results['sensitive_data']['forms'])}")
    print(f"  External links: {white}{len(results['external_links'])}")
    print(f"  Broken links: {white}{len(results['broken_links'])}")
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Report saved to: {white}{report_file}")

    Continue()
    Reset()
except Exception as e:
    Error(e)