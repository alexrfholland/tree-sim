from scipy.sparse.construct import random
import scipy.stats as stats
import random



from geometry import *

import uuid

class ArtificialAgent:
    

    def __init__(self, _scene):
   

        self.scene = _scene
        
        max = round(self.scene['serviceLife'] + (self.scene['serviceLife'] * ARTLIFEVARIATION))
        min = round(self.scene['serviceLife'] - (self.scene['serviceLife'] * ARTLIFEVARIATION))

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
        self.performance = self.scene['performance']
        self.point = self.SetPoint()
        self.num = uuid.uuid1().hex

        self.GetResources()
        self.GetCarrying()

    def GetCarrying(self):
        
        #generate a probability density functition

        pPred = self.scene['mean']
        pLow = self.scene['low']
        pUpper = self.scene['up']
        pSD = self.scene['sd']


        distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)

        #need to sum meters as it returns a list, even though we are only finding for 1 artificial structure
        capacity = sum(distributionFunction.rvs(1))

        if capacity < 0:
            capacity = 0

        #print (f"mean is {pPred} for {self.scene['id']}, capacity artificial is {capacity}")

        self.resourcesThisYear.update({"carrySuit" : capacity})

    
    def GetResources(self):

            self.resourcesThisYear.update({
            'high' : self.scene["suitLengths"] * self.performance,
            'dead' : self.scene["suitLengths"],
            'total' : self.scene["totalLengths"],
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


