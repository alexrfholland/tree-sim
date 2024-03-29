import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import List
from typing import Dict
import random



def GetWeights(value, weight):
    return (value - (value * weight))

def GetVals(densityFunction, no):
    vals = []
    for i in range (0, no):
        #need to sum meters as it returns a list, even though we are only finding for 1 artificial structure
        numb = sum(densityFunction.rvs(1))

        if numb < 0:
            numb = 0

        vals.append(numb)
    return vals
    

def GetProbabilityFunctions():
        
        temp = pd.read_csv("/Users/alexholland/Coding/tree-sim/data/model-infos/updated-sustainability/snag-distributions.csv")
        totals = temp.iloc[0].to_dict()
        perches = temp.iloc[1].to_dict()

        print(perches)
        print(totals)
        
        densityfunctions: Dict[str, ] = {}


        #generate a probability density functition for perches
        pPred = perches['mean']
        pLow = perches['low']
        pUpper = perches['high']
        pSD = perches['sd']
        
        perchDistributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)
        densityfunctions.update({'perchDist' : perchDistributionFunction})


        #generate a weighted probability density functition for perches
        pPred = GetWeights(perches['high'], 0.2)
        pLow = perches['low']
        pUpper = perches['high']
        pSD = perches['sd']/2
        
        weightedPerchDistributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)
        densityfunctions.update({'weightedPerchDist' : weightedPerchDistributionFunction})


        #generate a probability density functition for branches

        pPred = totals['mean']
        pLow = totals['low']
        pUpper = totals['high']
        pSD = totals['sd']

        branchDistributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)
        densityfunctions.update({'branchDist' : branchDistributionFunction})


        #generate a weighted probability density functition for branches

        pPred = GetWeights(totals['high'], 0.2)
        pLow = totals['low']
        pUpper = totals['high']
        pSD = totals['sd']/2

        weightedBranchDistributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)
        densityfunctions.update({'weightedBranchDist' : weightedBranchDistributionFunction})

        return densityfunctions



    







