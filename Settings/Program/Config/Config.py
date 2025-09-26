import os
import sys

# Tool Information
name_tool = "VulnReaper by ahm0x"
version_tool = "v1.0"
type_tool = "Cybersecurity Framework"
copyright = "Copyright (c) 2025 ahm0x"
coding_tool = "Python"
language_tool = f"Python {sys.version.split()[0]}"
creator = "ahm0x"
platform = "Windows | Linux"

# URLs and Links
website = "https://ahm0x.github.io/"
github_tool = "https://github.com/ahm0x/VulnReaper"
telegram = "https://t.me/ahm0x"
discord_server = "https://discord.gg/ZqpqmRXR"

# Paths
tool_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# API Configuration
api_config = {
    'timeout': 10,
    'max_retries': 3,
    'rate_limit_delay': 1,
    'user_agent': f'{name_tool} {version_tool} (Professional Security Scanner)'
}

# Security Configuration
security_config = {
    'max_threads': 100,
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'allowed_file_types': ['.txt', '.json', '.csv', '.xml', '.html'],
    'max_scan_targets': 1000,
    'session_timeout': 3600  # 1 hour
}

# Webhook Configuration
color_webhook = 0xa80505
username_webhook = name_tool
avatar_webhook = 'https://cdn.discordapp.com/attachments/1218378256617705554/1325085753864359968/mango_icono.jpg'

# Version and update information
version_info = {
    'current_version': version_tool,
    'release_date': '2025-01-01',
    'update_url': f'{github_tool}/releases/latest',
    'changelog_url': f'{github_tool}/blob/main/CHANGELOG.md'
}