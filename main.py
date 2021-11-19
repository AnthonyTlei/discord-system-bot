# Discord.py library
import discord 
# parse JSON
import json
# Make HTTP requests
import requests
# Handle Random numbers
import random

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

def get_random_mars_photo():
    
    URI = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={}'.format(nasaToken)
    response = requests.get(URI)
    json_data = json.loads(response.text)
    photos = json_data["photos"]

    random_photo_index = random.randint(0, len(photos))
    random_photo_object = photos[random_photo_index]
    random_photo_URL = random_photo_object['img_src']

    return random_photo_URL


@client.event
async def on_ready():
    print('System Initialized: {0.user}'.format(client))

@client.event
async def on_message(message):

    # Return if the message is sent from the bot itself
    if message.author == client.user:
        return 
    
    if message.content.startswith('<'):

        msg = message.content[1:]

        if msg.lower() == 'ping':
            await message.channel.send('PONG')

        if msg.lower() == 'quote':
            quote = get_random_quote()
            await message.channel.send(quote)

        if msg.lower() == 'mars':
            photo = get_random_mars_photo()
            await message.channel.send(photo)

startBot()