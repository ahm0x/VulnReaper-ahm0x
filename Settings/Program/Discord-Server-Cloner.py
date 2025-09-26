from Config.Util import *
from Config.Config import *
try:
    import requests
    import json
    import time
    import asyncio
    import discord
    from discord.ext import commands
except Exception as e:
    ErrorModule(e)

Title("Discord Server Cloner")

try:
    Slow(discord_banner)
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Server Structure Cloning Tool")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {yellow}Educational purposes - Clone your own servers only")
    
    def get_server_structure(token, guild_id):
        """Get complete server structure"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            
            # Get guild info
            guild_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}', headers=headers, timeout=10)
            if guild_response.status_code != 200:
                return None
            
            guild_data = guild_response.json()
            
            # Get channels
            channels_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers, timeout=10)
            channels_data = channels_response.json() if channels_response.status_code == 200 else []
            
            # Get roles
            roles_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers, timeout=10)
            roles_data = roles_response.json() if roles_response.status_code == 200 else []
            
            # Get emojis
            emojis_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers=headers, timeout=10)
            emojis_data = emojis_response.json() if emojis_response.status_code == 200 else []
            
            return {
                'guild': guild_data,
                'channels': channels_data,
                'roles': roles_data,
                'emojis': emojis_data
            }
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error getting server structure: {white}{e}")
            return None

    def clone_server_structure(bot_token, target_guild_id, structure):
        """Clone server structure using bot"""
        try:
            intents = discord.Intents.default()
            intents.guilds = True
            intents.members = True
            
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            @bot.event
            async def on_ready():
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Bot connected: {white}{bot.user}")
                
                # Find target guild
                target_guild = bot.get_guild(int(target_guild_id))
                if not target_guild:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Target guild not found")
                    await bot.close()
                    return
                
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Cloning to guild: {white}{target_guild.name}")
                
                # Clone roles (excluding @everyone)
                role_mapping = {}
                for role_data in structure['roles']:
                    if role_data['name'] != '@everyone':
                        try:
                            new_role = await target_guild.create_role(
                                name=role_data['name'],
                                permissions=discord.Permissions(role_data['permissions']),
                                color=discord.Color(role_data['color']),
                                hoist=role_data['hoist'],
                                mentionable=role_data['mentionable']
                            )
                            role_mapping[role_data['id']] = new_role.id
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Role created: {white}{role_data['name']}")
                            await asyncio.sleep(1)  # Rate limit protection
                        except Exception as e:
                            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to create role {role_data['name']}: {white}{e}")
                
                # Clone categories and channels
                category_mapping = {}
                for channel_data in structure['channels']:
                    try:
                        if channel_data['type'] == 4:  # Category
                            new_category = await target_guild.create_category(
                                name=channel_data['name'],
                                position=channel_data['position']
                            )
                            category_mapping[channel_data['id']] = new_category.id
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Category created: {white}{channel_data['name']}")
                            
                        elif channel_data['type'] == 0:  # Text channel
                            category = None
                            if channel_data.get('parent_id') and channel_data['parent_id'] in category_mapping:
                                category = bot.get_channel(category_mapping[channel_data['parent_id']])
                            
                            new_channel = await target_guild.create_text_channel(
                                name=channel_data['name'],
                                category=category,
                                topic=channel_data.get('topic', ''),
                                position=channel_data['position']
                            )
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Text channel created: {white}{channel_data['name']}")
                            
                        elif channel_data['type'] == 2:  # Voice channel
                            category = None
                            if channel_data.get('parent_id') and channel_data['parent_id'] in category_mapping:
                                category = bot.get_channel(category_mapping[channel_data['parent_id']])
                            
                            new_channel = await target_guild.create_voice_channel(
                                name=channel_data['name'],
                                category=category,
                                bitrate=channel_data.get('bitrate', 64000),
                                user_limit=channel_data.get('user_limit', 0),
                                position=channel_data['position']
                            )
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Voice channel created: {white}{channel_data['name']}")
                        
                        await asyncio.sleep(0.5)  # Rate limit protection
                        
                    except Exception as e:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to create channel {channel_data['name']}: {white}{e}")
                
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Server cloning completed")
                await bot.close()
            
            bot.run(bot_token)
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error during cloning: {white}{e}")

    def save_server_template(structure, server_name):
        """Save server structure as template"""
        try:
            template_file = os.path.join(tool_path, "1-Output", "ServerTemplates", f"{server_name}_template.json")
            os.makedirs(os.path.dirname(template_file), exist_ok=True)
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(structure, f, indent=2, ensure_ascii=False)
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Template saved: {white}{template_file}")
            return template_file
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error saving template: {white}{e}")
            return None

    print(f"""
 {BEFORE}01{AFTER}{white} Analyze server structure
 {BEFORE}02{AFTER}{white} Clone server structure
 {BEFORE}03{AFTER}{white} Save server template
 {BEFORE}04{AFTER}{white} Load and apply template
    """)
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Option -> {reset}")
    
    if choice in ['1', '01']:
        guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Server ID to analyze -> {reset}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Analyzing server structure...")
        structure = get_server_structure(token, guild_id)
        
        if structure:
            guild_info = structure['guild']
            print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} Server Analysis:
    Name: {white}{guild_info['name']}
    ID: {white}{guild_info['id']}
    Owner ID: {white}{guild_info.get('owner_id', 'Unknown')}
    Member Count: {white}{guild_info.get('approximate_member_count', 'Unknown')}
    Channels: {white}{len(structure['channels'])}
    Roles: {white}{len(structure['roles'])}
    Emojis: {white}{len(structure['emojis'])}""")
            
            # Show channel breakdown
            text_channels = [c for c in structure['channels'] if c['type'] == 0]
            voice_channels = [c for c in structure['channels'] if c['type'] == 2]
            categories = [c for c in structure['channels'] if c['type'] == 4]
            
            print(f"""
    Channel Breakdown:
        Categories: {white}{len(categories)}
        Text Channels: {white}{len(text_channels)}
        Voice Channels: {white}{len(voice_channels)}""")
    
    elif choice in ['2', '02']:
        source_guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Source server ID -> {reset}")
        target_guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target server ID -> {reset}")
        bot_token = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Bot token (with admin permissions) -> {reset}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Getting source server structure...")
        structure = get_server_structure(token, source_guild_id)
        
        if structure:
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Starting cloning process...")
            clone_server_structure(bot_token, target_guild_id, structure)
    
    elif choice in ['3', '03']:
        guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Server ID to save as template -> {reset}")
        template_name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Template name -> {reset}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Creating server template...")
        structure = get_server_structure(token, guild_id)
        
        if structure:
            template_file = save_server_template(structure, template_name)
            if template_file:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Template created successfully")
    
    elif choice in ['4', '04']:
        template_file = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Template file path -> {reset}")
        target_guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target server ID -> {reset}")
        bot_token = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Bot token -> {reset}")
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                structure = json.load(f)
            
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Applying template...")
            clone_server_structure(bot_token, target_guild_id, structure)
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error loading template: {white}{e}")
    
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)