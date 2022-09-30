
from tabulate import tabulate
import termplotlib as tpl
from settings.setting import *

import numpy as np

from agenttree import *
from agentartificial import *

import simulationcore as simu

from typing import List
from typing import Dict


############## From Year of Sim

"""year = simu.year
trees : List[TreeAgent]  = simu.trees
artificials  : List[ArtificialAgent] = simu.artificials
"""



year = 0
trees: List[TreeAgent]  = []
artificials: List[ArtificialAgent] = []
isRecruit = False
isBuilt = False
recruitMessage = ""
builtMesssage = ""

############## calculated here

yrTreeResources = {}
yrArtResources = {}


noTreesAliveThisYear = 0
noArtificialsAliveThisYear = 0

yrDBHS = []
yrArtPerf = []

averageDBH = 0
maxDBH = 0
averageArtPerf = 0
maxArtPerf = 0


def TransferYearStats(_year, _trees, _artificials, _isRecruit, _isBuilt, _recruitMessage, _builtMessage):

    #########

    global year
    global trees
    global artificials

    global logAllTrees
    global logAllArtificials
    
    global yrTreeResources
    global yrArtResources

    global isRecruit
    global isBuilt
    global recruitMessage
    global builtMesssage

    global noTreesAliveThisYear
    global noArtificialsAliveThisYear
    
    global yrDBHS
    global yrArtPerf

    global averageDBH
    global maxDBH
    global averageArtPerf
    global maxArtPerf



    


    


    ########### clear previous

    for name in RESOURCES:
        yrTreeResources.update({name: []})
        yrArtResources.update({name: []})


    

    

    yrDBHS.clear()
    yrArtPerf.clear()
    

    noTreesAliveThisYear = 0
    noArtificialsAliveThisYear = 0


    ################update from model

    year = _year
    trees = _trees
    artificials = _artificials

    isRecruit = _isRecruit
    isBuilt = _isBuilt
    recruitMessage = _recruitMessage
    builtMesssage = _builtMessage

    ################obtain stats

    for agent in trees:
        if agent.isAlive:
            noTreesAliveThisYear += 1
            yrDBHS.append(agent.dbh)

            #print(f'{name}: {agent.resourcesThisYear[name]}')


            for name in RESOURCES:
                yrTreeResources[name].append(agent.resourcesThisYear[name])

    #print(f'no trees alive this year is {noTreesAliveThisYear}')
               
                
    for agent in artificials:
        if agent.isAlive:
            noArtificialsAliveThisYear += 1
            yrArtPerf.append(agent.performance)



            #print(f'artificial {name}: {agent.resourcesThisYear[name]}')


    ############ cal other stats
    
    averageDBH = round(sum(yrDBHS)/len(yrDBHS))
    maxDBH = max(yrDBHS)

    if noArtificialsAliveThisYear > 0:
        averageArtPerf = "{:.2f}".format(sum(yrArtPerf)/len(yrArtPerf))
        maxArtPerf = "{:.2f}".format(max(yrArtPerf))


