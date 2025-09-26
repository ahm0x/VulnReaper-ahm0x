#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VulnReaper by ahm0x - Professional Cybersecurity Framework
Version: v1.0
Author: ahm0x
Website: https://ahm0x.github.io/
GitHub: https://github.com/ahm0x/VulnReaper
License: GPL-3.0

Professional Bug Bounty & Penetration Testing Framework
79 Advanced Cybersecurity Modules | Real-time API Integration
"""

import os
import sys
import time

# Add the Settings/Program directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
settings_dir = os.path.join(current_dir, "Settings", "Program")
sys.path.insert(0, settings_dir)

try:
    from Config.Config import *
    from Config.Util import *
except ImportError as e:
    print(f"Error importing configuration: {e}")
    print("Please ensure all required files are present and run Setup.py first.")
    sys.exit(1)

def display_banner():
    """Display the main VulnReaper banner"""
    banner = f"""
{MainColor2('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡠⠶⡶⠀⠉⠉⠋⠛⠒⠉⠈⠀⠈⠉⠉⠋⠉⠉⠀⠒⠂⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠠⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢤⡲⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⡀⠠⢀⠀⠠⠀⠄⡀⢂⠀⡀⠁⡐⡂⢀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡾⠞⠁⠀⠀⠀⢀⠀⢀⡈⠠⣤⡴⢷⣴⠾⣴⣫⡾⠽⠮⠿⠾⠶⡍⣶⣶⣄⣹⣀⡇⣤⡘⣖⣞⣢⢸⣌⡀⠢⠄⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⡶⠛⢁⠀⠀⠀⠀⠀⡀⠀⣀⠈⡁⠄⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠈⠉⠉⠉⠀⠒⠒⠒⠫⠭⠍⢙⣛⡚⠯⠷⢯⣻⣦⠻⡴⣆⡀⢒⠀⠙⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣺⡼⢀⣪⡤⠴⠛⠊⠩⠐⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠐⠂⠭⠭⠓⡛⠧⢗⣄⠄⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⣝⡞⠋⣉⡀⠠⣤⡠⣤⠤⢤⣤⣀⣀⣀⣀⠀⠀⠀⠀⢀⣀⣀⣀⣀⢀⣀⣀⣀⡀⠀⠀⡀⠠⠀⠤⠤⠤⠤⠂⠐⠦⠒⣒⣢⣤⣤⣀⣠⢍⢐⣒⠉⢀⠨⡢⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠝⣿⢾⣻⣭⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣴⣲⣤⣰⣒⢢⣤⣀⡀⠀⠌⠙⠁⠢⠙⠭⢿⣯⡿⣶⣄⡙⠵⡀⢀⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢿⣿⣷⣿⣾⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣷⣾⣿⣿⣾⣾⣷⣾⣧⣤⣴⣤⣭⣍⣁⠛⢛⣿⣷⠏⢹⠦⠡⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡿⠛⠉⠙⣿⣿⣿⣷⣿⣾⣻⢷⣯⣷⢿⣻⢿⣻⢿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⠃⢀⣀⠻⠲⣧
''')}

    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                      ║
    ║                        {red}⚡ VulnReaper by ahm0x v1.0 ⚡{white}                           ║
    ║                                                                                      ║
    ║                    {yellow}Professional Bug Bounty & Penetration Testing{white}                ║
    ║                              {yellow}Framework with 79 Modules{white}                         ║
    ║                                                                                      ║
    ║  {green}🎯 Real-time API Integration  🔍 Advanced OSINT  🛡️ Enterprise Reporting{white}     ║
    ║                                                                                      ║
    ║  {blue}Website:{white} https://ahm0x.github.io/                                           ║
    ║  {blue}GitHub:{white}  https://github.com/ahm0x/VulnReaper                              ║
    ║  {blue}Telegram:{white} https://t.me/ahm0x                                              ║
    ║                                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    return banner

def display_main_menu():
    """Display the main menu options"""
    menu = f"""
    {red}╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                                {white}🛠️  MAIN MENU  🛠️{red}                                ║
    ╠══════════════════════════════════════════════════════════════════════════════════════╣
    ║                                                                                      ║
    ║  {BEFORE}01{AFTER}{white} 🎯 Bug Bounty Automation     {BEFORE}11{AFTER}{white} 🔐 Hash & Crypto Tools        ║
    ║  {BEFORE}02{AFTER}{white} 🔍 OSINT Framework           {BEFORE}12{AFTER}{white} 📱 Discord Security Suite     ║
    ║  {BEFORE}03{AFTER}{white} 🌐 Web Application Security  {BEFORE}13{AFTER}{white} 🎮 Gaming Platform Tools      ║
    ║  {BEFORE}04{AFTER}{white} 🌍 Network Analysis          {BEFORE}14{AFTER}{white} 🔬 Digital Forensics          ║
    ║  {BEFORE}05{AFTER}{white} 🔧 Exploit Development       {BEFORE}15{AFTER}{white} 📊 Reporting & Documentation  ║
    ║                                                                                      ║
    ║  {BEFORE}88{AFTER}{white} ℹ️  Tool Information         {BEFORE}99{AFTER}{white} 🌐 Open Web Interface         ║
    ║  {BEFORE}00{AFTER}{white} 🚪 Exit Framework                                                    ║
    ║                                                                                      ║
    {red}╚══════════════════════════════════════════════════════════════════════════════════════╝{white}
    """
    return menu

def main():
    """Main application entry point"""
    try:
        # Clear screen and set title
        Clear()
        Title("VulnReaper by ahm0x - Main Menu")
        
        # Display banner and menu
        print(display_banner())
        print(display_main_menu())
        
        # Get user choice
        choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Select option -> {reset}")
        
        # Handle menu choices
        if choice in ['01', '1']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Bug Bounty Automation...")
            StartProgram("VulnReaper-by-ahm0x.py")
            
        elif choice in ['02', '2']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading OSINT Framework...")
            StartProgram("OSINT-Framework.py")
            
        elif choice in ['03', '3']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Web Security Tools...")
            StartProgram("Website-Vulnerability-Scanner.py")
            
        elif choice in ['04', '4']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Network Analysis...")
            StartProgram("Network-Scanner.py")
            
        elif choice in ['05', '5']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Exploit Development...")
            StartProgram("Exploit-Database-Search.py")
            
        elif choice in ['11']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Hash & Crypto Tools...")
            StartProgram("Hash-Cracker.py")
            
        elif choice in ['12']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Discord Security Suite...")
            StartProgram("Discord-Token-Info.py")
            
        elif choice in ['13']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Gaming Platform Tools...")
            StartProgram("Roblox-User-Info.py")
            
        elif choice in ['14']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Digital Forensics...")
            StartProgram("Forensics-Analyzer.py")
            
        elif choice in ['88']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Loading Tool Information...")
            StartProgram("Info.py")
            
        elif choice in ['99']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Opening Web Interface...")
            try:
                import webbrowser
                webbrowser.open('http://localhost:3000')
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Web interface opened in browser")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error opening web interface: {white}{e}")
            Continue()
            main()
            
        elif choice in ['00', '0']:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Thank you for using VulnReaper by ahm0x!")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Visit: {white}{website}")
            sys.exit(0)
            
        else:
            ErrorChoiceStart()
            time.sleep(1)
            main()
            
    except KeyboardInterrupt:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Framework interrupted by user")
        sys.exit(0)
    except Exception as e:
        Error(e)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)