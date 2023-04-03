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
        #self.performance = self.scene['performance']
        self.performance = 0
        self.point = self.SetPoint()
        self.num = uuid.uuid1().hex

        self.GetResources()
        #self.GetCarrying()

    #find a distribution based on a meanv value and the 95% confidence interval
    def GetCarryingNew(self, mean, lower, upper):
        #find a distribution based on a meanv value and the 95% confidence interval
        #generate a probability density functition 
        pPred = mean
        pLow = lower
        pUpper = upper
        pSD = (pUpper - pPred) / 1.96
        



    
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

        high = 0
        total = 0

        if self.scene["mode"] == "pole":
            high = random.uniform(self.scene["perchLow"], self.scene["perchHigh"])
            total = random.uniform(self.scene["totalLow"], self.scene["totalHigh"])


        #use snags
        elif self.scene["mode"] == "snag":
            branchFunction = -1
            perchFunction = -1 

            if self.scene["no"] == 6:
                branchFunction = self.scene["distributions"]["branchDist"]
                perchFunction = self.scene["distributions"]["perchDist"]
            
            #use snags but retain branches
            elif self.scene["no"] == 7 or self.scene["no"] == 8:
                branchFunction = self.scene["distributions"]["weightedBranchDist"]
                perchFunction = self.scene["distributions"]["weightedPerchDist"]

            
            total = sum(branchFunction.rvs(1))
            high = sum(perchFunction.rvs(1))

        self.resourcesThisYear.update({
        'high' : high,
        'dead' : 0,
        'total' : total,
        'lateral' : 0,
        'low' : 0,
        'medium' : 0,
        'carrySuit' : 0})

        print(f"artificial agent with {self.resourcesThisYear['high']}m perches and {self.resourcesThisYear['total']}m total branches")



    
    """def GetResources(self):

        self.resourcesThisYear.update({
        'high' : self.scene["suitLengths"] * self.performance,
        'dead' : self.scene["suitLengths"],
        'total' : self.scene["totalLengths"],
        'lateral' : 0,
        'low' : 0,
        'medium' : 0})"""


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


