import json
from os import name
from numpy import result_type
# Make HTTP requests
import requests
# Handle Random numbers
import random

import pandas as pd

from libs import AgentRandomizer as agentSelector, TieBreaker as tieBreaker
# import AgentRandomizer as agentSelector, TieBreaker as tieBreaker

def get_random_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def get_random_mars_photos(count, token):

    URI = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={}'.format(token)
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
    a = agentSelector.randomize(players).to_markdown(tablefmt="pipe")
    return "```" + str(a) + "```"

def nasa(countStr, token, botKeyword):
    try:
        count = int(countStr)
    except:
        return "The command format is: {}mars(#) where # is a number between 1 and 5".format(botKeyword)
    
    if count > 0 and count <= 5:
        photos = get_random_mars_photos(count, token)
        return photos
    else:
        return "Number must be between 1 and 5"

def breakTie(players):
    return tieBreaker.breakTie(players)
def coinFlip(message = ""):
    if len(message) > 0:
        m = message.split(" ")
        return tieBreaker.coinFlip(m)
    return tieBreaker.coinFlip()
def shuffle(message=""):
    m = [x for x in set(message.split(" ")) if x != ""]
    if len(m) < 2: return "Provide at least 2 entities to shuffle."
    a = pd.DataFrame(tieBreaker.shuffle(m), columns=["Entity"])
    a.index.name = "Order"
    return "```" + str(a.to_markdown(tablefmt = "pipe")) + "```"
def rollDice(count = 1):
    k = tieBreaker.rollDice(count)
    return k if len(k) > 1 else k[0]
def cap(message):
    result = tieBreaker.coinFlip([":billed_cap:", ":man_gesturing_no: :billed_cap:"])
    if len(message) == 0:
        return result
    else:
        m = [x for x in set(message.split(" ")) if x != ""][0]
        return m + " is " + result + "-ping"