
from tabulate import tabulate
import termplotlib as tpl
from setting import *

import numpy as np

from agenttree import *
from agentartificial import *

import simulationcore as sim

from typing import List
from typing import Dict

##exportStates
perStructureTotals = {}
resources = ['total', 'dead', 'high', 'carrySuit']
"""for n in resources:
        perStructureTotals.update({n : {
            'year' : [],
            'id' : [],
            'resources' : [],
            'type' : [],
        }})"""

globalYearlyTotals = {}

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

def Reset():
    global perStructureTotals
    
    global year
    global trees
    global artificials
    global isRecruit
    global isBuilt
    global recruitMessage
    global builtMesssage

    global yrTreeResources
    global yrArtResources

    global noTreesAliveThisYear
    global noArtificialsAliveThisYear
    
    global yrDBHS
    global yrArtPerf

    global averageDBH
    global maxDBH
    global averageArtPerf
    global maxArtPerf


    perStructureTotals = {}
    for n in resources:
            perStructureTotals.update({n : {
                'year' : [],
                'id' : [],
                'resources' : [],
                'type' : [],
            }})

    
    year = 0
    trees.clear()
    artificials.clear()
    isRecruit = False
    isBuilt = False
    recruitMessage = ""
    builtMesssage = ""

    yrTreeResources.clear()
    yrArtResources.clear()

    noTreesAliveThisYear = 0
    noArtificialsAliveThisYear = 0

    yrDBHS.clear()
    yrArtPerf.clear()

    averageDBH = 0
    maxDBH = 0
    averageArtPerf = 0
    maxArtPerf = 0 


def TransferYearStats(_year, _trees, _artificials, _isRecruit, _isBuilt, _recruitMessage, _builtMessage, thisRun):

    #########

    global year
    global trees
    global artificials

    #global logAllTrees
    #global logAllArtificials
    
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

    #ExportYrly(thisRun)



def ExportYrly2(_run, exportDic):
    
    resThisYear = {}
    perStructureExports = settings._perStructureTotals.copy()

    for n in resources:
            resThisYear.update({ n : {
                    'trees' : [], 
                    'artificial' : []
                    }})

    for agent in artificials:   
        if agent.isAlive:
            for n in resources:
                perStructureExports[n]['year'].append(year)
                perStructureExports[n]['type'].append('artificial')
                perStructureExports[n]['id'].append(agent.num)
                perStructureExports[n]['resources'].append(agent.resourcesThisYear[n])

                resThisYear[n]['artificial'].append(agent.resourcesThisYear[n])

            
    for agent in trees:
        if agent.isAlive:
            for n in resources:
                perStructureExports[n]['year'].append(year)
                perStructureExports[n]['type'].append('trees')
                perStructureExports[n]['id'].append(agent.num)
                perStructureExports[n]['resources'].append(agent.resourcesThisYear[n])

                resThisYear[n]['trees'].append(agent.resourcesThisYear[n])

    for n in resources:
        exportDic['sampleType'].append(settings.samplingType)
        exportDic['structureType'].append(settings.mode)
        exportDic['scenario'].append(settings.samplingScenario)
        exportDic['design'].append(settings.scenario)
        exportDic['run'].append(_run)
        exportDic['year'].append(year)
        exportDic['type'].append(n)
        exportDic['treeQuantity'].append(sum(resThisYear[n]['trees']))

        if settings.mode == "tree":
            exportDic['quantity'].append(sum(resThisYear[n]['trees']))
        else:
            exportDic['quantity'].append(sum(resThisYear[n]['artificial']))

             


def ExportYrly(_run):

    resThisYear = {}

    for n in resources:
            resThisYear.update({ n : {
                    'trees' : [], 
                    'artificial' : []
                    }})

    for agent in artificials:   
        if agent.isAlive:
            for n in resources:
                perStructureTotals[n]['year'].append(year)
                perStructureTotals[n]['type'].append('artificial')
                perStructureTotals[n]['id'].append(agent.num)
                perStructureTotals[n]['resources'].append(agent.resourcesThisYear[n])

                resThisYear[n]['artificial'].append(agent.resourcesThisYear[n])

            
    for agent in trees:
        if agent.isAlive:
            for n in resources:
                perStructureTotals[n]['year'].append(year)
                perStructureTotals[n]['type'].append('trees')
                perStructureTotals[n]['id'].append(agent.num)
                perStructureTotals[n]['resources'].append(agent.resourcesThisYear[n])

                resThisYear[n]['trees'].append(agent.resourcesThisYear[n])

    for n in resources:
        globalYearlyTotals['sampleType'].append(settings.samplingType)
        globalYearlyTotals['structureType'].append(settings.mode)
        globalYearlyTotals['scenario'].append(settings.samplingScenario)
        globalYearlyTotals['design'].append(settings.scenario)
        globalYearlyTotals['run'].append(_run)
        globalYearlyTotals['year'].append(year)
        globalYearlyTotals['type'].append(n)
        globalYearlyTotals['treeQuantity'].append(sum(resThisYear[n]['trees']))

        if settings.mode == "tree":
            globalYearlyTotals['quantity'].append(sum(resThisYear[n]['trees']))
        else:
            globalYearlyTotals['quantity'].append(sum(resThisYear[n]['artificial']))

             
             



def ExportYrLog(filePath, modelRun):
    dfTotals = pd.DataFrame(globalYearlyTotals)
    path = f'{filePath}-{settings.scenario}-{modelRun}.csv'
    print(f'model runn {modelRun} ended, saving {len(dfTotals)} structures to {path}')
    dfTotals.to_csv(path)

    globalYearlyTotals.clear()
    perStructureTotals.clear()

    


    """filePath = f'{settings.SUSTAINABILITY}Stats/CSV/per structure resources/{settings.scenario}.csv'
   #dfStructures = pd.DataFrame(perStructureTotals['high'])
    dfStructures = pd.DataFrame(perStructureTotals)
    dfStructures.to_csv(filePath)
    """


def ExportModelRun():
    return globalYearlyTotals.copy()
    


            


