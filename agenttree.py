from scipy.sparse.construct import random
import random

# generate random integer values
from random import randint

import uuid

import pandas as pd

import setting as settings
from resourcecurves import *
from geometry import *

class TreeAgent:

    def __init__(self):

        self.yearborn = -1
        self.yeardeath = -1

        self.age = 0.0
        self.exactDbh = settings.TREESTARTDBH
        self.dbh = int(round(self.exactDbh))
        self.isAlive = True
        self.lifespan = randint(settings.TREELIFESPAN[0], settings.TREELIFESPAN[1])

        self.resources = {}
        self.resourcesThisYear = {}

        self.hResources = {}
        self.hAge = {}
        self.hPerf = {}
        self.num = uuid.uuid1().hex
        self.resources = {}
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
        

    def KillTree(self, year):
        self.isAlive = False
        self.yeardeath = year
    
    def CheckIfTooOld(self, year):
        if self.age > self.lifespan:
            self.KillTree

    

    
    """def ChanceDeath(self, year):
        deathChance = random.uniform(settings.deathLow, settings.deathHigh)
            
        value = random.uniform(0, 1)

        if value <= deathChance:
            self.isAlive = False
            self.yeardeath = year
        
        #print(f'tree alive is {self.isAlive} as value is {value}, death chance is {deathChance}')


        if self.age > self.lifespan:
            self.isAlive = False
            self.yeardeath = year



        return deathChance"""

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