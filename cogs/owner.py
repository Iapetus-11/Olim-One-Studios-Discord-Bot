from discord.ext import commands
import discord

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unload")
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension("cogs."+cog)
        except Exception as e:
            await ctx.send("Error while unloading extension: "+cog+"\n``"+str(e)+"``")
            return
        await ctx.send("Successfully unloaded cog: "+cog)

    @commands.command(name="load")
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension("cogs."+cog)
        except Exception as e:
            await ctx.send("Error while loading extension: "+cog+"\n``"+str(e)+"``")
            return
        await ctx.send("Successfully loaded cog: "+cog)
            
    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension("cogs."+cog)
        except Exception as e:
            await ctx.send("Error while unloading extension: "+cog+"\n``"+str(e)+"``")
            return
        try:
            self.bot.load_extension("cogs."+cog)
        except Exception as e:
            await ctx.send("Error while loading extension: "+cog+"\n``"+str(e)+"``")
            return
        await ctx.send("Successfully reloaded cog: "+cog)

    @commands.command(name="guilds")
    @commands.is_owner()
    async def guilds(self, ctx):
        for guild in self.bot.guilds:
            await ctx.send(guild.name+" "+str(guild.id))

def setup(bot):
    bot.add_cog(Owner(bot))
