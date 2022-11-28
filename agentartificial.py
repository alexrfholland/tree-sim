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



                
        """for resource in RESOURCES:
                  
            dbh = 100

            pred = DPREDICTIONS[resource]
            low = DLOWS[resource]
            up = DUPS[resource]
            standard = DSTANDARDS[resource]
            
            #generate a probability density functition  at this DBH for this resource
            
            pPred = pred(dbh)
            pLow = low(dbh)
            pUpper = up(dbh)

            pSD = standard(dbh)/self.constrictor

            distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)



            #get how many trees there are and generate lengths via probbility density function
            noOfTrees = 1

            #need to sum meters as it returns a list, even though we are only finding for 1 artificial structure
            meters = sum(distributionFunction.rvs(noOfTrees))

            if meters < 0:
                meters = 0

            self.resourcesThisYear.update({resource : meters * self.performance})"""

    
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


