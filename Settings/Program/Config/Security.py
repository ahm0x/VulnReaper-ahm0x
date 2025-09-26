#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - Security Module
Enhanced security functions and validations
"""

import hashlib
import hmac
import secrets
import base64
import re
import time
from datetime import datetime, timedelta
import ipaddress
import socket
import ssl
import requests
from urllib.parse import urlparse

class SecurityValidator:
    """Security validation and sanitization class"""
    
    @staticmethod
    def sanitize_input(user_input, max_length=1000):
        """Sanitize user input to prevent injection attacks"""
        if not isinstance(user_input, str):
            return str(user_input)
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', user_input)
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'eval\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\(',
            r'passthru\s*\(',
            r'file_get_contents\s*\(',
            r'file_put_contents\s*\(',
            r'fopen\s*\(',
            r'fwrite\s*\(',
            r'include\s*\(',
            r'require\s*\(',
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def validate_url(url):
        """Validate URL format and security"""
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False, "Invalid URL scheme"
            
            # Check hostname
            if not parsed.netloc:
                return False, "Missing hostname"
            
            # Check for localhost/private IPs in production
            hostname = parsed.hostname
            if hostname:
                try:
                    ip = socket.gethostbyname(hostname)
                    ip_obj = ipaddress.ip_address(ip)
                    if ip_obj.is_private and not ip_obj.is_loopback:
                        return True, "Private IP detected"  # Allow but warn
                except:
                    pass
            
            return True, "Valid URL"
        except Exception as e:
            return False, f"URL validation error: {e}"
    
    @staticmethod
    def validate_ip_address(ip):
        """Validate IP address"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return True, f"Valid {ip_obj.version} address"
        except ValueError:
            return False, "Invalid IP address format"
    
    @staticmethod
    def validate_domain(domain):
        """Validate domain name"""
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        
        if not domain or len(domain) > 253:
            return False, "Invalid domain length"
        
        if domain_pattern.match(domain):
            return True, "Valid domain"
        else:
            return False, "Invalid domain format"
    
    @staticmethod
    def validate_port(port):
        """Validate port number"""
        try:
            port_num = int(port)
            if 1 <= port_num <= 65535:
                return True, "Valid port"
            else:
                return False, "Port out of range (1-65535)"
        except ValueError:
            return False, "Invalid port format"
    
    @staticmethod
    def check_rate_limit(identifier, max_requests=100, time_window=3600):
        """Simple rate limiting check"""
        # In a real implementation, this would use a database or cache
        # For now, we'll use a simple file-based approach
        try:
            rate_limit_file = f"/tmp/rate_limit_{hashlib.md5(identifier.encode()).hexdigest()}.txt"
            current_time = time.time()
            
            if os.path.exists(rate_limit_file):
                with open(rate_limit_file, 'r') as f:
                    data = json.loads(f.read())
                
                # Clean old entries
                data['requests'] = [req_time for req_time in data['requests'] 
                                  if current_time - req_time < time_window]
                
                if len(data['requests']) >= max_requests:
                    return False, "Rate limit exceeded"
                
                data['requests'].append(current_time)
            else:
                data = {'requests': [current_time]}
            
            with open(rate_limit_file, 'w') as f:
                f.write(json.dumps(data))
            
            return True, "Within rate limit"
        except:
            return True, "Rate limit check failed, allowing request"

class SecureSession:
    """Secure session management"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'VulnReaper-Security-Scanner/1.0 (Educational-Research)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Configure SSL verification
        self.session.verify = True
        
        # Set timeouts
        self.default_timeout = 10
    
    def safe_get(self, url, **kwargs):
        """Make safe GET request"""
        kwargs.setdefault('timeout', self.default_timeout)
        kwargs.setdefault('allow_redirects', True)
        
        try:
            return self.session.get(url, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def safe_post(self, url, **kwargs):
        """Make safe POST request"""
        kwargs.setdefault('timeout', self.default_timeout)
        
        try:
            return self.session.post(url, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

class CryptoUtils:
    """Cryptographic utilities"""
    
    @staticmethod
    def generate_secure_token(length=32):
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_data(data, algorithm='sha256'):
        """Hash data with specified algorithm"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if algorithm == 'md5':
            return hashlib.md5(data).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(data).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def verify_hash(data, expected_hash, algorithm='sha256'):
        """Verify data against hash"""
        calculated_hash = CryptoUtils.hash_data(data, algorithm)
        return hmac.compare_digest(calculated_hash, expected_hash)

class NetworkSecurity:
    """Network security utilities"""
    
    @staticmethod
    def is_safe_target(target):
        """Check if target is safe to scan"""
        try:
            # Parse target
            if target.startswith(('http://', 'https://')):
                parsed = urlparse(target)
                hostname = parsed.hostname
            else:
                hostname = target
            
            # Resolve to IP
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)
            
            # Check for dangerous targets
            dangerous_ranges = [
                ipaddress.ip_network('127.0.0.0/8'),    # Localhost
                ipaddress.ip_network('169.254.0.0/16'), # Link-local
                ipaddress.ip_network('224.0.0.0/4'),    # Multicast
            ]
            
            for dangerous_range in dangerous_ranges:
                if ip_obj in dangerous_range:
                    return False, f"Target in restricted range: {dangerous_range}"
            
            # Check for government/military domains
            dangerous_domains = [
                '.gov', '.mil', '.edu', '.bank',
                'government', 'military', 'pentagon',
                'whitehouse', 'fbi', 'cia', 'nsa'
            ]
            
            for dangerous in dangerous_domains:
                if dangerous in hostname.lower():
                    return False, f"Restricted domain detected: {dangerous}"
            
            return True, "Target appears safe"
            
        except Exception as e:
            return False, f"Target validation error: {e}"
    
    @staticmethod
    def check_ssl_certificate(hostname, port=443):
        """Check SSL certificate information"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'san': cert.get('subjectAltName', [])
                    }
        except Exception as e:
            return None

# Global security instance
security = SecurityValidator()
secure_session = SecureSession()
crypto_utils = CryptoUtils()
network_security = NetworkSecurity()