from agentartificial import *
from agenttree import *
from settings.setting import *

import csv
import os
from turtle import width
from tabulate import tabulate

import termplotlib as tpl
import plotext as tplt

from signal import Sigmasks
from this import d, s
import numpy as np
from pyparsing import dblSlashComment
from scipy import rand
from scipy.interpolate import interp1d
from scipy.sparse.construct import random
import scipy.stats as stats
from enum import Enum
import random
from scipy.stats import truncnorm

import json
import itertools

from codetiming import Timer

# generate random integer values
from random import seed
from random import randint

# seed random number generator
seed(1)

from drawnow import drawnow
import matplotlib.pyplot as plt

import matplotlib.colors as colors
import matplotlib.cbook as cbook
from matplotlib import cm
from matplotlib import gridspec
from matplotlib.colorbar import Colorbar # For dealing with Colorbars the proper way - TBD in a separate PyCoffee ?


import seaborn as sns
import pandas as pd

class Model:
    size = AREA
    density = (DENSITYHIGH + DENSITYLOW)/2

    year = 0
    timeperiod = TIMEPERIOD
    recruitmentInterval = INTERVAL
    recruitmentChance = 0.2




    resourceCurves = {}
    totalResources = {}
    previousDotsX = []
    previousDotsY = []
    treesAliveThisYear = 0

    snapTotalAlive = {}
    snapMeters = {}

    resourcesSortedByDBH = {}

    trees = []
    artificials = []

    artPerf = ARTPERFMIN

    recruitMessage = UPDATEMESSAGE
    builtMesssage = UPDATEMESSAGE

    exportTree = {'year' : [], 'high' : []}
    exportPros = {'year' : [], 'high' : []}


    #yrTreeRescources and yrARtResources are hierachical dictionaries.
    # First level: key is year since sim began, value is second level:
    # Second level: YrTreeResource and YrArtResource: dictionary with resource name as key, value is a list of floats with each item in the list representing a tree

    treeResources = {}
    artResources = {}


    

    
    @Timer(name = "Finished running model in {:.2f} seconds")
    def __init__(self):
        self.year = 0

        #rivX.extend(self.geo.riverPts[:,0])
        #rivY.extend(self.geo.riverPts[:,1])


        for name in RESOURCES:
            self.artResources.update({name : []}) 

        for i in range (round(self.size * self.density)):
            tree = TreeAgent()
            self.trees.append(tree)
        
        for j in range(self.timeperiod):
            self.Cycle()
            self.year += 1

    @Timer(name = "Year in {:.2f} seconds")
    def Cycle(self):

        #fig2YearsHist.append(self.year)

        yrResourcesAcrossDBHs = {}
        artResourcesPerStructure = {}
        
        #yrTreeRescources and yrARtResources are dictionaries with resource name as key, value is a list of floats with each item in the list representing a tree
        yrTreeResources = {}
        yrArtResources = {}

        #list of DBHS for the year
        yrDBHS = []
        yrArtPerf = []

        isRecruit = False
        isBuilt = False


        if MODELRECRUIT and self.year != 0 and self.year % INTERVAL == 0:
            isRecruit = True
            self.recruitMessage = self.Recruit()

        if self.year % ARTINTERVAL == 0:
            isBuilt = True
            self.builtMesssage = self.Build()

        self.treesAliveThisYear = 0

        for agent in self.trees:
            if agent.isAlive:
                grow = agent.NextYear()
                if MODELDEATH:
                    death = agent.ChanceDeath()
                #print(f'Grow Rate: {grow} \t Death Rate: {death}')

        for artAgent in self.artificials:
            artAgent.GrowOld()
            self.artificials

        ##calculate number of trees at each DBH level
        ##create list of trees per DBH

        DBHdist = {}
        treesPerDBH = {}
        #initialise dic

        dbhSpan = range(30,MAXDBH)

        
        for cnt in dbhSpan:
            DBHdist.update({cnt : 0})
            treesPerDBH.update({cnt : []})

        for tree in self.trees:
            if tree.isAlive:
                DBHdist[tree.dbh] += 1
                self.treesAliveThisYear += 1
                treesPerDBH[tree.dbh].append(tree)
                yrDBHS.append(tree.dbh)

        #go through each resource
        for resource in RESOURCES:

            resourceMetersAcrossDBH = {}
            metersPerArtificial = []


            col = 'red'
            xplot = []
            yplot = []


            yrAliveArt = []

            for artAgent in self.artificials:
                
                if artAgent.isAlive:
                    metersPerArtificial.append(artAgent.resources[resource])
                    yrArtPerf.append(artAgent.performance)
                    yrAliveArt.append(artAgent)
            
                
            yrArtResources.update({resource : metersPerArtificial})

                
            #find resource list for trees of this DBH
            for key, value in DBHdist.items():
                 
                
                resourceMetersAtThisDBH = []

                dbh = key

                constrictor = 200

                if dbh > CONSTRICTORDBHLOW:
                    constrictor = self.GetConstrictor2(dbh)

                #print(f'dbh: {key}, constrictor: {constrictor}')

                pred = DPREDICTIONS[resource]
                low = DLOWS[resource]
                up = DUPS[resource]
                standard = DSTANDARDS[resource]
                
                #generate a probability density functition  at this DBH for this resource
                
                pPred = pred(dbh)
                pLow = low(dbh)
                pUpper = up(dbh)



                pSD = standard(dbh)/constrictor

                ##

                distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = pSD)

                #distributionFunction = stats.truncnorm((pLow - pPred) / pSD, (pUpper - pPred) / pSD, loc = pPred, scale = constrictor)


                #get how many trees there are and generate lengths via probbility density function
                noOfTrees = value
                uncappedResouceMetersAtThisDBH = distributionFunction.rvs(noOfTrees)


                #engine
                #truncate function so min lengths are 0
                for i in range(len(uncappedResouceMetersAtThisDBH)):
                    j = float(uncappedResouceMetersAtThisDBH[i])
                    
                    if j < RESOURCEBELOW:
                        j = 0
   
                    
                    resourceMetersAtThisDBH.append(float(j))

                    treesPerDBH[dbh][i].resources[resource].append(j)
                    treesPerDBH[dbh][i].resourcesThisYear.update({resource : float(j)})
                    
                    if resource == 'high':
                        
                        """print(j)
                        print(treesPerDBH[dbh][i].resourcesThisYear['high'])
                        print(f'dbh: {dbh}')
                        print(f'tree per dbh: {len(treesPerDBH[dbh])}')
                        print(f'resources in loop: {len(uncappedResouceMetersAtThisDBH)}')
                        print(f'iteration: {i})')
                        print(f'xPos: {treesPerDBH[dbh][i].point[0]}')

                        if i > 0:
                            print(f'previous: {treesPerDBH[dbh][i-1].resourcesThisYear["high"]}')
                            print(f'previous xPos: {treesPerDBH[dbh][i-1].point[0]}')

                        print("")"""



                    #select tree agent and put resource there
                    #print(f'Year: {self.year} \t DBH: {dbh}  \t Trees Alive: {self.treesAliveThisYear} \t Resource: {resource} \t Amount: {j}m')

                
                if resource == 'high':
        
                    test = []
                    dist = range(len(treesPerDBH[dbh]))
                    
                    for z in dist:                       
                        test.append(treesPerDBH[dbh][z].resourcesThisYear['high'])

                        """print(f'dbh: {dbh}')
                        print("resources")
                        print(f'z is {z}')
                        print(f"resources are: {treesPerDBH[dbh][z].resourcesThisYear['high']}")
                        print(f"resources in list are: {test[-1]}")"""

                    if len(treesPerDBH[dbh]) > 0:
                        """print(f'dbh: {dbh}')
                        print(f'tree per dbh: {len(treesPerDBH[dbh])}')
                        print(f'resources in loop: {len(uncappedResouceMetersAtThisDBH)}')
                        #print(f'{resource} and {test}')"""


                if len(resourceMetersAtThisDBH) > 0:
                    resourceMetersAcrossDBH.update({int(dbh) : resourceMetersAtThisDBH})

                yrResourcesAcrossDBHs.update({resource : resourceMetersAcrossDBH})

                flattendResources = list(itertools.chain.from_iterable(list(resourceMetersAcrossDBH.values())))
              
                yrTreeResources.update({resource : flattendResources})
                


        #add to main tracking dictionarie:
        self.resourcesSortedByDBH.update({self.year : yrResourcesAcrossDBHs})
        
        self.treeResources.update({int(self.year) : yrTreeResources})
        self.artResources.update({int(self.year) : yrArtResources})




        self.snapTotalAlive.update({self.year : self.treesAliveThisYear})


        #print(f"Year: {self.year} \t Trees Alive: {self.treesAliveThisYear} \t Total: {sum(yrResources['total'])}")

        
        no = int(self.treesAliveThisYear)
        noArt = int(len(yrAliveArt))

        row1 = []
        row2 = []
        row2a = []
        row3 = []
        row4 = []

        if no > 0:
            averageDBH = round(sum(yrDBHS)/len(yrDBHS))
            maxDBH = max(yrDBHS)
            row1 = ['Natural Trees', f'{self.treesAliveThisYear} trees']
            row2 = ['Per Tree', f'Avrg DBH: {averageDBH}cm']
            row2a = ['Max', f'Max DBH: {maxDBH}cm']

            for name in RESOURCES:
                
                met0 = round(sum(yrTreeResources[name]))
                met1= "{:,}".format(met0)
                met2 = "{:,}".format(round(met0/no))

                maxRes = max(yrTreeResources[name])
                #if name == 'high':
                    #print(f'Year: {self.year} \t totalHigh: {met0} \t maxHigh: {maxRes}m \t meanHigh: {met2}m')

                row1.append(f"{met1}m")
                row2.append(f"{met2}m/tree")
                row2a.append(f'{maxRes}m')

        if noArt > 0:
            averageArtPerf = "{:.2f}".format(sum(yrArtPerf)/noArt)
            maxArtPerf = "{:.2f}".format(max(yrArtPerf))

            row3 = ['Prosthetic Structures ', f'{noArt} structures' ]
            row4 = ['Per Artificial', f'Avrg Perf: {averageArtPerf}%, Max Perf: {maxArtPerf}%']

            for name in RESOURCES:
        
                artMet0 = round(sum(yrArtResources[name]))
                artMet1= "{:,}".format(artMet0)
                artMet2 = "{:,}".format(round(artMet0/noArt))

                row3.append(f"{artMet1}m")
                row4.append(f"{artMet2}m/structure")

        row5 = ["-------------------------------------------"]
        
        row6 = [self.recruitMessage]
        row7 = [self.builtMesssage]

        heads = [f"Year: {self.year}", 'Habitat Structures']
        heads.extend(RESOURCES)
        if isRecruit:
            row6 = [UPDATEMESSAGE]
        if isBuilt:
            row7 = [UPDATEMESSAGE]

        print(tabulate([row1, row2, row2a, row3, row4, row5, row6, row7],headers = heads))
        print('')
                

        sample = yrDBHS
        sample.extend([0,145])
        counts, bin_edges = np.histogram(sample, bins=75)
        fig = tpl.figure()
        fig.hist(counts, dbhSpan, grid=[15, 25], force_ascii=False)
        fig.show()

    def Recruit(self):
        recruitment = round(random.uniform(2, 3) * AREA)

        for z in range (recruitment):
            tree = TreeAgent()
            self.trees.append(tree)

        return(f"Last recruit Year: {self.year}, {recruitment} trees")

    
    def Build(self):
        self.artPerf += ARTIMPROVE
        if self.artPerf >= ARTPERFMAX:
            self.artPerf = ARTPERFMAX

        for a in range(ARTNUMBER):
            artificial = ArtificialAgent(self.artPerf)
            self.artificials.append(artificial)

        percent = "{:.2f}".format(self.artPerf)
        return (f"Last built Year: {self.year}, {ARTNUMBER} prosthetics @{percent}")

    def GetConstrictor2(self, dbh):
        
        minDBH = CONSTRICTORDBHLOW 
        maxDBH = 120 
        minConstrictor = 1
        maxConstrictor = 10
        inConstrictorVal = ( (dbh - minDBH) / (maxDBH - minDBH) ) * (maxConstrictor - minConstrictor) + minConstrictor

        constrictorVal = maxConstrictor - inConstrictorVal

        maxTrunc = 1000
        minTrunc = 1

        if constrictorVal > maxTrunc:
            constrictorVal = maxTrunc
        if constrictorVal < minTrunc:
            constrictorVal = minTrunc

        #print(f'DBH: {dbh} \t Constrictor Value: {constrictorVal}')

        return constrictorVal