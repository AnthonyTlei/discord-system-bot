from numpy.random import default_rng

rng = default_rng()

diceImages = [
    "https://imgur.com/POEaO9n",
    "https://imgur.com/i43BuGD",
    "https://imgur.com/cPq7mPr",
    "https://imgur.com/ViPTHG0",
    "https://imgur.com/JGOFfS8",
    "https://imgur.com/300GJxd"
]

def breakTie(players):
    p = [x for x in set(players.split(" ")) if x != ""]
    return "{} wins".format(rng.choice(p)) if len(p) >= 2 else "There has to be at least 2 participants."

def rollDice(count = 1):
    return [diceImages[rng.integers(1, 7) - 1] for x in range(int(count))]

def coinFlip(arr=["Heads", "Tails"]):
    if len(arr) != 2 : return "You must provide 2 sides to the coin"
    return rng.choice(arr)

def shuffle(arr=["You must give a list with length greater than 0"]):
    try:
        return rng.permutation(list(arr.values()) if isinstance(arr, dict) else list(arr))
    except:
        return rng.permutation(list(str(arr)))