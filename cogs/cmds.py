from discord.ext import commands
import discord
import arrr
from mcstatus import MinecraftServer
from yandex.Translater import Translater
from random import choice as randomChoice
from googlesearch import search
from socket import *

#Yandex.Translate config
tr = Translater()
tr.set_key('trnsl.1.1.20190519T001258Z.4378ae11d5fc7776.639b743d37945f8e49bec9662b132531f80779e1')

class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help") #displays help messages
    async def help(self, ctx):
        helpMessage = """__Bot Commands:__
    **!help** *to display this help message and view the bot commands*
    **!google** ***search*** *to search google*
    **!youtube** ***search*** *to search youtube*
    **!mcstatus** *to check the official Minecraft server status*
    **!arrr** ***text*** *to speak like a pirate*
    **!translate** ***from*** **to** ***text*** *to translate between languages*
    **!langs** *to list the languages available for translation*
    **!mcping** ***ip:port*** *to check the status of another Java Edition minecraft server*
    **!ping** *to see the bot's latency between itself and the discord API*
    **!engrish** ***text*** *turns english into engrish*
    **!villagerspeak** ***text*** *turns english text into villager sounds*
    **!enchant** ***text*** *turns english text into the Minecraft enchantment table language, a.k.a. the Standard Galactic Alphabet.*
    """
        await ctx.send(helpMessage)
    
    @commands.command(name="google") #google stuff command
    async def google(self, ctx, *, message: str):
        await ctx.trigger_typing()
        for result in search(message, tld="co.in", num=1, stop=1, pause=0.1):
            await ctx.send(result)

    @commands.command(name="youtube") #same as google but limited to youtube only
    async def youtube(self, ctx, *, message: str):
        await ctx.trigger_typing()
        for result in search(message, tld="co.in", domains=['youtube.com'], num=1, stop=1, pause=0.1):
            await ctx.send(result)

    @commands.command(name="mcstatus") #checks status of JE server
    async def mcstatus(self, ctx):
        if ctx.guild.id == 593954944059572235: #if guild is Xenon MC
            await ctx.trigger_typing()
            status = MinecraftServer.lookup("172.10.17.177:25565")
            try:
                status = status.status()
                await ctx.send("Xenon JE is online with {0} player(s) and a ping of {1}.".format(status.players.online, status.latency))
            except Exception:
                await message.channel.send("Xenon JE is either offline or unavailable at the moment.")
        else:
            await ctx.send("This feature is not available for this server.")

    @commands.command(name="arrr") #converts english to pirate speak
    async def arrr(self, ctx, *, message: str):
        await ctx.send(arrr.translate(message))

    @commands.command(name="translate") #translates from one language to another
    async def translate(self, ctx, *, message: str):
        message = "!translate "+message
        await ctx.trigger_typing()
        from_lang = message[11:13]
        to_lang = message[14:16]
        try:
            tr.set_from_lang(from_lang)
        except Exception:
            await ctx.send("Translation error. 'Translation from' language is not supported.")
            return
        try:
            tr.set_to_lang(to_lang)
        except Exception:
            await ctx.send("Translation error. 'Translation to' language is not supported.")
            return
        to_lang = "{0} ".format(to_lang)
        from_lang = "{0} ".format(from_lang)
        if not message[16:] == '':
            if message[16:] is not "":
                try:
                    tr.set_text(message[16:])
                    translation = tr.translate()
                except Exception:
                    translation = "Translation error. Perhaps check the formatting of the command?"
                await ctx.send(translation)
            elif message[16:] is "":
                await ctx.send("No text was provided for translation.")

    @commands.command(name="langs")
    async def langs(self, ctx):
        await ctx.send("http://172.10.17.177/images/langs.png")

    @commands.command(name="mcping") #pings a java edition minecraft server
    async def mcping(self, ctx, *, message: str):
        await ctx.trigger_typing()
        status = MinecraftServer.lookup(message)
        try:
            status = status.status()
            await ctx.send(message+" is online with {0} player(s) and a ping of {1}.".format(status.players.online, status.latency))
        except Exception:
            await ctx.send(message+" is either offline or unavailable at the moment.")
            await ctx.send("Did you type the ip and port correctly? (Like ip:port)")

    @commands.command(name="ping") #checks latency between Discord API and the bot
    async def ping(self, ctx):
        await ctx.send("Pong! "+str(self.bot.latency*1000)[:5]+" ms")

    @commands.command(name="engrish") #converts english into engrish
    async def engrish(self, ctx, *, message: str):
        msg = message.split(" ")
        final = ""
        for word in msg:
            wordd = word + " "
            wordd = wordd.replace("ck", "xk").replace("like", "liek").replace("ee", "i").replace("gh", "hg").replace("t", randomChoice(["t", "t", "t", "t", "t", "T", "t", "t", "t", "t"]))
            wordd = wordd.replace("o", "oo").replace("and", "an").replace("was", "were").replace(" a ", " ").replace("’", "")
            wordd = wordd.replace("nch", "ntch").replace("english", "engrish").replace("ea", "e").replace("'", "").replace("an", "and")
            wordd = wordd.replace(".", "").replace("to", "too").replace("I", "i").replace("ay", "ey").replace("em", "m").replace("pac", "pas")
            wordd = wordd.replace("you", "u").replace("what", "wat").replace("similar", "simialiar").replace("which", "wich").replace("ty", "tee")
            wordd = wordd.replace("definitely", "definately").replace("l", "ll").replace("noob", "nub").replace("ae", "ay").replace(",", "")
            wordd = wordd.replace("io", "i").replace("ed", randomChoice(["eded", "ed"])).replace("ge ", "jeh ").replace("ry", "ree").replace("ai", "e")
            wordd = wordd.replace(" f ", " oof ").replace("that", "taht").replace("so", randomChoice(["sooo", "so", "soo", "so"])).replace("wom", "wam").replace("llll", "l")
            wordd = wordd.replace("the", randomChoice(["teh", "the"])).replace("thanks", "tahnks").replace("e", randomChoice(["e", "e", "e", "e", "e", "E", "e", "e", "e", "e", "e"]))
            final += wordd
        if not len(final) > 2000:
            await ctx.send(final)
        else:
            await ctx.send("Message would be too long to convert!")

    @commands.command(name="villagerspeak") #converts english into villager noises
    async def villagerspeak(self, ctx, *, message: str):
        letters = list(message)
        final = ""
        for letter in letters:
            letterr = letter
            letterr = letterr.replace("A", "HRUH").replace("a", "hruh").replace("B", "HUR").replace("b", "hur").replace("C", "HURGH").replace("c", "hurgh")
            letterr = letterr.replace("D", "HDUR").replace("d", "hdur").replace("E", "MREH").replace("e", "mreh").replace("F", "HRGH").replace("f", "hrgh")
            letterr = letterr.replace("G", "HG").replace("g", "hg").replace("H", "HHH").replace("h", "hhh").replace("I", "EHR").replace("i", "EHR")
            letterr = letterr.replace("J", "HRG").replace("j", "hrg").replace("K", "HREGH").replace("k", "hregh").replace("L", "HRMG").replace("l", "hrmg")
            letterr = letterr.replace("M", "HRMM").replace("m", "hrmm").replace("N", "HMEH").replace("n", "hmeh").replace("O", "HUGH").replace("o", "hugh")
            letterr = letterr.replace("P", "HRUM").replace("p", "hrum").replace("Q", "HUERHG").replace("q", "huerhg").replace("R", "HRRRH").replace("r", "hrrrh")
            letterr = letterr.replace("S", "SURGGHM").replace("s", "surgghm").replace("T", "EHRRG").replace("t", "ehrrg").replace("U", "HRMHM").replace("u", "hrmhm")
            letterr = letterr.replace("V", "HRRRM").replace("v", "hrrrm").replace("W", "HWURGH").replace("w", "hhwurgh").replace("X", "MURR").replace("x", "murr")
            letterr = letterr.replace("Y", "HURR").replace("y", "hurr").replace("Z", "MHEHMEM").replace("z", "mhhmem")
            final += letterr
        if not len(final) > 2000:
            await ctx.send(final)
        else:
            await ctx.send("Message would be too long to convert!")

    @commands.command(name="enchant") #converts english to enchantment table language
    async def enchant(self, ctx, *, message: str):
        msg = message
        msg = msg.replace("A", "ᔑ").replace("a", "ᔑ").replace("B", "ʖ").replace("b", "ʖ").replace("C", "ᓵ").replace("c", "ᓵ")
        msg = msg.replace("D", "↸").replace("d", "↸").replace("E", "ᒷ").replace("e", "ᒷ").replace("F", "⎓").replace("f", "⎓")
        msg = msg.replace("G", "⊣").replace("g", "⊣").replace("H", "⍑").replace("h", "⍑").replace("I", "╎").replace("i", "╎")
        msg = msg.replace("J", "⋮").replace("j", "⋮").replace("K", "ꖌ").replace("k", "ꖌ").replace("L", "ꖎ").replace("l", "ꖎ")
        msg = msg.replace("M", "ᒲ").replace("m", "ᒲ").replace("N", "リ").replace("n", "リ").replace("O", "J").replace("o", "J")
        msg = msg.replace("P", "!¡").replace("p", "!¡").replace("Q", "ᑑ").replace("q", "ᑑ").replace("R", "∷").replace("r", "∷")
        msg = msg.replace("S", "ᓭ").replace("s", "ᓭ").replace("T", "ℸ").replace("t", "ℸ").replace("U", "⚍").replace("u", "⚍")
        msg = msg.replace("V", "⍊").replace("v", "⍊").replace("W", "∴").replace("w", "∴").replace("X", "̇/").replace("x", "̇/")
        msg = msg.replace("Y", "||").replace("y", "||").replace("Z", "⨅").replace("z", "⨅")
        await ctx.send("```"+msg+"```")

def setup(bot):
    bot.add_cog(Cmds(bot))
