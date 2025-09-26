from Config.Util import *
from Config.Config import *
try:
    import itertools
    import requests
    import os
    from datetime import datetime
    import random
    import string
except Exception as e:
    ErrorModule(e)

Title("Wordlist Generator")

try:
    def generate_combinations(keywords, min_length=1, max_length=4):
        """Generate all possible combinations of keywords"""
        combinations = []
        
        # Single words
        combinations.extend(keywords)
        
        # Combinations of 2 words
        if max_length >= 2:
            for combo in itertools.combinations(keywords, 2):
                combinations.append(''.join(combo))
                combinations.append('_'.join(combo))
                combinations.append('-'.join(combo))
                combinations.append('.'.join(combo))
                # Reverse order
                combinations.append(''.join(reversed(combo)))
                combinations.append('_'.join(reversed(combo)))
                combinations.append('-'.join(reversed(combo)))
        
        # Combinations of 3 words
        if max_length >= 3:
            for combo in itertools.combinations(keywords, 3):
                combinations.append(''.join(combo))
                combinations.append('_'.join(combo))
                combinations.append('-'.join(combo))
                combinations.append('.'.join(combo))
        
        # Combinations of 4 words
        if max_length >= 4:
            for combo in itertools.combinations(keywords, 4):
                combinations.append(''.join(combo))
                combinations.append('_'.join(combo))
                combinations.append('-'.join(combo))
        
        return combinations

    def add_common_variations(base_words):
        """Add common variations like numbers, years, special chars"""
        variations = []
        common_numbers = ['1', '12', '123', '1234', '12345', '123456', '2024', '2025', '2023', '2022', '2021', '2020', '01', '02', '03', '00']
        common_suffixes = ['!', '@', '#', '$', '%', '&', '*', '123', '321', '01', '02', '03', '2024', '2025', 'admin', 'user', 'test']
        common_prefixes = ['admin', 'user', 'test', 'demo', 'guest', 'root', 'super', 'master', 'main', 'default']
        years = ['2020', '2021', '2022', '2023', '2024', '2025', '19', '20', '21', '22', '23', '24', '25']
        
        for word in base_words:
            variations.append(word)
            variations.append(word.upper())
            variations.append(word.lower())
            variations.append(word.capitalize())
            
            # Add numbers at the end
            for num in common_numbers:
                variations.append(word + num)
                variations.append(num + word)
            
            # Add years
            for year in years:
                variations.append(word + year)
                variations.append(year + word)
            
            # Add suffixes
            for suffix in common_suffixes:
                variations.append(word + suffix)
            
            # Add prefixes
            for prefix in common_prefixes:
                variations.append(prefix + word)
                variations.append(prefix + '_' + word)
                variations.append(prefix + '-' + word)
                variations.append(prefix + '.' + word)
            
            # Add common transformations
            variations.append(word[::-1])  # Reverse
            if len(word) > 3:
                variations.append(word[:-1])  # Remove last char
                variations.append(word[1:])   # Remove first char
        
        return list(set(variations))  # Remove duplicates

    def add_leet_speak_variations(words):
        """Add leet speak variations"""
        leet_map = {
            'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['5', '$'],
            't': ['7', '+'], 'l': ['1', '|'], 'g': ['9'], 'b': ['6'], 'z': ['2']
        }
        
        leet_variations = []
        
        for word in words[:50]:  # Limit to avoid explosion
            leet_word = word.lower()
            
            # Apply single character substitutions
            for char, replacements in leet_map.items():
                for replacement in replacements:
                    if char in leet_word:
                        leet_variations.append(leet_word.replace(char, replacement))
            
            # Apply multiple substitutions
            multi_leet = leet_word
            for char, replacements in leet_map.items():
                if char in multi_leet:
                    multi_leet = multi_leet.replace(char, replacements[0])
            
            if multi_leet != leet_word:
                leet_variations.append(multi_leet)
        
        return leet_variations

    def download_external_wordlists():
        """Download popular wordlists from online sources"""
        wordlists = {
            'rockyou_top1000': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt',
            'common_passwords': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt',
            'usernames': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt',
            'directories': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt',
            'subdomains': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt'
        }
        
        downloaded_words = []
        
        for name, url in wordlists.items():
            try:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Downloading {white}{name}{red}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    words = response.text.splitlines()
                    # Filter out comments and empty lines
                    words = [word.strip() for word in words if word.strip() and not word.startswith('#')]
                    downloaded_words.extend(words[:1000])  # Limit to avoid too large files
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Downloaded {white}{len(words)}{red} words from {name}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to download {name}")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error downloading {name}: {white}{e}")
        
        return downloaded_words

    def merge_with_common_wordlists(custom_words):
        """Merge with common password patterns"""
        common_passwords = [
            'password', 'admin', 'root', 'user', 'guest', 'test', 'demo',
            'login', 'pass', 'secret', 'default', 'master', 'super',
            'administrator', 'manager', 'service', 'support', 'backup',
            'temp', 'temporary', 'welcome', 'hello', 'world', 'system',
            'database', 'server', 'client', 'public', 'private', 'secure',
            'access', 'control', 'panel', 'config', 'configuration', 'settings',
            'qwerty', 'abc123', 'letmein', 'monkey', 'dragon', 'princess',
            'shadow', 'master', 'azerty', 'trustno1', 'sunshine', 'iloveyou'
        ]
        
        merged = custom_words.copy()
        
        # Add common passwords
        merged.extend(common_passwords)
        
        # Create combinations with common passwords
        for custom_word in custom_words[:15]:  # Limit to avoid explosion
            for common in common_passwords[:25]:
                merged.append(custom_word + common)
                merged.append(common + custom_word)
                merged.append(custom_word + '_' + common)
                merged.append(common + '_' + custom_word)
                merged.append(custom_word + '-' + common)
                merged.append(common + '-' + custom_word)
                merged.append(custom_word + '.' + common)
                merged.append(common + '.' + custom_word)
        
        return list(set(merged))

    def add_contextual_words(keywords, wordlist_type):
        """Add contextual words based on wordlist type"""
        context_words = {
            'passwords': [
                'password', 'pass', 'pwd', 'secret', 'key', 'login', 'auth',
                'secure', 'private', 'hidden', 'access', 'unlock', 'code'
            ],
            'usernames': [
                'admin', 'administrator', 'root', 'user', 'guest', 'test',
                'demo', 'service', 'system', 'operator', 'manager', 'support'
            ],
            'directories': [
                'admin', 'backup', 'config', 'data', 'files', 'images',
                'uploads', 'downloads', 'temp', 'cache', 'logs', 'api'
            ],
            'subdomains': [
                'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging',
                'api', 'blog', 'shop', 'secure', 'vpn', 'remote'
            ]
        }
        
        contextual = []
        if wordlist_type in context_words:
            contextual.extend(context_words[wordlist_type])
            
            # Combine keywords with contextual words
            for keyword in keywords:
                for context in context_words[wordlist_type]:
                    contextual.append(keyword + context)
                    contextual.append(context + keyword)
                    contextual.append(keyword + '_' + context)
                    contextual.append(context + '_' + keyword)
        
        return contextual

    def generate_advanced_patterns(keywords):
        """Generate advanced password patterns"""
        patterns = []
        
        # Common password patterns
        for keyword in keywords:
            # Capitalization patterns
            patterns.append(keyword.capitalize() + '123')
            patterns.append(keyword.capitalize() + '!')
            patterns.append(keyword.capitalize() + '@')
            patterns.append(keyword.upper() + '123')
            patterns.append(keyword.lower() + '123')
            
            # Date patterns
            patterns.append(keyword + '2024')
            patterns.append(keyword + '2025')
            patterns.append('2024' + keyword)
            patterns.append('2025' + keyword)
            
            # Special character patterns
            special_chars = ['!', '@', '#', '$', '%', '&', '*']
            for char in special_chars:
                patterns.append(keyword + char)
                patterns.append(char + keyword)
                patterns.append(keyword + char + '123')
                patterns.append(keyword + '123' + char)
            
            # Keyboard patterns
            patterns.append(keyword + 'qwerty')
            patterns.append('qwerty' + keyword)
            patterns.append(keyword + 'asdf')
            patterns.append(keyword + '1qaz')
            
            # Double patterns
            patterns.append(keyword + keyword)
            patterns.append(keyword + keyword.capitalize())
        
        return patterns

    Slow(f"""{virus_banner}
 {BEFORE}01{AFTER}{white} Generate custom wordlist
 {BEFORE}02{AFTER}{white} Generate with external wordlists
 {BEFORE}03{AFTER}{white} Advanced wordlist generation
 {BEFORE}04{AFTER}{white} Contextual wordlist (passwords/usernames/directories)
 {BEFORE}05{AFTER}{white} Pattern-based generation
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Generation type -> {reset}")
    
    if choice not in ['1', '01', '2', '02', '3', '03', '4', '04', '5', '05']:
        ErrorChoice()

    # Get keywords from user
    keywords_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Keywords (separated by space) -> {reset}")
    keywords = [word.strip() for word in keywords_input.split() if word.strip()]
    
    if not keywords:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No keywords provided")
        Continue()
        Reset()

    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Base keywords: {white}{', '.join(keywords)}")

    # Generate wordlist based on choice
    if choice in ['1', '01']:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Generating basic combinations...")
        wordlist = generate_combinations(keywords)
        wordlist = add_common_variations(wordlist)
        
    elif choice in ['2', '02']:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Generating with external wordlists...")
        base_combinations = generate_combinations(keywords)
        base_variations = add_common_variations(base_combinations)
        external_words = download_external_wordlists()
        wordlist = merge_with_common_wordlists(base_variations)
        wordlist.extend(external_words)
        
    elif choice in ['3', '03']:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Generating advanced wordlist...")
        
        try:
            max_combo_length = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Max combination length (1-4) -> {reset}"))
            if max_combo_length > 4:
                max_combo_length = 4
        except:
            max_combo_length = 3
        
        # Generate all combinations
        wordlist = generate_combinations(keywords, max_length=max_combo_length)
        
        # Add variations
        wordlist = add_common_variations(wordlist)
        
        # Add leet speak variations
        leet_variations = add_leet_speak_variations(wordlist)
        wordlist.extend(leet_variations)
        
        # Add advanced patterns
        pattern_variations = generate_advanced_patterns(keywords)
        wordlist.extend(pattern_variations)
        
        # Merge with external if requested
        merge_external = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Merge with external wordlists? (y/n) -> {reset}")
        if merge_external.lower() in ['y', 'yes']:
            external_words = download_external_wordlists()
            wordlist = merge_with_common_wordlists(wordlist)
            wordlist.extend(external_words)
    
    elif choice in ['4', '04']:
        print(f"""
 {BEFORE}01{AFTER}{white} Passwords
 {BEFORE}02{AFTER}{white} Usernames
 {BEFORE}03{AFTER}{white} Directories
 {BEFORE}04{AFTER}{white} Subdomains
        """)
        
        context_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Context type -> {reset}")
        context_map = {'1': 'passwords', '01': 'passwords', '2': 'usernames', '02': 'usernames',
                      '3': 'directories', '03': 'directories', '4': 'subdomains', '04': 'subdomains'}
        
        wordlist_type = context_map.get(context_choice, 'passwords')
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Generating {white}{wordlist_type}{red} wordlist...")
        
        # Generate base combinations
        wordlist = generate_combinations(keywords)
        wordlist = add_common_variations(wordlist)
        
        # Add contextual words
        contextual_words = add_contextual_words(keywords, wordlist_type)
        wordlist.extend(contextual_words)
        
        # Add leet speak for passwords
        if wordlist_type == 'passwords':
            leet_variations = add_leet_speak_variations(wordlist[:100])
            wordlist.extend(leet_variations)
    
    elif choice in ['5', '05']:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Generating pattern-based wordlist...")
        
        # Generate base words
        wordlist = generate_combinations(keywords)
        
        # Add all types of variations
        wordlist = add_common_variations(wordlist)
        leet_variations = add_leet_speak_variations(wordlist[:50])
        pattern_variations = generate_advanced_patterns(keywords)
        
        wordlist.extend(leet_variations)
        wordlist.extend(pattern_variations)
        
        # Add keyboard patterns
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1qaz', '2wsx', '3edc', 'qazwsx', 'qwertyuiop']
        for keyword in keywords:
            for pattern in keyboard_patterns:
                wordlist.append(keyword + pattern)
                wordlist.append(pattern + keyword)
        
        # Add seasonal/temporal patterns
        seasons = ['spring', 'summer', 'autumn', 'winter', 'january', 'february', 'march', 'april', 'may', 'june']
        for keyword in keywords:
            for season in seasons:
                wordlist.append(keyword + season)
                wordlist.append(season + keyword)

    # Remove duplicates and sort
    wordlist = list(set(wordlist))
    wordlist.sort()
    
    # Filter out empty strings and very short passwords
    min_length = 3
    try:
        min_length = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Minimum word length (default: 3) -> {reset}") or "3")
    except:
        min_length = 3
    
    wordlist = [word for word in wordlist if len(word) >= min_length and word.strip()]
    
    # Optional: Limit wordlist size
    max_words = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Maximum words (press enter for no limit) -> {reset}")
    if max_words.strip():
        try:
            max_words = int(max_words)
            if len(wordlist) > max_words:
                # Keep most relevant words (shorter ones first, then by frequency patterns)
                wordlist = sorted(wordlist, key=lambda x: (len(x), x))[:max_words]
        except:
            pass
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Generated {white}{len(wordlist)}{red} unique words")
    
    # Save wordlist
    filename = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Wordlist filename -> {reset}")
    if not filename.strip():
        filename = f"custom_wordlist_{int(datetime.now().timestamp())}"
    
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    output_file = os.path.join(tool_path, "1-Output", "Wordlists", filename)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Custom Wordlist Generated by {name_tool}\n")
        f.write(f"# Website: {website}\n")
        f.write(f"# Keywords: {', '.join(keywords)}\n")
        f.write(f"# Generation Type: {choice}\n")
        f.write(f"# Generated: {current_time_day_hour()}\n")
        f.write(f"# Total words: {len(wordlist)}\n")
        f.write(f"# Minimum length: {min_length}\n\n")
        
        for word in wordlist:
            f.write(word + '\n')
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Wordlist saved to: {white}{output_file}")
    
    # Show statistics
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Wordlist Statistics:")
    print(f"  Total words: {white}{len(wordlist)}")
    print(f"  Average length: {white}{sum(len(word) for word in wordlist) / len(wordlist):.1f}")
    print(f"  Shortest word: {white}{min(len(word) for word in wordlist)}")
    print(f"  Longest word: {white}{max(len(word) for word in wordlist)}")
    
    # Show sample
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Sample words:")
    sample_size = min(20, len(wordlist))
    sample_words = random.sample(wordlist, sample_size) if len(wordlist) > sample_size else wordlist[:sample_size]
    
    for i, word in enumerate(sample_words):
        print(f"  {white}{word}")
    
    if len(wordlist) > sample_size:
        print(f"  {white}... and {len(wordlist) - sample_size} more")

    # Option to create additional wordlists
    create_more = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Create another wordlist? (y/n) -> {reset}")
    if create_more.lower() in ['y', 'yes']:
        Reset()

    Continue()
    Reset()
except Exception as e:
    Error(e)