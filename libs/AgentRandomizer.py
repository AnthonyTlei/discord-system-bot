import numpy as np
from numpy.random import default_rng
import pandas as pd
from pandas import Series, DataFrame

agents = ['Astra', 'Breach', 'Brimstone', 'Cypher', 'Jett', 'Killjoy', 'Omen', 'Phoenix', 'Raze', 'Reyna', 'Sage', 'Skye', 'Sova', 'Viper', 'Yoru']

def randomize(players):
    participants = players.split(" ")

    if len(participants) > 5:
        return "Number of players cannot exceed 5"

    rng = default_rng()
    choices = rng.choice(len(agents), size = len(participants), replace = False)
    return DataFrame(list(zip(participants, [agents[k] for k in choices])), columns=("Player", "Agent"))
