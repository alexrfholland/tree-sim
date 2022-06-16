from scipy.sparse.construct import random
import scipy.stats as stats



from settings.setting import *
from settings.resourcecurves import *
from settings.geometry import *


class ArtificialAgent:
    performance = 0
    lifespan = ARTLIFE
    resourcesThisYear = {}
    age = 0
    constrictor = 1
    isAlive = True


    def __init__(self, perf):
        
        self.performance = perf
        self.point = self.SetPoint()
        self.resourcesThisYear = {}

        for resource in RESOURCES:
                  
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

            self.resourcesThisYear.update({resource : meters * self.performance})

            if resource == 'high':
                if DEBUG == True:
                    print(f"Old Tree has: {meters}m \t Artificial Performance is: {self.performance}% \t Artificial Structure Has: {self.resourcesThisYear['high']}m")

    def GrowOld(self):
        self.age += 1
        
        if self.age > self.lifespan:
            self.isAlive = False

    def SetPoint(self):

        _point = GeoGetPoint()
        return _point


