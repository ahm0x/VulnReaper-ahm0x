
from Config.Util import *
from Config.Config import *
try:
    import webbrowser
except Exception as e:
   ErrorModule(e)

Title("Info")

try:
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Information Recovery..{reset}")

    Slow(f"""
    {INFO_ADD} Name Tool     :  {white}{name_tool}
    {INFO_ADD} Type Tool     :  {white}{type_tool}
    {INFO_ADD} Version       :  {white}{version_tool}
    {INFO_ADD} Copyright     :  {white}{copyright}
    {INFO_ADD} Coding        :  {white}{coding_tool}
    {INFO_ADD} Language      :  {white}{language_tool}
    {INFO_ADD} Creator       :  {white}{creator}
    {INFO_ADD} Platform      :  {white}{platform}
    {INFO_ADD} Website  [W]  :  {white}{website}
    {INFO_ADD} GitHub   [W]  :  {white}{github_tool}
    {INFO_ADD} Telegram [W]  :  {white}{telegram}
    {reset}""")

    print(f"""
 {BEFORE}01{AFTER}{white} Website
 {BEFORE}02{AFTER}{white} GitHub
 {BEFORE}03{AFTER}{white} Telegram
    """)
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open link -> {reset}")
    if choice in ['1', '01']:
        webbrowser.open_new_tab(website)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Opening website: {white}{website}")
    elif choice in ['2', '02']:
        webbrowser.open_new_tab(github_tool)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Opening GitHub: {white}{github_tool}")
    elif choice in ['3', '03']:
        webbrowser.open_new_tab(telegram)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Opening Telegram: {white}{telegram}")
    else:
        ErrorChoice()
    
    Continue()
    Reset()
except Exception as e:
    Error(e)