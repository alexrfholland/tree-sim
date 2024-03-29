import pandas as pd


SCENARIOS = ['intact','existing','replanting','prosthetics']



import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import List
from typing import Dict
import random
import newArtificialPropabilityFunctions as probFunctions

def GetModes(no, budget):

    temp = pd.read_csv("/Users/alexholland/Coding/tree-sim/data/model-infos/updated-sustainability/artificial-distributions.csv")
    stats =  temp.iloc[no].to_dict()
    stats.update({"distributions" : probFunctions.GetProbabilityFunctions(),
                "samplingType" : "notUsed"})


    if stats["mode"] != "tree":
        treeStats = temp.iloc[2].to_dict()

        stats.update({'treeCostLow' : treeStats["costLow"],
                      'treeCostHigh' : treeStats["costHigh"]})
        


    else:
        treeStats = temp.iloc[no].to_dict()

        stats.update({'treeCostLow' : treeStats["costLow"],
                      'treeCostHigh' : treeStats["costHigh"]})



    

    
    print(stats)
    return(stats)



def GetNumberInBudget(budget, low, high):
    noStructures = 0
    while budget > 0:
        noStructures = noStructures + 1
        cost = random.uniform(low, high)
        budget = budget - cost
        print(f'cost is ${cost}')

    print(f'no structures is {noStructures}')
    return noStructures




"""def GetArtificial(i, path, budget):
    df = pd.read_csv(path)
    dic = df.to_dict(orient='index')
    row = dic[i]
    row.update({"isRecruit" : True,
                "isArtificials" : True,
                "isExistingTrees" : False,
                "artNo" : round(budget/row['cost']),
                "oldID" : row['id']})
    row["id"] = f"{row['id']} - {row['samplingType']}"
    print(row)
    return(row)
"""
   








def UpdateForScenarios():
    #INTACT
    #death  figures from 'our proposal' in Table 1 of Gibbons et al., “The Future of Scattered Trees in Agricultural Landscapes.”
    
    """settings.scenario = "Intact"
    settings.modelRecruit = True
    settings.modelProsthetics = False
    settings.existingTrees = True
    settings.deathHigh = 0.010
    settings.deathLow = 0.003"""

    #30: 2032, 44: 1668, 56: 1389, 70: 1120, 83: 917, 96: 773, 109: 642, 121: 526

    #EXISTING
    """settings.scenario = "Business-As-Usual"
    settings.modelRecruit = False
    settings.modelProsthetics = False
    settings.existingTrees = False
    settings.deathHigh = 0.035"""


    #REPLANTING
    """settings.scenario = "Continuous Replanting"
    settings.modelRecruit = True
    settings.modelProsthetics = False
    settings.existingTrees = False"""
"""
   
def SetScenarios(name):

    scenes = {}

    scenario = "Not set"
    serviceLife =  -1
    lifeVariation = -1
    mortality = -1
    length = -1
    deadlateral = -1
    performance = -1
    cost = -1

    maxPerformance = -1

    improveRate = 0
    improveInterval = 5
    isRecruit = True
    isArtificials = True
    isExistingTrees = False

    scenarios = [
            'p1',
            'p2',
            'p3',
            's1',
            's2',
            's3',
            's4',
            's5'
            ]

    #VBA POLE

    if name == scenarios[0]:
        scenario = 'VBA Pole'
        serviceLife = 25
        lifeVariation = 0.2
        mortality = 0
        performance = .12
        cost = 1524.06
        length = 13
        deadlateral = 3.5 
        performance = .12

    #CONCRETE POLE
        
    
    elif name == scenarios[1]:
        scenario = 'Concrete Pole'
        serviceLife = 50
        lifeVariation = 0.17
        mortality = 0
        length = 13
        deadlateral = 3.5 
        performance = .12
        cost = 2243.32

    #CUSTOM POLE
        
    elif name == scenarios[2]:
        scenario = 'Custom Pole'
        serviceLife = 25
        lifeVariation = 0.2
        mortality = 0
        length = 13
        deadlateral = 3.5 
        performance = .12
        cost = 16815 

    
    #SNAG1
    if name == scenarios[3]:
        scenario = 'Snag 1'
        serviceLife = 50
        lifeVariation = 0.2
        mortality = 0
        length = 45
        deadlateral = 3
        performance = .29
        cost = 24294

    #SNAG2
    elif name == scenarios[4]:
        scenario = 'Snag 2'
        serviceLife = 50
        lifeVariation = 0.2
        mortality = 0
        length = 75
        deadlateral = 2 
        performance = .29
        cost = 24294

    #SNAG3
    elif name == scenarios[5]:
        scenario = 'Snag 3'
        serviceLife = 50
        lifeVariation = 0.2
        mortality = 0
        length = 105
        deadlateral = 25 
        performance = .29
        cost = 24294

    #SNAG4
    elif name == scenarios[6]:
        scenario = 'Snag 4'
        serviceLife = 50
        lifeVariation = 0.2
        mortality = 0
        length = 105
        deadlateral = 25 
        performance = .29
        cost = 24294/2
        
        

    #SNAG - LEARNING
    elif name == scenarios[7]:
        scenario = 'Snag - Learning'
        serviceLife = 50
        lifeVariation = 0.2
        mortality = 0
        length = 13
        deadlateral = 3.5 
        performance = .29
        maxPerformance = .84
        cost = 24294

        improveRate = 0.01


    scenes.update(
            {'scenario' : scenario, 
            'serviceLife' : serviceLife, 
            'lifeVariation' : lifeVariation,
            'mortality' : mortality,
            'performance' : performance,
            'maxPerformance' : maxPerformance,
            'cost' : cost,
            'improveRate' : improveRate,
            'isRecruit' : isRecruit,
            'isArtificials' : isArtificials,
            'isExistingTrees' : isExistingTrees,
            'improveInterval' : improveInterval,
            'length' : length,
            'deadlateral' : deadlateral}
            )

    print(scenario)
    return(scenes)

"""



"""#PROSTHETICS
settings.scenario = "Replanting and Prosthetics"
settings.modelRecruit = True
settings.modelProsthetics = True
settings.existingTrees = False"""


