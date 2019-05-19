import discord
import arrr
from mcstatus import MinecraftServer
from yandex.Translater import Translater as Translator

#discord config
client = discord.Client()
discordToken = 'Discord Token'

#mcstatus config
serverOnline = True
try:
    server = MinecraftServer.lookup("172.10.17.177:25565")
    status = server.status()
except Exception:
    serverOnline = False
    pass

#Yandex.Translate config
tr = Translator()
tr.set_key('Yandex.translate API key')

@client.event
async def on_ready():
    try:
        #print bot information
        print(client.user.name)
        print(client.user.id)
        print("Successfully connected to Discord!")
        
    except Exception as e:
        #print the error
        print(e)

@client.event
async def on_message(message):
    print(message.content) #print message content
    #Help command
    if message.content[:5] == "!help":
        helpMessage = """__Olim One Studios Bot Commands:__
**!help** *to display this help message and view the bot commands.*
**!web** ***search*** *to search the web with google.*
**!mcstats** *to check the official Minecraft server statistics.*
**!arrr** ***text** *to speak like a pirate!*
**!translate** ***from*** ***to*** ***text*** *to translate between languages.*
**!langs** *to list the languages available for translation*
"""
        await message.channel.send(helpMessage)
    
    #Google search command
    if message.content[:4] == "!web ":
        query = message.content.replace('!web ', '').replace(' ', '+')
        googleurl = "https://www.google.com/search?q={0}".format(query)
        await message.channel.send(googleurl)

    #mcstatus Olim One Studios server status command
    if message.content[:9] == "!mcstats":
        if serverOnline == True:
            status = server.status()
            serverstats = "{0} players are on the Minecraft server and the server ping is {1} milliseconds.".format(status.players.online, status.latency)
            await message.channel.send(serverstats)
        else:
            await message.channel.send("The Minecraft server is currently offline.")

    #English to pirate speak command
    if message.content[:5] == "!arrr ":
        english = message.content.replace('!arrr ', '')
        piratespeak = arrr.translate(english)
        await message.channel.send(piratespeak)

    #Yandex Translate command
    if message.content[:11] == "!translate ":
        from_lang = message.content[11:13]
        to_lang = message.content[14:16]
        tr.set_from_lang(from_lang)
        tr.set_to_lang(to_lang)
        to_lang = "{0} ".format(to_lang)
        from_lang = "{0} ".format(from_lang)
        tr.set_text(message.content[16:])
        await message.channel.send(tr.translate())
    
    #List languages that can be translated between
    if message.content[:7] == "!langs":
        await message.channel.send("http://172.10.17.177/images/langs.png")     
        
client.run(discordToken)
