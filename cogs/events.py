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
            xenonWelcome = """Hey {0}, welcome to **Xenon Gaming**! Please read through {3}. If you're interested in our Minecraft server, take a look at the {1} and fill it out in {2}."""
            await channel.send(xenonWelcome.format(member.mention, self.bot.get_channel(593999836647391252).mention, self.bot.get_channel(593973607160348682).mention, self.bot.get_channel(593997092234461194).mention))
        if member.guild == self.bot.get_guild(641117791272960031):
            channel = self.bot.get_channel(643269881919438860)
            await channel.send("""Welcome, **{0}**, please read through the {1}""".format(member.display_name, self.bot.get_channel(641119824105308182)))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild == self.bot.get_guild(593954944059572235):
            channel = self.bot.get_channel(593988932564418590)
            xenonGoodbye = """Goodbye, **{0}**"""
            await channel.send(xenonGoodbye.format(member.display_name))
        if member.guild == self.bot.get_guild(641117791272960031):
            channel = self.bot.get_channel(643269881919438860)
            await channel.send("""Goodbye, **{0}**""".format(member.display_name))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        channel = self.bot.get_channel(642440269819674655)
        await channel.send(ctx.author.name+"#"+ctx.author.discriminator+": ```"+ctx.message.content+"\n--------------------------\n"+str(error)+"```")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        channel = self.bot.get_channel(645827431634042882)
        await channel.send(str(message.author)+": "+str(message.content))

def setup(bot):
    bot.add_cog(Events(bot))
