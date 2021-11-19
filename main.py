# Discord.py library
import discord 
# parse JSON
import json
# Make HTTP requests
import requests

# Intializing the discord client
client = discord.Client()

""" Register an event 

    Discord.py is an asynchonous library
    So things are done using callbacks 
    A callback is a function that is called when something else happens
    The event function names are from the discord.py lib

"""
def startBot():
    f = open('environment.JSON')
    data = json.load(f)
    botInfo = data["bot"]
    botToken = botInfo["token"]
    # Run the Bot
    client.run(botToken)

def get_random_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


@client.event
async def on_ready():
    print('System Initialized: {0.user}'.format(client))

@client.event
async def on_message(message):

    # Return if the message is sent from the bot itself
    if message.author == client.user:
        return 
    
    if message.content.startswith('|'):

        msg = message.content[1:]

        if msg.lower() == 'ping':
            await message.channel.send('PONG')

        if msg.lower() == 'quote':
            quote = get_random_quote()
            await message.channel.send(quote)

startBot()