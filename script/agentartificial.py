import csv
import os

import settings as settings

import numpy as np
from pyparsing import dblSlashComment
from scipy import rand
from scipy.interpolate import interp1d
from scipy.sparse.construct import random
import scipy.stats as stats
from enum import Enum
import random
from scipy.stats import truncnorm

import itertools

from codetiming import Timer

# generate random integer values
from random import seed
from random import randint

# seed random number generator
seed(1)

import pandas as pd



class ArtificialAgent:
    performance = 0
    lifespan = settings.ARTLIFE
    resources = {}
    resourcesThisYear = {}
    age = 0
    constrictor = 1
    isAlive = True


    def __init__(self, perf, geo):
        
        self.performance = perf
        self.point = self.SetPoint(geo)
        self.resources = {}

        for resource in settings.RESOURCES:
                  
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

            self.resources.update({resource : meters * self.performance})

            if resource == 'high':
                print(f"Old Tree has: {meters}m \t Artificial Performance is: {self.performance}% \t Artificial Structure Has: {self.resources['high']}m")

    def GrowOld(self):
        self.age += 1
        
        if self.age > self.lifespan:
            self.isAlive = False

    def SetPoint(self, geo):
        """x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        z = random.uniform(50, 100)

        return [x,y,z]"""

        _point = geo.GetPoint()
        return _point