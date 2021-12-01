# Discord.py library
import discord 
# parse JSON
import json
# Local Libraries
from libs import botFunctions as botFuncs

# Intializing the discord client
client = discord.Client()

""" Register an event 

    Discord.py is an asynchonous library
    So things are done using callbacks 
    A callback is a function that is called when something else happens
    The event function names are from the discord.py lib

"""

botKeyword = "-"
envData = {}
tokens = {}
commands = {}

def startBot():
    with open("environment.json",'r+') as file:
        global envData
        envData = json.load(file)

    with open("commands.json",'r+') as file:
        global commands
        commands = json.load(file)

    tokens["NASA"] = envData["api"]["nasa"]
    tokens["Bot"] = envData["bot"]["token"]

    client.run(tokens["Bot"])

def get_random_quote():
    return botFuncs.get_random_quote()

def get_random_mars_photos(countStr):
    return botFuncs.nasa(countStr, tokens["NASA"], botKeyword)
def select_random_agents(players):
    return botFuncs.select_random_agents(players)
def breakTie(players):
    return botFuncs.breakTie(players)
def coinFlip(message=""):
    return botFuncs.coinFlip(message)
def shuffle(message = ""):
    return botFuncs.shuffle(message)
def rollDice(count = 1):
    return botFuncs.rollDice(count)
def cap(message = ""):
    return botFuncs.cap(message)
def ping():
    return botFuncs.ping()
def generate_artifact():
    with open(botFuncs.generate_artifact(), 'rb') as f:
        return discord.File(f)

@client.event
async def on_ready():
    print('System Initialized: {0.user}'.format(client))

@client.event
async def on_message(message):

    # Return if the message is sent from the bot itself
    if message.author == client.user:
        return 

    if "good boi" in message.content.lower() :
        if message.author.id in [323805449067560960, 709779444411138108]:
            await message.channel.send("Thank you master")
            return 
        else:
            await message.channel.send("Know your place, peasant")
            return
    
    if message.content.startswith(botKeyword):

        msg = message.content[1:]

        if msg.lower() == 'help':
            response = "..."
            await message.channel.send(response)

        if msg.lower() == 'generate-artifact':
            response = generate_artifact()
            await message.channel.send(file=response)
            return

        for command in commands:
            if command in msg.lower():
                print(command)
                func = globals()[commands[command]]
                param = msg.lower()[len(command)+1: -1]
                try:
                    if len(param) > 0:
                        if isinstance(func(param), str):
                            await message.channel.send(func(param))
                        else:
                            for m in func(param):
                                await message.channel.send(m)
                    else:
                        await message.channel.send(globals()[commands[command]]())
                except:
                    await message.channel.send("Make sure your command exists and is written correctly.")
                break

startBot()

