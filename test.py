import setting as settings
import pandas as pd
import scipy.stats as stats



for sceneNo in range(0,len(pd.read_csv(settings.ARTIFICIALINFOPATH))):
    
    settings.GetScenario(sceneNo)

    pPred = settings.scene['mean']
    pLow = settings.scene['low']
    pUpper = settings.scene['up']
    pSD = settings.scene['sd']/5

    distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)

    for i in range(0, 10):    
        #need to sum meters as it returns a list, even though we are only finding for 1 artificial structure
        capacity = sum(distributionFunction.rvs(1))

        if capacity < 0:
            capacity = 0

        print (f'{settings.scenario} capacity artificial is {capacity}')
