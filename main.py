import discord
import os

from discord.ext import tasks, commands
from discord.utils import get
from itertools import cycle

#Comman prefix is setup here, this is what you have to type to issue a command to the bot
bot = commands.Bot(command_prefix = './')

#Removed the help command to create a custom help guide
bot.remove_command('help')

#Variable containing statuses for the bot to cycle through
status = cycle(['status 1', "status 2", "status3"])

#|--------------------EVENTS--------------------|

@bot.event
async def on_ready():
    #Enter any startup tasks here
    change_status.start()
    #This is printed in the console to notify the user that the bot is running correctly without error
    print("Bot is ready to use.")

@bot.event
async def on_member_join(context,member):
    #When a member joins the discord, they will get mentioned with this welcome message
    await context.send(f'Member {member.mention} has joined!')

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
    helpC.add_field(name="Clear", value="To use this command type ./clear and the number of messages you would like to delete, the default is 5.", inline=False)
    helpC.add_field(name="kick/ban/unban", value="To use this command type ./kick/ban/unban then mention the user you would like to perform this on, NOTE: user must have permissions to use this command.", inline=False)

    await message.channel.send(embed=helpC)

@bot.command()
#Checks whether the user has the correct permissions when this command is issued
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

#Kick and ban work in a similar way as they both require a member to kick/ban and a reason for this
#As long as the moderator has the right permissions the member will be banned/kicked
@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, meember : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    print(f'Member {member} kicked')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    print(f'Member {member} kicked')

#Unbanning a member is done via typing ./unban and the member name, this command will retrieve the ban list from the server
#It will check whether the user is in the banned list and then will unban them if so
@bot.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, *, member):
    bannedList = await context.guild.bans()
    name, descriminator = member.split('#')

    for unbanEntry in bannedList:
        toUnban = unbanEntry.User
        if (toUnban.name, toUnban.descriminator) == (name, descriminator):
            await context.guild.unban(toUnban)

#@bot.command()
#@commands.has_permissions(ban_members=True)
#async def softban(context, *, member, time):


#ADD SOFTBAN | CLEAN MESSAGES

#|------------------TASKS------------------| 
#This is a task which runs every 5 seconds (change this to however long you require
@tasks.loop(seconds=5)
async def change_status():
    #This loops through the status variable at the top of this file every 5 seconds
    await bot.change_presence(activity=discord.Game(next(status)))

#Enter your bot token from discord here, so when the code runs, your discord bot will come online
bot.run('')
