# Discord-Moderation-bot
   Basic discord bot written in python and discord.py to provide useful moderation tools to a discord server

# Features
   - kick
   - Ban/unban/softban
   - Clear
   - Profanity filter
   - Roles (In progress)
 
# Modules to install
   - Discord
   - Itertools
   - asyncio
  
# How to setup
   To setup this bot yourself simply clone the repo add the token from the discord bot bot you have created via discord:
   
   ```
   bot.run('insert_token_here')
   ```
    
   To change the command prefix (default = './') to something such as "/" or "~":
   ```
   bot = commands.Bot(command_prefix = 'insert_preifx_here')
   ```
# To run
   Ensure that the script is executable: ```chmod +x main.py```
   
   Run the script: ```./main.py```
   
# How to use
   Commands:
   - Kick: ./kick member_name
   - Ban: ./ban  member_name
   - Unban: ./unban member_name
   - Softban: ./softban member_name time
   - Clear: ./clear 20 (this means 20 messages will be deleted)
   - Blacklist: ./blacklist_add word (word is where you would type what you want to blacklist

# Notes

- Migrated from old github account