# Discord.py library
import discord 
# parse JSON
import json
# Make HTTP requests
import requests
# Handle Random numbers
import random
# Local Libraries
from libs import AgentRandomizer as agentSelector

# Intializing the discord client
client = discord.Client()

""" Register an event 

    Discord.py is an asynchonous library
    So things are done using callbacks 
    A callback is a function that is called when something else happens
    The event function names are from the discord.py lib

"""

# Global Variables
global botKeyword

botKeyword = "-"

def startBot():

    f = open('environment.JSON')
    data = json.load(f)

    botInfo = data["bot"]
    apiInfo = data["api"]

    global botToken 
    botToken = botInfo["token"]
    global nasaToken 
    nasaToken = apiInfo["nasa"]

    print("Bot Token: " + botToken)
    print("NASA Token: " + nasaToken)

    # Run the Bot
    client.run(botToken)

def get_random_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def get_random_mars_photos(count):

    URI = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={}'.format(nasaToken)
    response = requests.get(URI)
    json_data = json.loads(response.text)
    photos = json_data["photos"]
    photos_URLs = []

    for i in range(count):
        random_photo_index = random.randint(0, len(photos))
        random_photo_object = photos[random_photo_index]
        random_photo_URL = random_photo_object['img_src']
        photos_URLs.append(random_photo_URL)

    return photos_URLs

def select_random_agents(players):
    return agentSelector.randomize(players)

@client.event
async def on_ready():
    print('System Initialized: {0.user}'.format(client))

@client.event
async def on_message(message):

    # Return if the message is sent from the bot itself
    if message.author == client.user:
        return 
    
    if message.content.startswith(botKeyword):

        msg = message.content[1:]

        if msg.lower() == 'help':
            response = "..."
            await message.channel.send(response)

        if msg.lower() == 'ping':
            await message.channel.send('PONG')

        if msg.lower() == 'quote':
            quote = get_random_quote()
            await message.channel.send(quote)

        if 'mars' in msg.lower():
            countStr = msg.lower()[5:-1]

            try:
                count = int(countStr)
            except:
                await message.channel.send("The command format is: {}mars(#) where # is a number between 1 and 5".format(botKeyword))
                return 

            if count > 0 and count <= 5:
                photos = get_random_mars_photos(count)
                for photo in photos:
                    await message.channel.send(photo)

            else:
                await message.channel.send("Number must be between 1 and 5")

        if 'select-agents' in msg.lower():
            playerListStr = msg.lower()[14:-1]
            data = select_random_agents(playerListStr)
            print(data)
            await message.channel.send(data)

startBot()

