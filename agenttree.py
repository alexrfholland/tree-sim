from scipy.sparse.construct import random
import random

# generate random integer values
from random import seed
from random import randint

# seed random number generator
seed(1)


import pandas as pd

from settings.setting import *
from settings.resourcecurves import *
from settings.geometry import *

class TreeAgent:

    age = 0.0
    exactDbh = TREESTARTDBH
    dbh = int(round(exactDbh))
    isAlive = True
    lifespan = randint(TREELIFESPAN[0],TREELIFESPAN[1])

    resources = {}
    resourcesThisYear = {}

    def __init__(self):

        self.resources = {}
        self.resourcesThisYear = {}
        self.point = self.SetPoint()
       
        for name in RESOURCES:

            self.resources.update({name : []})
        
    
    def NextYear(self):
            if self.dbh > 145:
                self.dbh = 145
                grow = 0
            else: 
                grow = self.GrowRate()
                
            self.age += 1
            self.exactDbh += grow
            self.dbh = round(self.exactDbh)
            return grow
        

    def ChanceDeath(self):
        deathChance = random.uniform(DEATHLOW, DEATHHIGH)

        value = random.uniform(0, 1)
        if value <= deathChance:
            self.isAlive = False

        if self.age > self.lifespan:
            self.isAlive = False

        return deathChance

    def GrowRate(self):       
        growRate = randint(TREEGROWRATE[0], TREEGROWRATE[1]) / 100
        return 1 * (1 / growRate)

    """def SetPoint(self):
        x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        z = random.uniform(50, 100)

        return [x,y,z]"""

    def SetPoint(self):
        _point = GeoGetPoint()
        return _point