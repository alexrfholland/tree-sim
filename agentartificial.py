from scipy.sparse.construct import random
import scipy.stats as stats
import random



from setting import *
from resourcecurves import *
from geometry import *

import uuid

class ArtificialAgent:
    

    def __init__(self, perf):
   

        max = round(ARTLIFE + (ARTLIFE * ARTLIFEVARIATION))
        min = round(ARTLIFE - (ARTLIFE * ARTLIFEVARIATION))

        self.lifespan = random.randint(min, max)
        
        #print(f'artlife is {ARTLIFE},  artvariation is {ARTLIFEVARIATION}, lifespan min is {min}, max is {max}, lifespan is {self.lifespan}')
    

        self.resourcesThisYear = {}
        self.age = 0
        self.constrictor = 1
        self.isAlive = True

        self.newResourcesThisYear = {}

        self.hResources = {}
        self.hAge = {}
        self.hPerf = {}
        self.performance = perf
        self.point = self.SetPoint()
        self.num = uuid.uuid1().hex

        self.GetResources()
        self.GetCarrying()

    def GetCarrying(self):
        
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

        self.resourcesThisYear.update({"carrySuit" : capacity})

    
    def GetResources(self):

            self.resourcesThisYear.update({
            'high' : ARTDEADLATERAL * self.performance,
            'dead' : ARTDEADLATERAL,
            'total' : ARTLENGTH,
            'lateral' : 0,
            'low' : 0,
            'medium' : 0})


    def GrowOld(self):
        self.age += 1
        
        if self.age > self.lifespan:
            self.isAlive = False

    def Upgrade(self, currentPerf):
         self.performance = currentPerf
         self.GetResources()

    def SetPoint(self):

        _point = GeoGetPoint()
        return _point


