#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - API Security Scanner
Advanced API endpoint discovery and security testing
"""

from Config.Util import *
from Config.Config import *
from Config.Security import *

try:
    import requests
    import json
    import re
    from urllib.parse import urljoin, urlparse
    from bs4 import BeautifulSoup
    import threading
    import time
except Exception as e:
    ErrorModule(e)

Title("API Security Scanner")

try:
    def discover_api_endpoints(base_url):
        """Discover API endpoints through various methods"""
        endpoints = set()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Discovering API endpoints...")
        
        # Common API paths
        common_api_paths = [
            '/api', '/api/v1', '/api/v2', '/api/v3', '/rest', '/graphql',
            '/swagger', '/swagger.json', '/swagger.yaml', '/swagger-ui',
            '/openapi.json', '/openapi.yaml', '/docs', '/redoc',
            '/api-docs', '/api/docs', '/api/documentation',
            '/v1', '/v2', '/v3', '/v4', '/version',
            '/health', '/status', '/ping', '/info', '/metrics',
            '/admin/api', '/api/admin', '/internal/api', '/private/api',
            '/dev/api', '/test/api', '/staging/api', '/beta/api'
        ]
        
        # Test common API paths
        for path in common_api_paths:
            test_url = urljoin(base_url, path)
            try:
                response = secure_session.safe_get(test_url)
                if response and response.status_code in [200, 401, 403]:
                    endpoints.add(test_url)
                    status_color = green if response.status_code == 200 else yellow
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} API endpoint: {white}{test_url}{status_color} [{response.status_code}]")
            except:
                pass
        
        # Parse main page for API references
        try:
            response = secure_session.safe_get(base_url)
            if response and response.status_code == 200:
                content = response.text
                
                # Look for API URLs in JavaScript
                api_patterns = [
                    r'["\']([^"\']*api[^"\']*)["\']',
                    r'["\']([^"\']*rest[^"\']*)["\']',
                    r'["\']([^"\']*graphql[^"\']*)["\']',
                    r'fetch\s*\(\s*["\']([^"\']+)["\']',
                    r'axios\.[get|post|put|delete]+\s*\(\s*["\']([^"\']+)["\']',
                    r'\.ajax\s*\(\s*["\']([^"\']+)["\']'
                ]
                
                for pattern in api_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if '/api' in match.lower() or '/rest' in match.lower():
                            full_url = urljoin(base_url, match)
                            endpoints.add(full_url)
                            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Found in JS: {white}{full_url}")
        except:
            pass
        
        return list(endpoints)

    def test_api_authentication(endpoint):
        """Test API authentication mechanisms"""
        auth_tests = []
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing authentication for: {white}{endpoint}")
        
        # Test without authentication
        try:
            response = secure_session.safe_get(endpoint)
            if response:
                auth_tests.append({
                    'method': 'No Authentication',
                    'status_code': response.status_code,
                    'accessible': response.status_code == 200
                })
        except:
            pass
        
        # Test with common API keys
        common_keys = ['test', 'demo', 'api_key', 'key', 'token', 'admin', 'guest']
        
        for key in common_keys:
            try:
                # Test as query parameter
                response = secure_session.safe_get(f"{endpoint}?api_key={key}")
                if response and response.status_code == 200:
                    auth_tests.append({
                        'method': f'API Key (query): {key}',
                        'status_code': response.status_code,
                        'accessible': True
                    })
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Weak API key: {white}{key}")
                
                # Test as header
                headers = {'X-API-Key': key, 'Authorization': f'Bearer {key}'}
                response = secure_session.safe_get(endpoint, headers=headers)
                if response and response.status_code == 200:
                    auth_tests.append({
                        'method': f'API Key (header): {key}',
                        'status_code': response.status_code,
                        'accessible': True
                    })
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Weak API key header: {white}{key}")
            except:
                pass
        
        return auth_tests

    def test_api_methods(endpoint):
        """Test different HTTP methods on API endpoint"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
        method_results = []
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing HTTP methods...")
        
        for method in methods:
            try:
                if method == 'GET':
                    response = secure_session.safe_get(endpoint)
                elif method == 'POST':
                    response = secure_session.safe_post(endpoint, json={})
                elif method == 'OPTIONS':
                    response = requests.options(endpoint, timeout=10)
                else:
                    response = requests.request(method, endpoint, timeout=10)
                
                if response:
                    method_results.append({
                        'method': method,
                        'status_code': response.status_code,
                        'allowed': response.status_code not in [405, 501]
                    })
                    
                    if response.status_code not in [405, 501]:
                        status_color = green if response.status_code < 400 else yellow
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} {method}: {status_color}{response.status_code}")
                        
                        # Check for interesting headers
                        if method == 'OPTIONS' and 'Allow' in response.headers:
                            allowed_methods = response.headers['Allow']
                            print(f"    Allowed methods: {white}{allowed_methods}")
            except:
                pass
        
        return method_results

    def test_api_injection(endpoint):
        """Test for injection vulnerabilities in API"""
        injection_tests = []
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing for injection vulnerabilities...")
        
        # SQL injection payloads
        sql_payloads = [
            "' OR '1'='1", "' OR 1=1--", "'; DROP TABLE test--",
            "' UNION SELECT NULL--", "admin'--", "' OR 'a'='a"
        ]
        
        # NoSQL injection payloads
        nosql_payloads = [
            '{"$ne": null}', '{"$gt": ""}', '{"$regex": ".*"}',
            '{"$where": "this.username == this.password"}',
            '{"username": {"$ne": null}, "password": {"$ne": null}}'
        ]
        
        # Command injection payloads
        command_payloads = [
            '; ls', '| whoami', '& dir', '; cat /etc/passwd',
            '`id`', '$(whoami)', '; ping -c 1 127.0.0.1'
        ]
        
        # Test SQL injection
        for payload in sql_payloads:
            try:
                test_data = {'id': payload, 'search': payload, 'query': payload}
                response = secure_session.safe_post(endpoint, json=test_data)
                
                if response:
                    # Check for SQL error indicators
                    sql_errors = ['SQL syntax', 'mysql_fetch', 'ORA-01756', 'SQLite', 'PostgreSQL']
                    for error in sql_errors:
                        if error.lower() in response.text.lower():
                            injection_tests.append({
                                'type': 'SQL Injection',
                                'payload': payload,
                                'evidence': error
                            })
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} SQL Injection: {white}{error}")
                            break
            except:
                pass
        
        # Test NoSQL injection
        for payload in nosql_payloads:
            try:
                response = secure_session.safe_post(endpoint, 
                                                  json={'query': payload},
                                                  headers={'Content-Type': 'application/json'})
                
                if response and response.status_code == 200:
                    # Check response size or content changes
                    if len(response.text) > 1000:  # Unusually large response
                        injection_tests.append({
                            'type': 'NoSQL Injection',
                            'payload': payload,
                            'evidence': 'Large response size'
                        })
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Possible NoSQL injection")
            except:
                pass
        
        return injection_tests

    def test_api_security_headers(endpoint):
        """Test API security headers"""
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Checking security headers...")
        
        try:
            response = secure_session.safe_get(endpoint)
            if not response:
                return []
            
            headers = response.headers
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=',
                'Content-Security-Policy': 'default-src',
                'X-API-Version': None,
                'Access-Control-Allow-Origin': '*'
            }
            
            header_results = []
            
            for header, expected in security_headers.items():
                if header in headers:
                    value = headers[header]
                    
                    if header == 'Access-Control-Allow-Origin' and value == '*':
                        header_results.append({
                            'header': header,
                            'value': value,
                            'status': 'Vulnerable',
                            'issue': 'Overly permissive CORS policy'
                        })
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} CORS misconfiguration: {white}{value}")
                    else:
                        header_results.append({
                            'header': header,
                            'value': value,
                            'status': 'Present'
                        })
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {header}: {white}{value}")
                else:
                    header_results.append({
                        'header': header,
                        'value': None,
                        'status': 'Missing'
                    })
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Missing header: {white}{header}")
            
            return header_results
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Header check failed: {white}{e}")
            return []

    def test_api_rate_limiting(endpoint):
        """Test API rate limiting"""
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing rate limiting...")
        
        try:
            requests_made = 0
            rate_limited = False
            
            for i in range(20):  # Make 20 rapid requests
                response = secure_session.safe_get(endpoint)
                requests_made += 1
                
                if response:
                    if response.status_code == 429:  # Too Many Requests
                        rate_limited = True
                        print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Rate limiting active after {white}{requests_made}{green} requests")
                        break
                    elif response.status_code >= 500:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Server error at request {white}{requests_made}")
                        break
                
                time.sleep(0.1)  # Small delay
            
            if not rate_limited:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No rate limiting detected after {white}{requests_made}{red} requests")
                return False
            
            return True
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Rate limiting test failed: {white}{e}")
            return False

    def generate_api_security_report(base_url, endpoints, test_results):
        """Generate comprehensive API security report"""
        report_file = os.path.join(tool_path, "1-Output", "APIScanner", f"api_security_{urlparse(base_url).netloc}_{int(time.time())}.txt")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(generate_report_header("API Security Scanner", base_url, "API Security Assessment"))
            
            f.write(f"TARGET ANALYSIS\n")
            f.write(f"Base URL: [REDACTED]\n")
            f.write(f"Endpoints Discovered: {len(endpoints)}\n")
            f.write(f"Scan Date: {current_time_day_hour()}\n\n")
            
            f.write("DISCOVERED ENDPOINTS\n")
            f.write("="*50 + "\n")
            for endpoint in sorted(endpoints):
                f.write(f"• {endpoint}\n")
            
            f.write(f"\nSECURITY TEST RESULTS\n")
            f.write("="*50 + "\n")
            
            for endpoint, results in test_results.items():
                f.write(f"\nEndpoint: {endpoint}\n")
                f.write("-" * 40 + "\n")
                
                if 'auth_tests' in results:
                    f.write("Authentication Tests:\n")
                    for auth_test in results['auth_tests']:
                        f.write(f"  • {auth_test['method']}: {auth_test['status_code']}\n")
                
                if 'method_tests' in results:
                    f.write("HTTP Methods:\n")
                    for method_test in results['method_tests']:
                        if method_test['allowed']:
                            f.write(f"  • {method_test['method']}: {method_test['status_code']}\n")
                
                if 'injection_tests' in results:
                    f.write("Injection Vulnerabilities:\n")
                    for injection in results['injection_tests']:
                        f.write(f"  • {injection['type']}: {injection['evidence']}\n")
                
                if 'security_headers' in results:
                    f.write("Security Headers:\n")
                    for header in results['security_headers']:
                        status = header['status']
                        if status == 'Missing':
                            f.write(f"  ⚠ Missing: {header['header']}\n")
                        elif status == 'Vulnerable':
                            f.write(f"  🚨 Vulnerable: {header['header']} = {header['value']}\n")
                        else:
                            f.write(f"  ✓ Present: {header['header']}\n")
            
            f.write(f"\nRECOMMENDATIONS\n")
            f.write("="*50 + "\n")
            f.write("1. Implement proper authentication and authorization\n")
            f.write("2. Add rate limiting to prevent abuse\n")
            f.write("3. Validate and sanitize all input data\n")
            f.write("4. Implement proper error handling\n")
            f.write("5. Add security headers (CORS, CSP, etc.)\n")
            f.write("6. Use HTTPS for all API communications\n")
            f.write("7. Implement API versioning and deprecation policies\n")
            f.write("8. Add comprehensive logging and monitoring\n")
        
        return report_file

    # Main execution
    Slow(f"""{scan_banner}
 {BEFORE}01{AFTER}{white} Discover API endpoints
 {BEFORE}02{AFTER}{white} Test API authentication
 {BEFORE}03{AFTER}{white} Test API security
 {BEFORE}04{AFTER}{white} Comprehensive API assessment
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    target_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target URL -> {reset}")
    
    # Validate and sanitize URL
    is_valid, message = security.validate_url(target_url)
    if not is_valid:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {message}")
        Continue()
        Reset()
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    Censored(target_url)
    
    if choice in ['1', '01', '4', '04']:
        # Discover API endpoints
        endpoints = discover_api_endpoints(target_url)
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Discovered {white}{len(endpoints)}{red} API endpoints")
    
    if choice in ['2', '02', '4', '04']:
        # Test authentication
        if 'endpoints' not in locals():
            endpoints = [target_url]
        
        for endpoint in endpoints[:5]:  # Limit to first 5 endpoints
            auth_results = test_api_authentication(endpoint)
    
    if choice in ['3', '03', '4', '04']:
        # Test API security
        if 'endpoints' not in locals():
            endpoints = [target_url]
        
        test_results = {}
        
        for endpoint in endpoints[:3]:  # Limit to first 3 endpoints
            print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Testing security for: {white}{endpoint}")
            
            endpoint_results = {}
            
            # Authentication tests
            endpoint_results['auth_tests'] = test_api_authentication(endpoint)
            
            # HTTP method tests
            endpoint_results['method_tests'] = test_api_methods(endpoint)
            
            # Injection tests
            endpoint_results['injection_tests'] = test_api_injection(endpoint)
            
            # Security headers
            endpoint_results['security_headers'] = test_api_security_headers(endpoint)
            
            # Rate limiting
            endpoint_results['rate_limiting'] = test_api_rate_limiting(endpoint)
            
            test_results[endpoint] = endpoint_results
    
    if choice in ['4', '04']:
        # Generate comprehensive report
        if 'endpoints' in locals() and 'test_results' in locals():
            report_file = generate_api_security_report(target_url, endpoints, test_results)
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Comprehensive report saved: {white}{report_file}")

    Continue()
    Reset()

except Exception as e:
    Error(e)