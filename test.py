import numpy as np
import pandas as pd
import scipy.stats as stats

temp = pd.read_csv("/Users/alexholland/Coding/tree-sim/data/model-infos/updated-sustainability/snag-distributions.csv")

totals = temp.iloc[0].to_dict()
perches = temp.iloc[1].to_dict()
print (perches)

def GetCarrying():
        
        #generate a probability density functition
        pPred = perches['mean']

        newMean = perches['high'] - (perches['high']*0.2)
        print(newMean)
        pPred = newMean
        pLow = perches['low']
        pUpper = perches['high']
        pSD = perches['sd']/2
        

        distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)

        #need to sum meters as it returns a list, even though we are only finding for 1 artificial structure
        capacity = sum(distributionFunction.rvs(1))

        if capacity < 0:
            capacity = 0

        print (f'capacity artificial is {capacity}')
        return capacity

sums = []

for i in range(0, 10):
    sums.append(GetCarrying())

print(sum(sums))

