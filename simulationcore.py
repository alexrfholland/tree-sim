from optparse import Values
from traceback import format_exc
from agentartificial import ArtificialAgent
from agenttree import TreeAgent
import setting as set
import resourcecurves as curves
import kdeExporter

#from settings.setting import set
import yearlyOutput as yearLog
from visuals import VisualOut
from textout import TextOut


import termplotlib as tpl

import numpy as np
from pyparsing import dblSlashComment
from scipy import rand
from scipy.sparse.construct import random
import scipy.stats as stats
import random

import itertools

from codetiming import Timer

# generate random integer values
from random import randint


from typing import List
from typing import Dict

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

    logAllTrees = {}
    logAllArtificials = {}

    logAllTrees2 = []
    logAllArtificials2 = []
    
    noTreesAtKeyLifeStages = {}
    
    trees: List[TreeAgent] = []
    artificials: List[ArtificialAgent] = []

    #size = set.AREA
    #density = (set.DENSITYHIGH + set.DENSITYLOW)/2 * (1 - set.BUDGETSPLIT)
    
    
    #startNoTrees = round(size * density)
    startNoTrees = -1
    print(f'start number of trees is {startNoTrees}')

    year = 0
    timeperiod = set.TIMEPERIOD

    resourceCurves = {}
    totalResources = {}
    previousDotsX = []
    previousDotsY = []
    treesAliveThisYear = 0

    snapTotalAlive = {}
    snapMeters = {}

    resourcesSortedByDBH = {}

    recruitMessage = set.UPDATEMESSAGE
    builtMesssage = set.UPDATEMESSAGE

    exportTree = {'year' : [], 'high' : []}
    exportPros = {'year' : [], 'high' : []}

    nextServiceLife = -1
    nextRecruitInterval = -1
    nextRecruitMultiplier = -1


    #yrTreeRescources and yrARtResources are hierachical dictionaries.
    # First level: key is year since sim began, value is second level:
    # Second level: YrTreeResource and YrArtResource: dictionary with resource name as key, value is a list of floats with each item in the list representing a tree

    treeResources = {}
    artResources = {}



    


    
    #@Timer(name = "Finished running model in {:.2f} seconds")
    def __init__(self, _run, _scenarioNo):

        self.sustainabilityExports = {
        "sampleType" : [],
        "structureType" : [],
        "scenario" : [],
        "design" : [],
        "run" : [],
        "year" : [],
        "type" : [],
        "quantity" : [],
        "treeQuantity" : []}
       
    
        set.modelRecruit = set.scene["isRecruit"]
        set.modelProsthetics = set.scene["isArtificials"]
        set.existingTrees = set.scene["isExistingTrees"]


        yearLog.globalYearlyTotals = set._globalYearlyTotals.copy()
        yearLog.perStructureTotals = set._perStructureTotals.copy()
        
        ###SET UP THIS RUN####
        
        self.thisRun = _run
        self.thisScenarioNo = _scenarioNo

        
        ######################
        
    
        self.year: int = 0

        
        if set.VISCOUNT != 0:
            self.vis = VisualOut()
        #print(set.scenario)

        #rivX.extend(self.geo.riverPts[:,0])
        #rivY.extend(self.geo.riverPts[:,1])


        for name in set.RESOURCES:
            self.artResources.update({name : []})


        ###SET UP RECRUIT####
        self.startNoTrees = set.GetNumberInBudget(set.BUDGET * set.scene['split'], set.scene['treeCostLow'], set.scene['treeCostHigh'])

        #print(f"{self.startNoTrees} trees planted between ${set.scene['treeCostLow']} and ${set.scene['treeCostHigh']}")




             
        #code to shut off trees
        if set.SHUTOFFFTREESINOTHERMODES and set.scene["mode"] != "tree":
            self.startNoTrees = 5
            set.MODELDEATH = False
            set.modelRecruit = False

        
        ###code to export kde stuff
        
        self.spatials = kdeExporter.spatialExporter(set.scene)




        """ if set.ISNOTREESAFTERFIRST and self.thisScenarioNo > 0:
            self.startNoTrees = 5
            set.MODELDEATH = False
            set.modelRecruit = False"""
    
        #for i in range (round(self.size * self.density)):
        for i in range (round(self.startNoTrees)):
            tree = TreeAgent()
            tree.yearborn = self.year
            self.trees.append(tree)

        if set.existingTrees:
            self.GetExtraTrees()
        
        for j in range(self.timeperiod):
            self.Cycle()
            self.year += 1

        self.nextServiceLife = self.GetNextServiceLife()
        self.nextRecruitInterval = self.GetNextRecrutimentInterval()
        self.nextRecruitMultiplier = self.GetNextRecruitmentMulti()

        

    #GOOD
    #@Timer(name = "Year in {:.2f} seconds")
    def Cycle(self):

        #global trees
        #global artificials

        
        #yrAliveArt : List[ArtificialAgent] = []
        
        #fig2YearsHist.append(self.year)

        yrResourcesAcrossDBHs = {}
        artResourcesPerStructure = {}
        
        #yrTreeRescources and yrARtResources are dictionaries with resource name as key, value is a list of floats with each item in the list representing a tree
        yrTreeResources = {}
        yrArtResources = {}

        #list of DBHS for the year
        yrDBHS = []
        #yrArtPerf = []

        isRecruit = False
        isBuilt = False

        if set.modelRecruit and self.year != 0 and self.year % set.INTERVAL == 0:
            isRecruit = True
            self.recruitMessage = self.Recruit()
        
        
        
        """
        
        if set.modelRecruit and self.year != 0 and self.year % self.nextRecruitInterval == 0:
            isRecruit = True
            self.recruitMessage = self.Recruit()
            self.nextRecruitInterval = self.GetNextRecrutimentInterval()
            self.nextRecruitMultiplier = self.GetNextRecruitmentMulti()"""
        
        
        #if set.modelProsthetics and self.year % set.ARTINTERVAL == 0:
        if set.modelProsthetics and self.year % self.nextServiceLife == 0:
            isBuilt = True
            self.builtMesssage = self.Build()
            self.nextServiceLife = self.GetNextServiceLife()

        

        
        if set.MODELDEATH:
    
            self.CullTrees()

        
        self.treesAliveThisYear = 0
        
        for agent in self.trees:
            if agent.isAlive:
                grow = agent.NextYear()
                if set.MODELDEATH:
                    #death = agent.ChanceDeath(self.year)
                    agent.CheckIfTooOld(self.year)
                #print(f'Grow Rate: {grow} \t Death Rate: {death}')

        for artAgent in self.artificials:
            artAgent.GrowOld()
            #print(f'art resources are {artAgent.resourcesThisYear}')

            #yrArtPerf.append(artAgent.performance)
            #yrAliveArt.append(artAgent)

        ##calculate number of trees at each DBH level
        ##create list of trees per DBH

        DBHdist = {}
        treesPerDBH: Dict[int, List[TreeAgent]] = {}
        #initialise dic

        dbhSpan = range(set.TREESTARTDBH,set.MAXDBH+1)

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
        for resource in set.RESOURCES:

            resourceMetersAcrossDBH = {}
            metersPerArtificial = []


            for artAgent in self.artificials:
                
                if artAgent.isAlive:
                    metersPerArtificial.append(artAgent.resourcesThisYear[resource])
                
            #print(f'{resource} artificial is {metersPerArtificial}')
            yrArtResources.update({resource : metersPerArtificial})

                
            #find resource list for trees of this DBH
            ##count = 0 ##VALUE FOR TESTING

            for key, value in DBHdist.items():
                 

                resourceMetersAtThisDBH = []

                dbh = key

                constrictor = 200

                if dbh > set.CONSTRICTORDBHLOW:
                    constrictor = self.GetConstrictor2(dbh)

                #print(f'dbh: {key}, constrictor: {constrictor}')

                pred =curves.DPREDICTIONS[resource]
                low = curves.DLOWS[resource]
                up = curves.DUPS[resource]
                standard = curves.DSTANDARDS[resource]
                
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
                
                ##countb = 0 ##VALUE FOR TESTING
                for i in range(len(uncappedResouceMetersAtThisDBH)):
                    j = float(uncappedResouceMetersAtThisDBH[i])
                    
                    if j < set.RESOURCEBELOW:
                        j = 0
   
                    
                    resourceMetersAtThisDBH.append(float(j))

                    treesPerDBH[dbh][i].resources[resource].append(j)
                    treesPerDBH[dbh][i].resourcesThisYear.update({resource : float(j)})

                """ ##TESTING - we have established that the raw generator are generating unique values, and that resources and resourcesthisyear have unique values so far
                    if resource == 'dead' and count == 0 and countb == 0 and len(uncappedResouceMetersAtThisDBH) > 0:
                        print(f'year is {self.year}')
                        print(f'raw j value for {resource} is {uncappedResouceMetersAtThisDBH[0]} and count is {count}')
                        print(f'agent is {treesPerDBH[dbh][0]}')
                        print(f'raw resources this year value for agent 0 at dbh:{dbh} is {treesPerDBH[dbh][0].resourcesThisYear[resource]}')
                        print(f'history state of resources is {treesPerDBH[dbh][0].resources[resource]}')

                        count = count + 1
                        

                    countb = countb + 1
                    ##END TESTING"""

                if len(resourceMetersAtThisDBH) > 0:
                    resourceMetersAcrossDBH.update({int(dbh) : resourceMetersAtThisDBH})

                yrResourcesAcrossDBHs.update({resource : resourceMetersAcrossDBH})

                flattendResources = list(itertools.chain.from_iterable(list(resourceMetersAcrossDBH.values())))
              
                yrTreeResources.update({resource : flattendResources})
                
                

                
        #add to main tracking dictionarie:
        self.resourcesSortedByDBH.update({self.year : yrResourcesAcrossDBHs})
        
        self.treeResources.update({int(self.year) : yrTreeResources})
        self.artResources.update({int(self.year) : yrArtResources})
        #print(f'Yr {self.year} art resources are {self.artResources}')


        self.snapTotalAlive.update({self.year : self.treesAliveThisYear})


        #print(f"Year: {self.year} \t Trees Alive: {self.treesAliveThisYear} \t Total: {sum(yrResources['total'])}")

        yearLog.TransferYearStats(self.year, self.trees, self.artificials, isRecruit, isBuilt, self.recruitMessage, self.builtMesssage, self.thisRun)
        self.GetYearlyTotalsSustain(self.sustainabilityExports)


        if self.year % set.SPATIALDATAINTERVAL == 0:
            self.spatials.GetYearlyTotalsSustain(self.trees, self.artificials, self.year)





        self.AddHistoryStates()
        res = 'dead'
        #print(f'{res} is {self.trees[0].resourcesThisYear[res]}') ##TEST this is matching the generated values
        #self.GetJSONOut()
        self.GetJSONOut2()

        #print(f'from sim core of the year log: {yearLog.noTreesAliveThisYear}')
        TextOut(set.samplingScenario)
        
        
        if set.VISCOUNT != 0:
            self.vis.Update()
    
        if self.year % set.INTERVAL == 00:
            self.noTreesAtKeyLifeStages.update({self.trees[0].dbh : self.treesAliveThisYear})

        
    def CullTrees(self):

        treesAliveBeforeCull = 0

        for agent in self.trees:
            if agent.isAlive:
                treesAliveBeforeCull = treesAliveBeforeCull + 1
        
        cutPercentage = random.uniform(set.scene["treeDeathLow"], set.scene["treeDeathHigh"])
        treesToCut = round(treesAliveBeforeCull * cutPercentage)

        print(f'trees to cut this year is {cutPercentage}% of {treesAliveBeforeCull} which is {treesToCut}')


        for agent in self.trees:
            
            if agent.isAlive:
                agent.isAlive = False
                treesToCut = treesToCut - 1

            if treesToCut < 1:
                break
        
        if treesToCut >= 1:
            0
            print(f'didnt kill enough trees - need to kill this many more: {treesToCut}')

    
    def GetYearlyTotalsSustain(self, _exportDic):
        resources = ['total', 'dead', 'high', 'carrySuit']        
        resThisYear = {}
        for n in resources:
                resThisYear.update({ n : {
                        'trees' : [], 
                        'artificial' : []
                        }})
                
        for agent in self.artificials:
            if agent.isAlive:
                for n in resources:
                    resThisYear[n]['artificial'].append(agent.resourcesThisYear[n])

                
        for agent in self.trees:
            if agent.isAlive:
                for n in resources:
                    resThisYear[n]['trees'].append(agent.resourcesThisYear[n])

        for n in resources:
            _exportDic['sampleType'].append(set.samplingType)
            _exportDic['structureType'].append(set.mode)
            _exportDic['scenario'].append(set.samplingScenario)
            _exportDic['design'].append(set.scenario)
            _exportDic['run'].append(self.thisRun)
            _exportDic['year'].append(self.year)
            _exportDic['type'].append(n)
            _exportDic['treeQuantity'].append(sum(resThisYear[n]['trees']))

            if set.mode == "tree":
                _exportDic['quantity'].append(sum(resThisYear[n]['trees']))
            else:
                _exportDic['quantity'].append(sum(resThisYear[n]['artificial']))

        def GetFinalStats(self, exportDic):
            return exportDic



                

        
        
        
    

    def Recruit(self):
        #recruitment = self.nextRecruitMultiplier * self.startNoTrees


        
        recruitment = 2 * set.GetNumberInBudget(set.BUDGET * set.scene['split'], set.scene['treeCostLow'], set.scene['treeCostHigh'])
        
        
        """if set.ISNOTREESAFTERFIRST and self.thisScenarioNo > 0:
            recruitment = 50"""

        for z in range (recruitment):
            tree = TreeAgent()
            tree.yearborn = self.year
            self.trees.append(tree)

        random.shuffle(self.trees)
        return(f"Last recruit Year: {self.year}, {recruitment} trees")
        

    
    def GetNextServiceLife(self):
        serviceLife = set.GetVariation(set.scene['serviceLife'], set.ARTSERVICELIFEVARIATION)
        print(f"next service life is {serviceLife}")
        return serviceLife

    def GetNextRecrutimentInterval(self):
        pulse = set.GetVariation(set.INTERVAL, .2)
        #pulse = set.GetVariation(set.INTERVAL, set.ARTSERVICELIFEVARIATION)
        print(f"next recrutiment pulse is {pulse}")
        return pulse

    def GetNextRecruitmentMulti(self):
        recruitNumber = set.GetVariation(set.RECRUITMULTIPLIER, set.ARTSERVICELIFEVARIATION)
        print(f"next recruit multiplier is {recruitNumber}")
        return recruitNumber
    


    """def Learn(self):
        if set.ARTIMPROVE > 0:
            self.artPerf += set.ARTIMPROVE
            if self.artPerf >= set.ARTPERFMAX:
                self.artPerf = set.ARTPERFMAX
        
    def Adapt(self):
        self.Learn()
        self.artPerf += set.ARTIMPROVE
        if self.artPerf >= set.ARTPERFMAX:
            self.artPerf = set.ARTPERFMAX

        for artagent in self.artificials:
            artagent.Upgrade(self.artPerf)"""
    
    def Build(self):
        #self.Learn()
        artificialsThisBuild = set.GetNumberInBudget(set.BUDGET * (1 - set.scene['split']), set.scene['costLow'], set.scene['costHigh'])
        
        
        #for a in range(set.scene["artNo"]):
        for a in range(artificialsThisBuild):
            artificial = ArtificialAgent(set.scene)
            self.artificials.append(artificial)

        #percent = "{:.2f}".format(set.scene["performance"])
        return (f"Last built Year: {self.year}, {artificialsThisBuild} {set.scene['mode']}s")
        #return (f"Last built Year: {self.year}, {set.scene['artNo']} prosthetics @{percent}")

    def GetExtraTrees(self):
        
        treeNos = [2032, 1668, 1389, 1120, 917, 773, 642, 526]
        treeDBHs = [30, 44, 56, 70, 83, 96, 109, 121]

        for i in range(len(treeNos)):
            for j in range(treeNos[i]):
                tree = TreeAgent()
                tree.dbh = (treeDBHs[i])
                tree.exactDbh = (treeDBHs[i])
                
                self.trees.append(tree)
    
    def GetConstrictor2(self, dbh):
        
        minDBH = set.CONSTRICTORDBHLOW 
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

    def GetStats(self):
        finalresources = {'x' : [], 'y' : []}
        for name in set.RESOURCES:
            finalresources.update({name : []})
        #print(finalresources)

        tree: TreeAgent
        for tree in self.trees:
            if tree.isAlive:
                finalresources['x'].append(tree.point[0])
                finalresources['y'].append(tree.point[1])
                for name in set.RESOURCES:
                    finalresources[name].append(tree.resourcesThisYear[name])

        #df = pd.DataFrame(finalresources)
        #filePath = set.MakeFolderPath(set.CSVOUT, f'total resources stats - {set.scenario}')
        #df.to_csv(filePath + f"{self.year} - {set.scenario}.csv")

    def GetJSONOut(self):
        yrT = {}
        yrA = {}

        for tree in self.trees:
            if tree.isAlive:
                #out = (tree.age, tree.dbh, tree.resourcesThisYear)
                out = {'age' : tree.age, 'performance' : tree.dbh, 'resources' : tree.resourcesThisYear}
                yrT.update({tree.num : out})

        for art in self.artificials:
            if art.isAlive:
                #out = (art.age, art.performance ,art.resourcesThisYear)
                out = {'age' : art.age, 'performance' : art.performance, 'resources' : art.resourcesThisYear}
                yrA.update({art.num : out})

        self.logAllTrees.update({self.year : yrT})
        self.logAllArtificials.update({self.year : yrA})


    def AddHistoryStates(self):
         for tree in self.trees:
                if tree.isAlive:
                    tree.hPerf.update({self.year : tree.dbh})
                    tree.hAge.update({self.year : tree.age})
                    tree.hResources.update({self.year : tree.resourcesThisYear.copy()})
                    
            
         for art in self.artificials:
                if art.isAlive:
                    art.hPerf.update({self.year : art.performance})
                    art.hAge.update({self.year : art.age})
                    art.hResources.update({self.year : art.resourcesThisYear.copy()})
         """
         ##TESTING
         resource = 'dead'
         print(self.trees[0])
         print (f"raw {resource} resources are {self.trees[0].resourcesThisYear[resource]}")
         for y in range(self.year):
            print (f'hResources of {resource} are {self.trees[0].hResources[y][resource]}') #now it works! here
"""
    def GetJSONOut2(self):
        
        count = 0
        for tree in self.trees:
            out = {'age' : tree.hAge, 'performance' : tree.hPerf, 'resources' : tree.hResources}
            if self.year in tree.hResources:
               """ print(f'agent is {count}, year is {self.year} and ages are {out["resources"][self.year]}')"""
            self.logAllTrees2.append(out)
            count = count + 1

        for art in self.artificials:
            out = {'age' : art.hAge, 'performance' : art.hPerf, 'resources' : art.hResources}
            self.logAllArtificials2.append(out)

    def GetTreeDataFrame(self):    
        dic = {}
        res = 'dead'
        for year in range(self.year):
            row = []
            for tree in self.trees:
                aliveThisYear = True
                cell = ({'age' : -1,
                        'performance' : -1,
                        'resources' : {'tree-dead': -1},
                        'alive' : False
                        })

                if year < tree.yearborn or year >= tree.yeardeath:
                    aliveThisYear = False
                
                if year in tree.hPerf:
                    cell = ({'age' : tree.hAge[year],
                        'performance' : tree.hPerf[year],
                        'resources' : tree.hResources[year],
                        'alive' : aliveThisYear
                        })
                row.append(cell)
            dic.update({f'y{year}' : row})
        

        df = pd.DataFrame.from_dict(dic)
        return df

                        
