from discord.ext import commands
import discord
from os import system

#set window title
system("title Discord Bot")

bot = commands.Bot(command_prefix='!', help_command=None)
cogs = ["cmds", "admincmds", "messages", "events", "owner"]

#load cogs in cogs list
for cog in cogs:
    bot.load_extension("cogs."+cog)

#actually start bot
key = open("key.txt", "r").read()
bot.run(key, bot=True)
