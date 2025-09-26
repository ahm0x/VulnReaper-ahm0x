#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - Database Module
Secure database operations and data management
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from Config.Util import *
from Config.Config import *

class VulnReaperDB:
    """VulnReaper database management class"""
    
    def __init__(self):
        self.db_path = os.path.join(tool_path, "1-Output", "Database", "vulnreaper.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Scan results table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scan_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_hash TEXT NOT NULL,
                        scan_type TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        subdomains_count INTEGER DEFAULT 0,
                        live_hosts_count INTEGER DEFAULT 0,
                        open_ports_count INTEGER DEFAULT 0,
                        vulnerabilities_count INTEGER DEFAULT 0,
                        report_path TEXT,
                        scan_duration REAL
                    )
                ''')
                
                # Vulnerabilities table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS vulnerabilities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scan_id INTEGER,
                        vulnerability_type TEXT NOT NULL,
                        severity TEXT DEFAULT 'Medium',
                        description TEXT,
                        affected_service TEXT,
                        port INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (scan_id) REFERENCES scan_results (id)
                    )
                ''')
                
                # Discovered hosts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS discovered_hosts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scan_id INTEGER,
                        hostname TEXT NOT NULL,
                        ip_address TEXT,
                        is_alive BOOLEAN DEFAULT 0,
                        response_time REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (scan_id) REFERENCES scan_results (id)
                    )
                ''')
                
                # Open ports table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS open_ports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scan_id INTEGER,
                        host_id INTEGER,
                        port INTEGER NOT NULL,
                        service_name TEXT,
                        service_version TEXT,
                        banner TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (scan_id) REFERENCES scan_results (id),
                        FOREIGN KEY (host_id) REFERENCES discovered_hosts (id)
                    )
                ''')
                
                # Activity logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS activity_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        activity_type TEXT NOT NULL,
                        target_hash TEXT,
                        description TEXT,
                        user_agent TEXT,
                        ip_address TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Database initialization failed: {white}{e}")
    
    def hash_target(self, target):
        """Create hash of target for privacy"""
        return hashlib.sha256(target.encode()).hexdigest()[:16]
    
    def save_scan_result(self, target, scan_type, subdomains_count=0, live_hosts_count=0, 
                        open_ports_count=0, vulnerabilities_count=0, report_path="", scan_duration=0):
        """Save scan results to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                target_hash = self.hash_target(target)
                
                cursor.execute('''
                    INSERT INTO scan_results 
                    (target_hash, scan_type, subdomains_count, live_hosts_count, 
                     open_ports_count, vulnerabilities_count, report_path, scan_duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (target_hash, scan_type, subdomains_count, live_hosts_count,
                      open_ports_count, vulnerabilities_count, report_path, scan_duration))
                
                scan_id = cursor.lastrowid
                conn.commit()
                return scan_id
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to save scan result: {white}{e}")
            return None
    
    def save_vulnerability(self, scan_id, vuln_type, severity, description, affected_service="", port=None):
        """Save vulnerability to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO vulnerabilities 
                    (scan_id, vulnerability_type, severity, description, affected_service, port)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (scan_id, vuln_type, severity, description, affected_service, port))
                
                conn.commit()
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to save vulnerability: {white}{e}")
    
    def get_scan_history(self, limit=10):
        """Get recent scan history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT target_hash, scan_type, timestamp, subdomains_count, 
                           live_hosts_count, open_ports_count, vulnerabilities_count
                    FROM scan_results 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                return cursor.fetchall()
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to get scan history: {white}{e}")
            return []
    
    def get_vulnerability_stats(self):
        """Get vulnerability statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT severity, COUNT(*) as count
                    FROM vulnerabilities 
                    GROUP BY severity
                    ORDER BY 
                        CASE severity 
                            WHEN 'Critical' THEN 1
                            WHEN 'High' THEN 2
                            WHEN 'Medium' THEN 3
                            WHEN 'Low' THEN 4
                            ELSE 5
                        END
                ''')
                
                return cursor.fetchall()
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to get vulnerability stats: {white}{e}")
            return []
    
    def log_activity(self, activity_type, target="", description="", user_agent="", ip_address=""):
        """Log activity to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                target_hash = self.hash_target(target) if target else ""
                
                cursor.execute('''
                    INSERT INTO activity_logs 
                    (activity_type, target_hash, description, user_agent, ip_address)
                    VALUES (?, ?, ?, ?, ?)
                ''', (activity_type, target_hash, description, user_agent, ip_address))
                
                conn.commit()
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to log activity: {white}{e}")

# Global database instance
vulnreaper_db = VulnReaperDB()