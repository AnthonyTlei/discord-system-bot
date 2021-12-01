import numpy as np
import pandas as pd
from numpy.random import default_rng
import json
import im as renderer



rng = default_rng()

exceptions = {'Pyro DMG Bonus%',
        'Electro DMG Bonus%','Cryo DMG Bonus%','Hydro DMG Bonus%','Anemo DMG Bonus%','Geo DMG Bonus%',
        'Physical DMG Bonus%', 'Healing Bonus%'}

subStatChances = pd.read_json("libs/artifact-simulator/sub.json").fillna(0)
mainStatChances = pd.read_json("libs/artifact-simulator/main.json").fillna(0)
values = pd.read_json("libs/artifact-simulator/values.json").fillna(0)

def gen(specifiedType = None, lines=None):
    artifact = {"Stat":{}, "Value":{}}
    a = rng.choice(mainStatChances.columns) if specifiedType == None else specifiedType
    myType = mainStatChances[a][mainStatChances[a] > 0] * 100
    stat = getStat(myType)
    artifact["Stat"]["mainStat"] = stat
    tempName = myType.name

    if myType.name == "Circlet":
        if stat in ['Crit Rate%', 'Crit DMG%']:
            tempName +="Crit"
        elif stat in 'Healing Bonus%':
            tempName += 'HB'
        else :
            tempName += "Normal"
    elif myType.name == "Goblet":
        if stat in ['ATK%', 'HP%', 'DEF%', 'Elemental Mastery', 'Energy Recharge%']:
            tempName +="NonEl"
        else :
            tempName += "El"

    artifact["Stat"]["type"] = tempName
    artifact["Value"]["type"] = 0

    artifact["Value"]["mainStat"]= values.loc[stat, "mainStat"][0]
    value = ""
    try :
        value = subStatChances[tempName].drop(stat)
    except:
        value = subStatChances[tempName]
        if tempName == "GobletEl" or tempName == "CircletHB":
            for x in exceptions:
                if x in value: value = value.drop(x)
    lineDecider = rng.choice([3,3,3,4]) if lines == None else lines
    for r in range(lineDecider):
        s = getStat(value)
        value = value.drop(s)
        artifact["Stat"]["sub" + str(r+1)] = s
        artifact["Value"]["sub" + str(r+1)] = rng.choice(values.loc[s, "subStat"])
    return pd.DataFrame(artifact)

def getStat(myType):
    z = np.empty(np.sum(myType.values, dtype= np.int32), dtype= object)
    j = 0
    for (x,y) in zip(myType.index, myType.values):
        temp = 0
        for p in np.arange(int(y)):
            z[j+p] = x
            temp +=1
        j += temp
    stat = rng.choice(z)
    return stat

def upgrade(artifact):
    if artifact.loc["type", "Value"] >= 20: return artifact
    artifact.loc["type", "Value"] += 4
    artifact.loc["mainStat", "Value"] = values.loc[artifact.loc["mainStat", "Stat"], "mainStat"][int(artifact.loc["type", "Value"] / 4)]
    if "sub4" not in artifact.index:
        aName = artifact.loc["type", "Stat"]
        v = ""
        try :
            v = subStatChances[aName].drop(artifact.loc["mainStat", "Stat"]) 
        except:
            v = subStatChances[aName]
            if aName == "GobletEl" or aName == "CircletHB":
                for x in exceptions:
                    if x in v: v = v.drop(x)
        for k in [artifact.loc["sub1":, "Stat"]]:
            v = v.drop(k)

        s = getStat(v)
        k = artifact.to_dict()
        k['Stat']["sub4"] = s
        k['Value']["sub4"] = rng.choice(values.loc[s, "subStat"])
        return pd.DataFrame(k)
    else:
        r = "sub" + str(rng.choice([1,2,3,4]))
        artifact.loc[r, "Value"] += rng.choice(values.loc[artifact.loc[r, "Stat"], "subStat"])
        return artifact

def save_artifact(artifact: pd.DataFrame, position = -1):
    s = json.dumps(artifact.to_dict())
    if position < 0:
        with open("libs/artifact-simulator/artifacts.json",'r+') as file:
            file_data = json.load(file)
            k = 0
            if len(file_data) > 0:
                k = int(list(file_data.keys())[-1]) + 1
                file_data[k] = s
            else:
                file_data[len(file_data)] = s
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    else:
        removeArtifact(str(position))
        with open("libs/artifact-simulator/artifacts.json",'r+') as file:
            file_data = json.load(file)
            file_data[position] = s
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    return s

def retrieveArtifact(pos = -1):
    data = {}
    arr = []
    with open("artifacts.json", "r") as file:
        data = json.load(file)
    if pos < 0:
        for x in data:
            arr.append(pd.read_json(data[x]))
        return arr
    else:
        return pd.read_json(data[str(pos)])

def removeArtifact(position = -1):
    data = {}
    k = None
    with open('libs/artifact-simulator/artifacts.json', 'r') as data_file:
        data = json.load(data_file)
    if position < 0:
        i = data.copy()
        count = 0
        for count,j in enumerate(i):
            data.pop(j)
        k = "Artifacts removed :" + str(count)
    else:
        try:
            k= data[str(position)]
            data.pop(str(position))
        except:
            return "No artifact at this position"
    with open('libs/artifact-simulator/artifacts.json', 'w') as data_file:
        data = json.dump(data, data_file)
    return k

def returnSpecific(mySet, countOnly= False, aType=None, main= None):
    arr = []
    for x in retrieveArtifact():
        if set(mySet).issubset(set(x.loc["sub1":, "Stat"].values)):
            if aType == None:
                if main == None:
                    arr.append(x)
                else:
                    if main in x.loc["mainStat", "Stat"]: arr.append(x)
            else:
                if aType in x.loc["type", "Stat"]:
                    if main == None:
                        arr.append(x)
                    else:
                        if main in x.loc["mainStat", "Stat"]: arr.append(x)
    return arr if countOnly == False else len(arr)

def upgradeMax(artifact):
    for i in range(5):
        artifact = upgrade(artifact)
    return artifact

def reRoll(artifact, subs, numbers, tries = 0):
    temp = artifact.copy()
    max = upgradeMax(artifact)
    if not (set(subs).issubset(set(max.loc["sub1":, "Stat"].values))):
        tries +=1
        reRoll(temp, subs, numbers, tries)
    else:
        for (stat, num) in zip(subs, numbers):
            if max[max.Stat == stat].Value[0] >= num:
                continue
            else:
                tries +=1
                return reRoll(temp, subs, numbers, tries)
    return [max, tries+1]

def reset(count = 0):
    removeArtifact()
    if count > 0:
        for i in range(count):
            save_artifact(gen())
    else : removeArtifact()