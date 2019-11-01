from discord.ext import commands
import discord
from random import choice

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("Successfully connected to Discord!"+"\n")
        playing = open("playing.txt", "r").readlines()
        await self.bot.change_presence(activity=discord.Game(name=choice(playing)))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == self.bot.get_guild(593954944059572235):
            channel = self.bot.get_channel(593988932564418590)
            xenonWelcome = """Hey {0}, welcome to **Xenon MC**! To access the server, please take a look at the {1} and fill it out in {2}. Then read through {3}. A moderator or the owner will look over your application soon after!"""
            await channel.send(xenonWelcome.format(member.mention, self.bot.get_channel(593999836647391252).mention, self.bot.get_channel(593973607160348682).mention, self.bot.get_channel(593997092234461194).mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild == self.bot.get_guild(593954944059572235):
            channel = self.bot.get_channel(593988932564418590)
            xenonGoodbye = """Goodbye, **{0}**"""
            await channel.send(xenonGoodbye.format(member.display_name))
            
def setup(bot):
    bot.add_cog(Events(bot))
