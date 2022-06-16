from scipy.sparse.construct import random
import random

# generate random integer values
from random import seed
from random import randint

# seed random number generator
seed(1)


import pandas as pd

import settings.setting as settings
from settings.resourcecurves import *
from settings.geometry import *

class TreeAgent:

    age = 0.0
    exactDbh = settings.TREESTARTDBH
    dbh = int(round(exactDbh))
    isAlive = True
    lifespan = randint(settings.TREELIFESPAN[0], settings.TREELIFESPAN[1])

    resources = {}
    resourcesThisYear = {}

    def __init__(self):

        self.resources = {}
        self.resourcesThisYear = {}
        self.point = self.SetPoint()
       
        for name in settings.RESOURCES:

            self.resources.update({name : []})
        
    
    def NextYear(self):
            if self.dbh >= settings.MAXDBH:
                self.dbh = settings.MAXDBH
                grow = 0
            else: 
                grow = self.GrowRate()
                
            self.age += 1
            self.exactDbh += grow
            self.dbh = round(self.exactDbh)
            return grow
        

    def ChanceDeath(self):
        deathChance = random.uniform(settings.deathLow, settings.deathHigh)

        #print(settings.deathHigh)
            
        value = random.uniform(0, 1)

        if value <= deathChance:
            self.isAlive = False
        #print(f'tree alive is {self.isAlive} as value is {value}, death chance is {deathChance}')


        if self.age > self.lifespan:
            self.isAlive = False



        return deathChance

    def GrowRate(self):       
        growRate = randint(settings.TREEGROWRATE[0], settings.TREEGROWRATE[1]) / 100
        return 1 * (1 / growRate)

    """def SetPoint(self):
        x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        z = random.uniform(50, 100)

        return [x,y,z]"""

    def SetPoint(self):
        _point = GeoGetPoint()
        return _point