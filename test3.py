from scenes import *
import scipy.stats as stats


def GetCarrying():
        
        #generate a probability density functition

        

        pPred = SCENE['sMean']
        pLow = SCENE['sLow']
        pUpper = SCENE['sUp']
        pSD = SCENE['sSD']

        distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)

        #need to sum meters as it returns a list, even though we are only finding for 1 artificial structure
        capacity = sum(distributionFunction.rvs(1))

        if capacity < 0:
            capacity = 0

        print (f'capacity artificial is {capacity}')

SCENE = GetArtificial(3)
for i in range(0, 5):
    GetCarrying()



