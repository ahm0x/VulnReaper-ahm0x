
from Config.Util import *
from Config.Config import *
try:
    import requests
    import threading
except Exception as e:
   ErrorModule(e)

Title("Discord Token Delete Friends")

try:
    Slow(discord_banner)
    token = Choice1TokenDiscord()
    r = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'}, timeout=5)
    if r.status_code == 200:
        pass
    else:
        ErrorToken()
    def DeleteFriends(friends, token):
        for friend in friends:
            try:
                requests.delete(
                    f'https://discord.com/api/v9/users/@me/relationships/'+friend['id'], headers={'Authorization': token}, timeout=5)
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Status: {white}Delete{red} | User: {white}{friend['user']['username']}#{friend['user']['discriminator']}")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Status: {white}Error: {e}{red}")

    if not requests.get("https://discord.com/api/v9/users/@me/relationships", headers={'Authorization': token, 'Content-Type': 'application/json'}, timeout=5).json():
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Status: {white}Error{red}")

    processes = []
    friend_id = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={'Authorization': token, 'Content-Type': 'application/json'}, timeout=5).json()
    if not friend_id:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No friends found.")

    for friend in [friend_id[i:i+3] for i in range(0, len(friend_id), 3)]:
        t = threading.Thread(target=DeleteFriends, args=(friend, token))
        t.start()
        processes.append(t)
    for process in processes:
        process.join()
    Continue()
    Reset()
except Exception as e:
    Error(e)