from Config.Util import *
from Config.Config import *
try:
    import requests
    import json
    import threading
    import time
except Exception as e:
    ErrorModule(e)

Title("Roblox Group Scanner")

try:
    def get_group_info(group_id):
        """Get detailed information about a Roblox group"""
        try:
            # Get basic group info
            response = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}", timeout=10)
            if response.status_code != 200:
                return None
            
            group_data = response.json()
            
            # Get additional info
            try:
                roles_response = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}/roles", timeout=10)
                roles_data = roles_response.json() if roles_response.status_code == 200 else {}
            except:
                roles_data = {}
            
            try:
                members_response = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100", timeout=10)
                members_data = members_response.json() if members_response.status_code == 200 else {}
            except:
                members_data = {}
            
            group_info = {
                'id': group_data.get('id'),
                'name': group_data.get('name'),
                'description': group_data.get('description', ''),
                'owner': group_data.get('owner', {}).get('username', 'None') if group_data.get('owner') else 'None',
                'owner_id': group_data.get('owner', {}).get('userId', 'None') if group_data.get('owner') else 'None',
                'member_count': group_data.get('memberCount', 0),
                'is_builders_club_only': group_data.get('isBuildersClubOnly', False),
                'public_entry_allowed': group_data.get('publicEntryAllowed', False),
                'is_locked': group_data.get('isLocked', False),
                'has_verified_badge': group_data.get('hasVerifiedBadge', False),
                'roles': roles_data.get('roles', []),
                'recent_members': members_data.get('data', [])
            }
            
            return group_info
        except Exception as e:
            return None

    def scan_group_vulnerabilities(group_info):
        """Scan for potential group vulnerabilities"""
        vulnerabilities = []
        
        # Check for open groups
        if group_info['public_entry_allowed']:
            vulnerabilities.append({
                'type': 'Open Group',
                'severity': 'Medium',
                'description': 'Group allows public entry without approval'
            })
        
        # Check for groups without owners
        if group_info['owner'] == 'None':
            vulnerabilities.append({
                'type': 'Ownerless Group',
                'severity': 'High',
                'description': 'Group has no owner, potentially claimable'
            })
        
        # Check for suspicious descriptions
        suspicious_keywords = ['free', 'robux', 'hack', 'cheat', 'exploit', 'script', 'bot']
        description_lower = group_info['description'].lower()
        
        for keyword in suspicious_keywords:
            if keyword in description_lower:
                vulnerabilities.append({
                    'type': 'Suspicious Content',
                    'severity': 'Low',
                    'description': f'Description contains suspicious keyword: {keyword}'
                })
                break
        
        # Check for high-privilege roles with many members
        for role in group_info['roles']:
            if role.get('rank', 0) >= 100 and 'admin' in role.get('name', '').lower():
                vulnerabilities.append({
                    'type': 'High Privilege Role',
                    'severity': 'Medium',
                    'description': f'Role "{role["name"]}" has high privileges'
                })
        
        return vulnerabilities

    def scan_multiple_groups(start_id, end_id, threads=10):
        """Scan multiple groups in a range"""
        results = []
        scanned = 0
        found = 0
        
        def scan_group_range(group_ids):
            nonlocal scanned, found
            for group_id in group_ids:
                scanned += 1
                group_info = get_group_info(group_id)
                
                if group_info:
                    found += 1
                    vulnerabilities = scan_group_vulnerabilities(group_info)
                    
                    result = {
                        'group_info': group_info,
                        'vulnerabilities': vulnerabilities
                    }
                    results.append(result)
                    
                    vuln_count = len(vulnerabilities)
                    vuln_color = red if vuln_count > 0 else green
                    
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Group {white}{group_id}{green}: {group_info['name']} {vuln_color}({vuln_count} issues)")
                    
                    if vulnerabilities:
                        for vuln in vulnerabilities:
                            severity_color = red if vuln['severity'] == 'High' else yellow if vuln['severity'] == 'Medium' else white
                            print(f"    {severity_color}[{vuln['severity']}]{red} {vuln['type']}: {vuln['description']}")
                
                if scanned % 50 == 0:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Progress: {white}{scanned}{red} scanned, {white}{found}{red} found")
        
        # Split range into chunks for threading
        group_range = list(range(start_id, end_id + 1))
        chunk_size = len(group_range) // threads
        chunks = [group_range[i:i + chunk_size] for i in range(0, len(group_range), chunk_size)]
        
        thread_list = []
        for chunk in chunks:
            if chunk:  # Only create thread if chunk is not empty
                t = threading.Thread(target=scan_group_range, args=(chunk,))
                t.start()
                thread_list.append(t)
        
        for t in thread_list:
            t.join()
        
        return results

    print(f"""
 {BEFORE}01{AFTER}{white} Scan single group
 {BEFORE}02{AFTER}{white} Scan group range
 {BEFORE}03{AFTER}{white} Search groups by keyword
 {BEFORE}04{AFTER}{white} Vulnerability assessment
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Scan type -> {reset}")
    
    if choice in ['1', '01']:
        try:
            group_id = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Group ID -> {reset}"))
        except:
            ErrorId()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning group {white}{group_id}{red}...")
        
        group_info = get_group_info(group_id)
        if group_info:
            vulnerabilities = scan_group_vulnerabilities(group_info)
            
            print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} Group Information:
    Name: {white}{group_info['name']}{red}
    ID: {white}{group_info['id']}{red}
    Owner: {white}{group_info['owner']}{red} (ID: {group_info['owner_id']})
    Members: {white}{group_info['member_count']}{red}
    Public Entry: {white}{group_info['public_entry_allowed']}{red}
    Builders Club Only: {white}{group_info['is_builders_club_only']}{red}
    Locked: {white}{group_info['is_locked']}{red}
    Verified: {white}{group_info['has_verified_badge']}{red}
    Roles: {white}{len(group_info['roles'])}{red}
            """)
            
            if group_info['description']:
                print(f"    Description: {white}{group_info['description'][:100]}{'...' if len(group_info['description']) > 100 else ''}")
            
            if vulnerabilities:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Security Issues Found:")
                for vuln in vulnerabilities:
                    severity_color = red if vuln['severity'] == 'High' else yellow if vuln['severity'] == 'Medium' else white
                    print(f"    {severity_color}[{vuln['severity']}]{red} {vuln['type']}: {vuln['description']}")
            else:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} No security issues detected")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Group not found or private")
    
    elif choice in ['2', '02']:
        try:
            start_id = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Start group ID -> {reset}"))
            end_id = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} End group ID -> {reset}"))
            threads = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (recommended: 10) -> {reset}"))
        except:
            ErrorNumber()
        
        if end_id - start_id > 10000:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Warning: Large range detected, this may take a long time")
            confirm = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Continue? (y/n) -> {reset}")
            if confirm.lower() not in ['y', 'yes']:
                Continue()
                Reset()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning groups {white}{start_id}{red} to {white}{end_id}{red}...")
        
        results = scan_multiple_groups(start_id, end_id, threads)
        
        # Generate report
        report_file = os.path.join(tool_path, "1-Output", "RobloxGroups", f"group_scan_{start_id}_{end_id}.txt")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Roblox Group Scan Report\n")
            f.write(f"# Range: {start_id} - {end_id}\n")
            f.write(f"# Date: {current_time_day_hour()}\n")
            f.write(f"# Groups Found: {len(results)}\n\n")
            
            for result in results:
                group = result['group_info']
                vulns = result['vulnerabilities']
                
                f.write(f"Group ID: {group['id']}\n")
                f.write(f"Name: {group['name']}\n")
                f.write(f"Owner: {group['owner']} (ID: {group['owner_id']})\n")
                f.write(f"Members: {group['member_count']}\n")
                f.write(f"Public Entry: {group['public_entry_allowed']}\n")
                
                if vulns:
                    f.write(f"Vulnerabilities:\n")
                    for vuln in vulns:
                        f.write(f"  - [{vuln['severity']}] {vuln['type']}: {vuln['description']}\n")
                
                f.write("\n" + "-" * 50 + "\n\n")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Report saved to: {white}{report_file}")
    
    elif choice in ['3', '03']:
        keyword = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Search keyword -> {reset}")
        Censored(keyword)
        
        # Simulate group search (in real scenario, use Roblox search API)
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching groups with keyword: {white}{keyword}")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Use Roblox website search: {white}https://www.roblox.com/search/groups?keyword={keyword}")
        
        open_search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open search in browser? (y/n) -> {reset}")
        if open_search.lower() in ['y', 'yes']:
            webbrowser.open(f"https://www.roblox.com/search/groups?keyword={keyword}")
    
    elif choice in ['4', '04']:
        try:
            group_id = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Group ID for vulnerability assessment -> {reset}"))
        except:
            ErrorId()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Performing vulnerability assessment...")
        
        group_info = get_group_info(group_id)
        if group_info:
            vulnerabilities = scan_group_vulnerabilities(group_info)
            
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Vulnerability Assessment for: {white}{group_info['name']}")
            
            if vulnerabilities:
                high_risk = [v for v in vulnerabilities if v['severity'] == 'High']
                medium_risk = [v for v in vulnerabilities if v['severity'] == 'Medium']
                low_risk = [v for v in vulnerabilities if v['severity'] == 'Low']
                
                print(f"    High Risk Issues: {white}{len(high_risk)}")
                print(f"    Medium Risk Issues: {white}{len(medium_risk)}")
                print(f"    Low Risk Issues: {white}{len(low_risk)}")
                
                for vuln in vulnerabilities:
                    severity_color = red if vuln['severity'] == 'High' else yellow if vuln['severity'] == 'Medium' else white
                    print(f"    {severity_color}[{vuln['severity']}]{red} {vuln['type']}: {vuln['description']}")
            else:
                print(f"    {green}No security issues detected")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Group not found")
    
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)