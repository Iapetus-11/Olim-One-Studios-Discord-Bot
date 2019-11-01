from discord.ext import commands
import discord
from random import choice

global msg_count
msg_count = 0

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global msg_count
        try:
            try:
                print(str(message.author)+": "+str(message.clean_content))
            except Exception:
                print(str(message.author)+": ")
        except Exception:
            pass
        msg_count += 1
        if msg_count%50 == 0:
            playing = open("playing.txt", "r").readlines()
            await self.bot.change_presence(activity=discord.Game(name=choice(playing)))

def setup(bot):
    bot.add_cog(Messages(bot))
