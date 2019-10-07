import discord
import arrr
import asyncio
from mcstatus import MinecraftServer
from yandex.Translater import Translater
from random import choice as randomChoice
from googlesearch import search
from socket import *
from os import system

#discord config
client = discord.Client()
discordToken = 'discord token'

#Yandex.Translate config
tr = Translater()
tr.set_key('translater key')

#other stuffs
userWelcomes = ["""Hey {0}, welcome to this server, we're glad to have you here! Please read the {1}.""", """Welcome, {0}, we're glad you joined! Please read the {1}.""",
                """Hello {0}, welcome to our Discord server! Please read the {1}.""", """Thanks for joining and welcome to the server {0}, please read the {1}."""]
userGoodbyes = ['Awwwww, {0} left us', '{0} did not even say goodbye ;(', '{0} just left...', '{0} could not handle the hot sauce.', '{0} decided to leave us.',
                'yeet yeet, {0} bounced back into the street.', 'I hope {0} has good luck on the outside...']
xenonMC1 = """Hey {0}, welcome to **XenonMC**! To access the server, please take a look at the {1} and fill it out in {2}. Then read through {3}. A moderator or the owner will look over your application soon after!"""
xenonMC2 = """Goodbye, **{0}**"""
playing = ["flirting with SlavBot", "hack the CIA", "Minecraft", "fortnite bad minecraft good", "Human Simulator 2019", "Big Chungus Simulator 2019", "Yandex.Translater",
              "flirting with ToddBot", "Pokecord", "Pokemon Red", "Pokemon Silver", "with a *****", "Winrar's 40 day trial - the simulation", "on a Wii", "Meme Assassin",
              "anything other than fortnite", "Minecraft Bedrock Edition", "Minecraft Java Edition", "Wii", "Thanos Simulator - Snapped Edition", "Tetris", "annoy the humans"]
system("title Discord Bot")
randomness = [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

#Iapetus11, Mckinlayyyy, Jake, LikeableCoconut, Raaaaoof SG, Rastley
admins = [536986067140608041, 480513935632498710, 338674447353380864, 447352787676692482, 454620186570653696, 593594606583808000]

@client.event
async def on_ready():
    try:
        #print bot information
        print(client.user.name)
        print(client.user.id)
        print("Successfully connected to Discord!")
        await client.change_presence(activity=discord.Game(name=randomChoice(playing)))
        
    except Exception as e:
        #print le error
        print(e)

@client.event
async def on_message(message):
    if randomChoice(randomness):
        await client.change_presence(activity=discord.Game(name=randomChoice(playing)))
        
    print(str(message.author) + " : " + str(message.clean_content)) #print message author and message
    
    #check to see if user is not self.
    if not message.author == client.user:
        #Help command
        if message.content[:5] == "!help":
            helpMessage = """__Bot Commands:__
    **!help** *to display this help message and view the bot commands.*
    **!google** ***search*** *to search google.*
    **!youtube** ***search*** *to search youtube.*
    **!mcstatus** *to check the official Minecraft server status.*
    **!arrr** ***text*** *to speak like a pirate.*
    **!translate** ***from*** **to** ***text*** *to translate between languages.*
    **!langs** *to list the languages available for translation.*
    **!purge** ***number of messages*** *deletes n number of messages in the channel it's summoned in. (admin only command)*
    """
            await message.channel.send(helpMessage)
        
        #Google search command
        if message.content[:8] == "!google ":
            await discord.User.trigger_typing(message.channel)
            query = message.content.replace('!google ', '')
            for result in search(query, tld="co.in", num=1, stop=1, pause=0.5):
                await message.channel.send(result)
        
        #Youtube search command
        if message.content[:9] == "!youtube ":
            await discord.User.trigger_typing(message.channel)
            query = message.content.replace('!youtube ', '')
            for result in search(query, tld="co.in", domains=['youtube.com'], num=1, stop=1, pause=0.5):
                await message.channel.send(result)

        #mcstatus Olim One Studios server status command    
        if message.content[:9] == "!mcstatus":
            await discord.User.trigger_typing(message.channel)
            if message.guild == client.get_guild(537377952581812224): #if guild is Olim One Studios.
                await message.channel.send("This feature is not available for this server.")
            elif message.guild == client.get_guild(593954944059572235): #if guild is Xenon MC 
                status = MinecraftServer.lookup("172.10.17.177:25565")
                try:
                    status = status.status()
                    await message.channel.send("Xenon JE is online with {0} player(s) and a ping of {1}.".format(status.players.online, status.latency))
                except Exception:
                    await message.channel.send("Xenon JE is either offline or unavailable at the moment.")

        #English to pirate speak command
        if message.content[:6] == "!arrr ":
            english = message.content.replace('!arrr ', '')
            pirateSpeak = arrr.translate(english)
            await message.channel.send(pirateSpeak)

        #Yandex Translate command
        if message.content[:11] == "!translate ":
            await discord.User.trigger_typing(message.channel)
            from_lang = message.content[11:13]
            to_lang = message.content[14:16]
            tr.set_from_lang(from_lang)
            tr.set_to_lang(to_lang)
            to_lang = "{0} ".format(to_lang)
            from_lang = "{0} ".format(from_lang)
            if not message.content[16:] == '':
                tr.set_text(message.content[16:])
                await message.channel.send(tr.translate())
        
        #List languages that can be translated between
        if message.content[:6] == "!langs":
            await message.channel.send("http://172.10.17.177/images/langs.png")

        #purge messages command
        if message.content[:7] == "!purge ":
            for admin in admins:
                if message.author.id == admin:
                    await message.delete()
                    await message.channel.purge(limit=int(message.content.replace('!purge ', '')))

@client.event
async def on_member_join(member):
    #check to see if member has joined Olim One Studios guild.
    if member.guild == client.get_guild(537377952581812224):
        channel = client.get_channel(537377952581812226)
        await channel.send(randomChoice(userWelcomes).format(member.mention, client.get_channel(538844326692651028).mention))

    #check to see if member has joined XenonMC guild.
    if member.guild == client.get_guild(593954944059572235):
        channel = client.get_channel(593988932564418590)
        await channel.send(xenonMC1.format(member.mention, client.get_channel(593999836647391252).mention, client.get_channel(593973607160348682).mention, client.get_channel(593997092234461194).mention))
    
@client.event
async def on_member_remove(member):
    #check to see if member has joined Olim One Studios guild.
    if member.guild == client.get_guild(537377952581812224):
        channel = client.get_channel(537377952581812226)
        await channel.send(randomChoice(userGoodbyes).format(member.mention))

    #check to see if member has joined XenonMC guild.
    if member.guild == client.get_guild(593954944059572235):
        channel = client.get_channel(593988932564418590)
        await channel.send(xenonMC2.format(member.display_name))

client.run(discordToken)
