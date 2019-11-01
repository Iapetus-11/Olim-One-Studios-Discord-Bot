from discord.ext import commands
import discord
from random import choice

class AdminCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="admincommands")
    @commands.has_any_role("Owner", "Former Owner/Co-Owner", "Admin")
    async def adminCommands(self, ctx):
        helpMessage = """__Bot Admin Commands:__
    **!purge** ***number of messages*** *deletes n number of messages in the channel it's summoned in.*
    **!activity** ***text for bot to display*** *sets the activity of the bot.*
    **!nextactivity** *skips to the next activity of the bot.*
    **!addactivity** ***activity*** *adds the given activity to the list of randomly picked activities for the bot.*
    """
        await ctx.send(helpMessage)
    
    @commands.command(name="addactivity")
    @commands.has_any_role("Owner", "Former Owner/Co-Owner", "Admin")
    async def activity(self, ctx, *, message: str):
        await ctx.message.delete()
        open("playing.txt", "a").write("\n"+message)
        
    @commands.command(name="activity")
    @commands.has_any_role("Owner", "Former Owner/Co-Owner", "Admin")
    async def playing(self, ctx, *, message: str):
        await ctx.message.delete()
        await self.bot.change_presence(activity=discord.Game(name=message))

    @commands.command(name="purge")
    @commands.has_any_role("Owner", "Former Owner/Co-Owner", "Admin")
    async def purgeMessages(self, ctx, *, message: str):
        try:
            await ctx.channel.purge(limit=int(message)+1)
        except Exception:
            await ctx.send("That is not a valid number")
            
    @commands.command(name="nextactivity")
    @commands.has_any_role("Owner", "Former Owner/Co-Owner", "Admin")
    async def nextactivity(self, ctx):
        playing = open("playing.txt", "r").readlines()
        await self.bot.change_presence(activity=discord.Game(name=choice(playing)))

def setup(bot):
    bot.add_cog(AdminCmds(bot))
