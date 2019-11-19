from discord.ext import commands
import discord
from random import choice

class AdminCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="admincommands")
    @commands.has_permissions(administrator=True)
    async def adminCommands(self, ctx):
        helpMsg = discord.Embed(
            description = "",
            color = discord.Color.blue()
        )
        helpMsg.add_field(name="__Admin Bot Commands__", value="""
**.purge** ***number of messages*** *deletes n number of messages in the channel it's summoned in.*
**.activity** ***text for bot to display*** *sets the activity of the bot.*
**.nextactivity** *skips to the next activity of the bot.*
**.addactivity** ***activity*** *adds the given activity to the list of randomly picked activities for the bot.*
    """)
        await ctx.send(embed=helpMsg)
    
    @commands.command(name="addactivity")
    @commands.has_permissions(administrator=True)
    async def activity(self, ctx, *, message: str):
        await ctx.message.delete()
        open("playing.txt", "a").write("\n"+message)
        
    @commands.command(name="activity")
    @commands.has_permissions(administrator=True)
    async def playing(self, ctx, *, message: str):
        await ctx.message.delete()
        await self.bot.change_presence(activity=discord.Game(name=message))

    @commands.command(name="purge")
    @commands.has_permissions(administrator=True)
    async def purgeMessages(self, ctx, *, message: str):
        try:
            await ctx.channel.purge(limit=int(message)+1)
        except Exception:
            await ctx.send("That is not a valid number")
            
    @commands.command(name="nextactivity")
    @commands.has_permissions(administrator=True)
    async def nextactivity(self, ctx):
        await ctx.message.delete()
        playing = open("playing.txt", "r").readlines()
        await self.bot.change_presence(activity=discord.Game(name=choice(playing)))
        
def setup(bot):
    bot.add_cog(AdminCmds(bot))
