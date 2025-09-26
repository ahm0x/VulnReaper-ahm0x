#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - Error Handler
Centralized error handling and logging
"""

import traceback
import logging
import os
import sys
from datetime import datetime
from Config.Util import *
from Config.Config import *

class VulnReaperErrorHandler:
    """Centralized error handling system"""
    
    def __init__(self):
        self.setup_logging()
        self.error_count = 0
        self.warning_count = 0
    
    def setup_logging(self):
        """Setup logging configuration"""
        try:
            log_dir = os.path.join(tool_path, "1-Output", "Logs")
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, f"vulnreaper_{datetime.now().strftime('%Y%m%d')}.log")
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler(sys.stdout)
                ]
            )
            
            self.logger = logging.getLogger('VulnReaper')
            
        except Exception as e:
            print(f"Failed to setup logging: {e}")
            self.logger = None
    
    def log_error(self, error, context="", severity="ERROR"):
        """Log error with context"""
        self.error_count += 1
        
        error_msg = f"[{severity}] {context}: {str(error)}"
        
        if self.logger:
            if severity == "CRITICAL":
                self.logger.critical(error_msg)
            elif severity == "ERROR":
                self.logger.error(error_msg)
            elif severity == "WARNING":
                self.logger.warning(error_msg)
            else:
                self.logger.info(error_msg)
        
        # Also print to console with colors
        if severity == "CRITICAL":
            print(f"{BEFORE + current_time_hour() + AFTER} {red}CRITICAL{reset} {error_msg}")
        elif severity == "ERROR":
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {error_msg}")
        elif severity == "WARNING":
            print(f"{BEFORE + current_time_hour() + AFTER} {yellow}WARNING{reset} {error_msg}")
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Global exception handler"""
        if issubclass(exc_type, KeyboardInterrupt):
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Operation interrupted by user")
            return
        
        error_msg = f"Unhandled exception: {exc_type.__name__}: {exc_value}"
        traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        self.log_error(error_msg, "UNHANDLED_EXCEPTION", "CRITICAL")
        
        if self.logger:
            self.logger.critical(f"Traceback:\n{traceback_str}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Critical error occurred. Check logs for details.")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Please report this issue to: {github_tool}/issues")
    
    def validate_dependencies(self):
        """Validate that all required dependencies are installed"""
        required_modules = [
            'requests', 'beautifulsoup4', 'dnspython', 'cryptography',
            'colorama', 'phonenumbers', 'python-whois', 'lxml'
        ]
        
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module.replace('-', '_'))
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Missing required modules:")
            for module in missing_modules:
                print(f"  - {white}{module}")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Install with: {white}pip install {' '.join(missing_modules)}")
            return False
        
        return True
    
    def check_system_requirements(self):
        """Check system requirements"""
        issues = []
        
        # Check Python version
        if sys.version_info < (3, 8):
            issues.append(f"Python 3.8+ required (current: {sys.version.split()[0]})")
        
        # Check available disk space
        try:
            import shutil
            free_space = shutil.disk_usage(tool_path).free
            if free_space < 100 * 1024 * 1024:  # 100MB
                issues.append("Low disk space (less than 100MB available)")
        except:
            pass
        
        # Check write permissions
        try:
            test_file = os.path.join(tool_path, "1-Output", "test_write.tmp")
            os.makedirs(os.path.dirname(test_file), exist_ok=True)
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except:
            issues.append("No write permission in output directory")
        
        if issues:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} System requirement issues:")
            for issue in issues:
                print(f"  - {white}{issue}")
            return False
        
        return True
    
    def get_error_statistics(self):
        """Get error statistics"""
        return {
            'total_errors': self.error_count,
            'total_warnings': self.warning_count,
            'log_file': os.path.join(tool_path, "1-Output", "Logs", f"vulnreaper_{datetime.now().strftime('%Y%m%d')}.log")
        }

# Global error handler instance
error_handler = VulnReaperErrorHandler()

# Set global exception handler
sys.excepthook = error_handler.handle_exception