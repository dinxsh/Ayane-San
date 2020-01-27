import discord
import os

from discord.ext import tasks, commands
from discord.utils import get
from itertools import cycle

bot = commands.Bot(command_prefix = './')

bot.remove_command('help')

status = cycle(['status 1', "status 2", "status3"])

@bot.event
async def on_ready():
    #Enter any startup tasks here
    change_status.start()
    print("Bot is ready to use.")

@bot.event
async def on_member_join(context,member):
    await context.send(f'Member {member.mention} has joined!')

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
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    print(f'Member {member} kicked')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    print(f'Member {member} kicked')

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
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

bot.run('')