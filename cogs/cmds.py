from discord.ext import commands
import discord
from mcstatus import MinecraftServer
from yandex.Translater import Translater
from random import choice, randint
from googlesearch import search
from os import listdir
import json
import arrow
from time import sleep

#Yandex.Translate config
tr = Translater()
tr.set_key('trnsl.1.1.20190519T001258Z.4378ae11d5fc7776.639b743d37945f8e49bec9662b132531f80779e1')

#other
global enchantlang
with open("enchantlang.json", "r") as langfile:
    enchantlang = json.load(langfile)
global villagersounds
with open("villagerlang.json", "r") as villagerlang:
    villagersounds = json.load(villagerlang)

class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help") #displays help messages
    async def help(self, ctx):
        helpMsg = discord.Embed(
            title = "__Bot Commands__",
            description = "",
            color = discord.Color.blue()
        )
        helpMsg.add_field(name="__Utility__", value="""
**.help** *to display this help message and view the bot commands*
**.google** ***search*** *to search google*
**.youtube** ***search*** *to search youtube*
**.mcstatus** *to check the official Minecraft server status*
**.translate** ***from*** *to* ***text*** *to translate between languages*
**.langs** *to list the languages available for translation*
**.mcping** ***ip:port*** *to check the status of another Java Edition minecraft server*
**.ping** *to see the bot's latency between itself and the discord API*
**.times** *bot will send the times of different areas of the world.*
    """)
        helpMsg.add_field(name="__Fun__", value="""
**.engrish** ***text*** *turns english into engrish*
**.villagerspeak** ***text*** *turns english text into villager sounds*
**.enchant** ***text*** *turns english text into the Minecraft enchantment table language, a.k.a. the Standard Galactic Alphabet*
**.unenchant** ***text*** *turns the enchanting table language back into English*
**.cute** *bot will send a cute picture of a pet your way!*
**.sarcastic** ***text*** *bot will change text to the sarcastic text*
**.battle** ***user*** *allows you to battle a friend via Discord*
    """)
        await ctx.send(embed=helpMsg)
    
    @commands.command(name="google") #google stuff command
    async def google(self, ctx, *, message: str):
        if message == "":
            ctx.send("You must say something for the bot to google.")
            return
        await ctx.trigger_typing()
        for result in search(message, tld="co.in", num=1, stop=1, pause=0.1):
            await ctx.send(result)

    @commands.command(name="youtube") #same as google but limited to youtube only
    async def youtube(self, ctx, *, message: str):
        if message == "":
            ctx.send("You must say something for the bot to search youtube for.")
            return
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
        await ctx.send(file=discord.File("imgs\langs.png"))

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
        if message == "":
            ctx.send("You must say something for the bot to translate.")
            return
        msg = message.split(" ")
        final = ""
        for word in msg:
            wordd = word + " "
            wordd = wordd.replace("ck", "xk").replace("like", "liek").replace("ee", "i").replace("gh", "hg").replace("t", choice(["t", "t", "t", "t", "t", "T", "t", "t", "t", "t"]))
            wordd = wordd.replace("o", "oo").replace("and", "an").replace("was", "were").replace(" a ", " ").replace("’", "")
            wordd = wordd.replace("nch", "ntch").replace("english", "engrish").replace("ea", "e").replace("'", "").replace("an", "and")
            wordd = wordd.replace(".", "").replace("to", "too").replace("I", "i").replace("ay", "ey").replace("em", "m").replace("pac", "pas")
            wordd = wordd.replace("you", "u").replace("what", "wat").replace("similar", "simialiar").replace("which", "wich").replace("ty", "tee")
            wordd = wordd.replace("definitely", "definately").replace("l", "ll").replace("noob", "nub").replace("ae", "ay").replace(",", "")
            wordd = wordd.replace("io", "i").replace("ed", choice(["eded", "ed"])).replace("ge ", "jeh ").replace("ry", "ree").replace("ai", "e")
            wordd = wordd.replace(" f ", " oof ").replace("that", "taht").replace("so", choice(["sooo", "so", "soo", "so"])).replace("wom", "wam").replace("llll", "l")
            wordd = wordd.replace("the", choice(["teh", "the"])).replace("thanks", "tahnks").replace("e", choice(["e", "e", "e", "e", "e", "E", "e", "e", "e", "e", "e"]))
            final += wordd
        if not len(final) > 2000:
            await ctx.send(final)
        else:
            await ctx.send("Message would be too long to convert.")

    @commands.command(name="villagerspeak") #converts english into villager noises
    async def villagerspeak(self, ctx, *, message: str):
        if message == "":
            ctx.send("You must say something for the bot to translate.")
            return
        global villagersounds
        villager = ""
        letters = list(message)
        for letter in letters:
            if letter.lower() in villagersounds:
                villager += villagersounds.get(letter.lower())
            else:
                villager += letter.lower()
        if not len(villager) > 2000:
            await ctx.send(villager)
        else:
            await ctx.send("Message would be too long to convert.")

    @commands.command(name="enchant") #converts english to enchantment table language
    async def enchant(self, ctx, *, message: str):
        if message == "":
            ctx.send("You must say something for the bot to translate.")
            return
        global enchantlang
        msg = message
        for key, value in enchantlang.items():
            msg = msg.replace(key, value)
        if len(msg)+6 <= 2000:
            await ctx.send("```"+msg+"```")
        else:
            await ctx.send("Message would be too long to convert.")

    @commands.command(name="unenchant") #converts enchantment table language to english
    async def unenchant(self, ctx, *, message: str):
        if message == "":
            ctx.send("You must say something for the bot to translate.")
            return
        global enchantlang
        msg = message
        for key, value in enchantlang.items():
            msg = msg.replace(value, key)
        if len(msg) <= 2000:
            await ctx.send(msg.lower())
        else:
            await ctx.send("Message would be too long to convert.")
            
    @commands.command(name="cute") #fetches random image of cute pet or animal
    async def randomimage(self, ctx):
        await ctx.trigger_typing()
        imgs = listdir("Z:\\Coding\\Python\\Discord Bot\\imgs\\cute\\")
        img = "imgs\\cute\\"+choice(imgs)
        await ctx.send(file=discord.File(img))

    @commands.command(name="times") #gets timezones and displays them
    async def timezones(self, ctx):
        await ctx.trigger_typing()
        msg = """
__**United States:**__
**Eastern (EST):** {0}
**Central (CST):** {1}
**Mountain (MST):** {2}
**Pacific (PST):** {3}
**Alaskan (AKST):** {4}
**Hawaiian (HST):** {5}\n
__**Greenwich Mean Time:**__
**GMT+9:** {6}**  GMT-3:** {16}
**GMT+8:** {7}**  GMT-4:** {17}
**GMT+7:** {6}**  GMT-5:** {18}
**GMT+6:** {7}**  GMT-6:** {19}
**GMT+5:** {8}**  GMT-7:** {20}
**GMT+4:** {9}**  GMT-8:** {21}
**GMT+3:** {10}**  GMT-9:** {22}
**GMT+2:** {11}**  GMT-10:** {23}
**GMT+1:** {12}**  GMT-11:** {24}
**GMT+0:** {13}**  GMT-12:** {25}
**GMT-1:** {14}**  GMT-13:** {26}
**GMT-2:** {15}**  GMT-14:** {27}
"""
        eastern = arrow.utcnow().to("US/Eastern").format("DD/MM HH:mm")
        central = arrow.utcnow().to("US/Central").format("DD/MM HH:mm")
        mountain = arrow.utcnow().to("US/Mountain").format("DD/MM HH:mm")
        pacific = arrow.utcnow().to("US/Pacific").format("DD/MM HH:mm")
        alaskan = arrow.utcnow().to("US/Alaska").format("DD/MM HH:mm")
        hawaiian = arrow.utcnow().to("US/Hawaii").format("DD/MM HH:mm")
        gmt9 = arrow.utcnow().to("Etc/GMT+9").format("DD/MM HH:mm")
        gmt8 = arrow.utcnow().to("Etc/GMT+8").format("DD/MM HH:mm")
        gmt7 = arrow.utcnow().to("Etc/GMT+7").format("DD/MM HH:mm")
        gmt6 = arrow.utcnow().to("Etc/GMT+6").format("DD/MM HH:mm")
        gmt5 = arrow.utcnow().to("Etc/GMT+5").format("DD/MM HH:mm")
        gmt4 = arrow.utcnow().to("Etc/GMT+4").format("DD/MM HH:mm")
        gmt3 = arrow.utcnow().to("Etc/GMT+3").format("DD/MM HH:mm")
        gmt2 = arrow.utcnow().to("Etc/GMT+2").format("DD/MM HH:mm")
        gmt1 = arrow.utcnow().to("Etc/GMT+1").format("DD/MM HH:mm")
        gmt0 = arrow.utcnow().to("Etc/GMT+0").format("DD/MM HH:mm")
        gmtmin1 = arrow.utcnow().to("Etc/GMT-1").format("DD/MM HH:mm")
        gmtmin2 = arrow.utcnow().to("Etc/GMT-2").format("DD/MM HH:mm")
        gmtmin3 = arrow.utcnow().to("Etc/GMT-3").format("DD/MM HH:mm")
        gmtmin3 = arrow.utcnow().to("Etc/GMT-3").format("DD/MM HH:mm")
        gmtmin4 = arrow.utcnow().to("Etc/GMT-4").format("DD/MM HH:mm")
        gmtmin5 = arrow.utcnow().to("Etc/GMT-5").format("DD/MM HH:mm")
        gmtmin6 = arrow.utcnow().to("Etc/GMT-6").format("DD/MM HH:mm")
        gmtmin7 = arrow.utcnow().to("Etc/GMT-7").format("DD/MM HH:mm")
        gmtmin8 = arrow.utcnow().to("Etc/GMT-8").format("DD/MM HH:mm")
        gmtmin9 = arrow.utcnow().to("Etc/GMT-9").format("DD/MM HH:mm")
        gmtmin10 = arrow.utcnow().to("Etc/GMT-10").format("DD/MM HH:mm")
        gmtmin11 = arrow.utcnow().to("Etc/GMT-11").format("DD/MM HH:mm")
        gmtmin12 = arrow.utcnow().to("Etc/GMT-12").format("DD/MM HH:mm")
        gmtmin13 = arrow.utcnow().to("Etc/GMT-13").format("DD/MM HH:mm")
        gmtmin14 = arrow.utcnow().to("Etc/GMT-14").format("DD/MM HH:mm")
        await ctx.send(msg.format(eastern, central, mountain, pacific, alaskan, hawaiian, gmt9, gmt8, gmt7, gmt6, gmt5, gmt4, gmt3, gmt2, gmt1, gmt0, gmtmin1, gmtmin2, gmtmin3, gmtmin4, gmtmin5, gmtmin6, gmtmin7, gmtmin8, gmtmin9, gmtmin10, gmtmin11, gmtmin12, gmtmin13, gmtmin14))

    @commands.command(name="sarcastic")
    async def sarcasm(self, ctx):
        changeletter = False
        sarcastic = ""
        for letter in ctx.message.content.replace(".sarcastic ", ""):
            if changeletter:
                sarcastic += letter.upper()
                changeletter = not changeletter
            else:
                sarcastic += letter.lower()
                changeletter = not changeletter
        await ctx.send(sarcastic)

    @commands.command(name="battle")
    async def fight(self, ctx, user: discord.User):
        battleAnnounce = discord.Embed(
            title = "***"+ctx.message.author.display_name+"***  has challenged ***"+user.display_name+"***  to a sword fight!",
            description = "**Who will the victor be? Who will be known as greater for the rest of time?**",
            color = discord.Color.from_rgb(255, 0, 0)
        )
        battleAnnounce.set_thumbnail(url="http://172.10.17.177/images/diamondswords2.png")
        await ctx.send(embed=battleAnnounce)
        if ctx.message.author == user:
            await ctx.send("**"+user.display_name+"** "+choice(["committed dig straight down.",
                                                "died by self inflicted stab wound.",
                                                "died by punching a golem.",
                                                "dug straight down into lava.",
                                                "blew themselves up with TNT.",
                                                "died by pillager raid.",
                                                "ran into a creeper."]))
            return

        p1_hp = 20
        p2_hp = 20
        await ctx.send(embed=discord.Embed(title="***"+ctx.message.author.display_name+":*** "+str(p1_hp)+" hp | ***"+user.display_name+":*** "+str(p2_hp)+" hp", color = discord.Color.from_rgb(255, 0, 0)))
        while p1_hp > 0 and p2_hp > 0:
            sleep(0.95)
            p2_hp -= randint(1, 12) #player 1's turn
            p1_hp -= randint(4, 12) #player 2's turn
            if p2_hp < 0:
                p2_hp = 0

            if p1_hp < 0:
                p1_hp = 0
            
            if p2_hp <= 0:
                p2_hp = 0
                if p1_hp <= 0:
                    p1_hp = 1
                await ctx.send(embed=discord.Embed(title="***"+ctx.message.author.display_name+":*** "+str(p1_hp)+" hp | ***"+user.display_name+":*** "+str(p2_hp)+" hp", color = discord.Color.from_rgb(255, 0, 0)))
                win = discord.Embed(
                    title = "**"+ctx.message.author.display_name+" The Great** has defeated **"+user.display_name+" the lesser!**",
                    color = discord.Color.from_rgb(255, 0, 0)
                )
                win.set_thumbnail(url=str(ctx.message.author.avatar_url))
                await ctx.send(embed=win)
            elif p1_hp <= 0:
                p1_hp = 0
                if p2_hp <= 0:
                    p2_hp = 1
                await ctx.send(embed=discord.Embed(title="***"+ctx.message.author.display_name+":*** "+str(p1_hp)+" hp | ***"+user.display_name+":*** "+str(p2_hp)+" hp", color = discord.Color.from_rgb(255, 0, 0)))
                win = discord.Embed(
                    title = "**"+user.display_name+" The Great** has defeated **"+ctx.message.author.display_name+" the lesser!**",
                    color = discord.Color.from_rgb(255, 0, 0)
                )
                win.set_thumbnail(url=str(user.avatar_url))
                await ctx.send(embed=win)
            else:
                await ctx.send(embed=discord.Embed(title="***"+ctx.message.author.display_name+":*** "+str(p1_hp)+" hp | ***"+user.display_name+":*** "+str(p2_hp)+" hp", color = discord.Color.from_rgb(255, 0, 0)))

def setup(bot):
    bot.add_cog(Cmds(bot))
