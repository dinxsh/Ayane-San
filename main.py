import discord
import os
import asyncio

from discord.ext import tasks, commands
from discord.utils import get
from itertools import cycle

prefix = '!'

bot = commands.Bot(command_prefix = prefix)

bot.remove_command('help')

status = cycle(["listening to yo mom", "listening to !help", "UwU"])

#|--------------------EVENTS--------------------|

@bot.event
async def on_ready():
    #Enter any startup tasks here
    change_status.start()
    #This is printed in the console to notify the user that the bot is running correctly without error
    print("Bot is ready to use.")

@bot.event
async def on_member_join(member):    
    print(f'Welcome {member.mention}!, glad to have you here!')

@bot.event
async def on_message(message):
    if prefix in message.content:
        print("This is a command")
        await bot.process_commands(message)
    else:
        # with open("words_blacklist.txt") as bf:
        #     blacklist = [word.strip().lower() for word in bf.readlines()]
        # bf.close()
        # blacklist words here 

        channel = message.channel        
                
    await bot.process_commands(message)

#This event waits for commands to be issued, if a specific command requires a permission or arguement
#This event will be invoked to tell the user that they dont have the required permissions
#or they havent issues the command correctly

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Oh no! Looks like you have missed out an argument for this command.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Oh no! Looks like you Dont have the permissions for this command.")
    if isinstance(error, commands.MissingRole):
        await context.send("Oh no! Looks like you Dont have the roles for this command.")
    #bot errors
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Oh no! Looks like I Dont have the permissions for this command.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Oh no! Looks like I Dont have the roles for this command.")
    

#|------------------COMMANDS------------------|   
@bot.command()
async def help(message):
    helpC = discord.Embed(title="moderator Bot \nHelp Guide", description="discord bot built for moderation")
    helpC.set_thumbnail(url='https://i.imgur.com/ZOKp8LH.png')
    helpC.add_field(name="clear", value="To use this command type !clear and the number of messages you would like to delete, the default is 5.", inline=False)
    helpC.add_field(name="kick/ban/unban", value="To use this command type !kick, !ban, !unban then mention the user you would like to perform this on, NOTE: user must have permissions to use this command.", inline=False)

    await message.channel.send(embed=helpC)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'Member {member} has been kicked')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member} has been banned')

@bot.command()
async def calc(context, *, equation):        
    await context.send(f'Answer: ' + eval(equation))

#Unbanning a member is done via typing ./unban and the ID of the banned member
@bot.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await bot.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} has been unbanned')
    
#Bans a member for a specific number of days
@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : discord.Member, days, reason=None):
    #Asyncio uses seconds for its sleep function
    #multiplying the num of days the user enters by the num of seconds in a day
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} has been softbanned')
    await asyncio.sleep(days)
    print("Time to unban")
    await member.unban()
    await context.send(f'{member} softban has finished')

#This command will add a word to the blacklist to prevent users from typing that specific word
@bot.command()
@commands.has_permissions(ban_members=True)
async def blacklist_add(context, *, word):
    with open("words_blacklist.txt", "a") as f:
        f.write("\n"+word)
    f.close()

    await context.send(f'Word "{word}" added to blacklist.')

#|------------------TASKS------------------| 
#This is a task which runs every 5 seconds 
@tasks.loop(seconds=5)
async def change_status():
    #This loops through the status variable at the top of this file every 5 seconds
    await bot.change_presence(activity=discord.Game(next(status)))

bot.run('BOT_TOKEN_HERE')
