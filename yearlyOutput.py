
from tabulate import tabulate
import termplotlib as tpl
from setting import *

import numpy as np

from agenttree import *
from agentartificial import *

import simulationcore as simu

from typing import List
from typing import Dict

##exportStates
globalYearlyTotals ={}
perStructureTotals = {}
resources = ['total', 'dead', 'high']

for n in resources:
        perStructureTotals.update({n : {
            'year' : [],
            'resources' : [],
            'type' : [],
        }})
        globalYearlyTotals.update({n : {
                'trees' : [], 
                'artificial' : []
            }})

############## From Year of Sim

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


            for name in RESOURCES:
                yrArtResources[name].append(agent.resourcesThisYear[name])



            #print(f'artificial {name}: {agent.resourcesThisYear[name]}')


    ############ cal other stats
    
    averageDBH = round(sum(yrDBHS)/len(yrDBHS))
    maxDBH = max(yrDBHS)

    if noArtificialsAliveThisYear > 0:
        averageArtPerf = "{:.2f}".format(sum(yrArtPerf)/len(yrArtPerf))
        maxArtPerf = "{:.2f}".format(max(yrArtPerf))

    ExportYrly()



def ExportYrly():

    resThisYear = {}

    print(perStructureTotals['total']['resources'])


    for n in resources:
            resThisYear.update({ n : {
                    'trees' : [], 
                    'artificial' : []
                    }})

    for agent in artificials:   
        if agent.isAlive:
            for n in resources:
                perStructureTotals[n]['year'] = year
                perStructureTotals[n]['type'] = f'{scenario} - artificial'
                perStructureTotals[n]['resources'] = agent.resourcesThisYear[n]

                resThisYear[n]['artificial'].append(agent.resourcesThisYear[n])

    print(trees)
            
    for agent in trees:
        if agent.isAlive:
            for n in resources:
                perStructureTotals[n]['year'] = year
                perStructureTotals[n]['type'] = f'{scenario} - trees'
                print(n)
                print(agent.resourcesThisYear)
                print(agent.resourcesThisYear['total'])
                perStructureTotals[n]['resources'] = agent.resourcesThisYear[n]

                resThisYear[n]['trees'].append(agent.resourcesThisYear[n])

    for n in resources:
        globalYearlyTotals[n]['trees'].append(sum(resThisYear[n]['trees']))
        globalYearlyTotals[n]['artificial'].append(sum(resThisYear[n]['artificial']))

def ExportYrLog():
    filePath = f'{settings.SUSTAINABILITY}CSV/cumulative resources - high - {settings.scenario}.csv'
    dfTotals = pd.DataFrame(globalYearlyTotals['high'])
    dfTotals.to_csv(filePath)


    """filePath = f'{settings.SUSTAINABILITY}CSV/per structure resources - {settings.scenario}.csv'
    dfStructures = pd.DataFrame(perStructureTotals)
    dfStructures.to_csv(filePath)
    """


            


