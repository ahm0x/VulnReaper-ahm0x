#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - API Manager
Centralized API management and rate limiting
"""

import requests
import time
import json
import hashlib
from datetime import datetime, timedelta
from Config.Util import *
from Config.Config import *

class APIManager:
    """Centralized API management with rate limiting and caching"""
    
    def __init__(self):
        self.rate_limits = {}
        self.cache = {}
        self.cache_duration = 3600  # 1 hour default cache
        
        # API endpoints configuration
        self.apis = {
            'shodan': {
                'base_url': 'https://api.shodan.io',
                'rate_limit': 1,  # requests per second
                'requires_key': True
            },
            'virustotal': {
                'base_url': 'https://www.virustotal.com/vtapi/v2',
                'rate_limit': 4,  # requests per minute
                'requires_key': True
            },
            'nvd': {
                'base_url': 'https://services.nvd.nist.gov/rest/json/cves/2.0',
                'rate_limit': 5,  # requests per second
                'requires_key': False
            },
            'crtsh': {
                'base_url': 'https://crt.sh',
                'rate_limit': 10,  # requests per second
                'requires_key': False
            },
            'ipinfo': {
                'base_url': 'https://ipinfo.io',
                'rate_limit': 50,  # requests per day for free tier
                'requires_key': False
            },
            'hackertarget': {
                'base_url': 'https://api.hackertarget.com',
                'rate_limit': 2,  # requests per second
                'requires_key': False
            }
        }
    
    def check_rate_limit(self, api_name):
        """Check if API call is within rate limits"""
        current_time = time.time()
        
        if api_name not in self.rate_limits:
            self.rate_limits[api_name] = []
        
        # Clean old entries
        api_config = self.apis.get(api_name, {})
        rate_limit = api_config.get('rate_limit', 1)
        
        # Remove entries older than 1 second (for per-second limits)
        self.rate_limits[api_name] = [
            timestamp for timestamp in self.rate_limits[api_name]
            if current_time - timestamp < 1
        ]
        
        # Check if we can make the request
        if len(self.rate_limits[api_name]) >= rate_limit:
            return False
        
        # Add current request
        self.rate_limits[api_name].append(current_time)
        return True
    
    def get_cache_key(self, api_name, endpoint, params):
        """Generate cache key for API request"""
        cache_string = f"{api_name}:{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get_cached_response(self, cache_key):
        """Get cached API response if valid"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['data']
        return None
    
    def cache_response(self, cache_key, data):
        """Cache API response"""
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def make_api_request(self, api_name, endpoint, params=None, method='GET', use_cache=True):
        """Make API request with rate limiting and caching"""
        if params is None:
            params = {}
        
        # Check cache first
        if use_cache:
            cache_key = self.get_cache_key(api_name, endpoint, params)
            cached_response = self.get_cached_response(cache_key)
            if cached_response:
                return cached_response
        
        # Check rate limits
        if not self.check_rate_limit(api_name):
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Rate limit reached for {api_name}, waiting...")
            time.sleep(1)
            return self.make_api_request(api_name, endpoint, params, method, use_cache)
        
        # Make request
        try:
            api_config = self.apis.get(api_name, {})
            base_url = api_config.get('base_url', '')
            
            if not base_url:
                return None
            
            url = f"{base_url}/{endpoint.lstrip('/')}"
            
            headers = {
                'User-Agent': f'{name_tool} {version_tool} (Professional Security Scanner)',
                'Accept': 'application/json',
            }
            
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=params, headers=headers, timeout=10)
            else:
                return None
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Cache successful response
                    if use_cache:
                        self.cache_response(cache_key, data)
                    
                    return data
                except json.JSONDecodeError:
                    return response.text
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} API {api_name} returned {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} API request failed: {white}{e}")
            return None
    
    def search_cve_database(self, service, version=""):
        """Search CVE database for vulnerabilities"""
        try:
            params = {
                'keywordSearch': f"{service} {version}".strip(),
                'resultsPerPage': 20
            }
            
            data = self.make_api_request('nvd', 'cves', params)
            
            if data and 'vulnerabilities' in data:
                cves = []
                for vuln in data['vulnerabilities']:
                    cve_data = vuln.get('cve', {})
                    cve_id = cve_data.get('id', '')
                    
                    # Get CVSS score
                    cvss_score = "Unknown"
                    severity = "Unknown"
                    
                    metrics = cve_data.get('metrics', {})
                    if 'cvssMetricV31' in metrics and metrics['cvssMetricV31']:
                        cvss_data = metrics['cvssMetricV31'][0]['cvssData']
                        cvss_score = cvss_data.get('baseScore', 'Unknown')
                        severity = cvss_data.get('baseSeverity', 'Unknown')
                    
                    # Get description
                    descriptions = cve_data.get('descriptions', [])
                    description = "No description available"
                    for desc in descriptions:
                        if desc.get('lang') == 'en':
                            description = desc.get('value', 'No description available')
                            break
                    
                    cves.append({
                        'id': cve_id,
                        'score': cvss_score,
                        'severity': severity,
                        'description': description[:200] + '...' if len(description) > 200 else description
                    })
                
                return cves
            
            return []
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} CVE search failed: {white}{e}")
            return []
    
    def get_ip_intelligence(self, ip_address):
        """Get IP intelligence information"""
        try:
            data = self.make_api_request('ipinfo', f'{ip_address}/json')
            
            if data:
                return {
                    'ip': data.get('ip'),
                    'hostname': data.get('hostname'),
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country': data.get('country'),
                    'location': data.get('loc'),
                    'organization': data.get('org'),
                    'postal': data.get('postal'),
                    'timezone': data.get('timezone')
                }
            
            return None
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} IP intelligence failed: {white}{e}")
            return None
    
    def search_certificate_transparency(self, domain):
        """Search Certificate Transparency logs"""
        try:
            params = {
                'q': f'%.{domain}',
                'output': 'json'
            }
            
            data = self.make_api_request('crtsh', '', params)
            
            if data:
                subdomains = set()
                for entry in data:
                    name_value = entry.get('name_value', '')
                    for subdomain in name_value.split('\n'):
                        subdomain = subdomain.strip()
                        if subdomain and subdomain.endswith(domain):
                            subdomains.add(subdomain)
                
                return list(subdomains)
            
            return []
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} CT search failed: {white}{e}")
            return []
    
    def get_subdomain_enumeration(self, domain):
        """Get subdomains using HackerTarget API"""
        try:
            data = self.make_api_request('hackertarget', f'hostsearch/?q={domain}')
            
            if data and isinstance(data, str):
                subdomains = []
                for line in data.split('\n'):
                    if ',' in line:
                        subdomain = line.split(',')[0].strip()
                        if subdomain and subdomain.endswith(domain):
                            subdomains.append(subdomain)
                
                return subdomains
            
            return []
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Subdomain enumeration failed: {white}{e}")
            return []
    
    def cleanup_cache(self):
        """Clean up expired cache entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, data in self.cache.items():
            if current_time - data['timestamp'] > self.cache_duration:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
    
    def get_api_status(self):
        """Get status of all APIs"""
        status = {}
        
        for api_name, config in self.apis.items():
            try:
                # Make a simple test request
                response = requests.get(config['base_url'], timeout=5)
                status[api_name] = {
                    'status': 'Online' if response.status_code < 500 else 'Error',
                    'response_time': response.elapsed.total_seconds(),
                    'rate_limit_remaining': config['rate_limit'] - len(self.rate_limits.get(api_name, []))
                }
            except:
                status[api_name] = {
                    'status': 'Offline',
                    'response_time': 0,
                    'rate_limit_remaining': 0
                }
        
        return status

# Global API manager instance
api_manager = APIManager()