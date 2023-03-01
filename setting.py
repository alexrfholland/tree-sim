from datetime import *
import os
from tokenize import Name
import scenes
import random



###OUTPUTS
_globalYearlyTotals = {
    "sampleType" : [],
    "structureType" : [],
    "scenario" : [],
    "design" : [],
    "run" : [],
    "year" : [],
    "type" : [],
    "quantity" : [],
    "treeQuantity" : []}


#find DRAWINGOUTPUT to see where to enable images

#JSONOUT = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/outputs/'
JSONOUT = '/Users/alexholland/Coding/tree-sim/data/outputs/json/'

#SUSTAINABILITY  = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/'
SUSTAINABILITY = '/Users/alexholland/Coding/tree-sim/data/outputs/sustainability/'

#VISUALOUT = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Chapter 1 Ethics/Sim/Outputs/Images'
VISUALOUT = '/Users/alexholland/Coding/tree-sim/data/outputs/images/'

#WINDOWSOUT = '/Users/alexholland/Documents/Windows Files/Sim Exports/'
WINDOWSOUT = '/Users/alexholland/Coding/tree-sim/data/outputs/windows/'
#FIGURESIZE = [5,5]
FIGURESIZE = [16,9]

DEBUG = False

ISVISOUT = False

RESOURCES = ["dead","lateral","total","low","medium","high","carrySuit"]
TIMEPERIOD = int(input('How many years?' )) #240
#SCENENO = int(input('What Scenario?'))
#BUDGETSPLIT = float(input('Budget Split?' )) #240
VISCOUNT = int(input('Visuals?' ))

#BUDGET = 554400 * BUDGETSPLIT

BUDGET = 200000


ISNOTREESAFTERFIRST = True



INTERVAL = 30
DENSITYLOW = 4.65
DENSITYHIGH = 4.65
AREA = 440
INITIALTREES = 50
INITIALDBHMIN = 90
INITIALDBHMAX = 130
INITAGEMIN = 200
INITAGEMAX = 400




MODELDEATH = True


modifier = 0.6
#modifier = 1
RESOURCECAPS = {'total' : 1500 * modifier, 'lateral' : 800 * modifier, 'dead' : 350 * modifier, 'high': 20 * modifier, 'medium' : 130 * modifier, 'low' : 1500 * modifier, "carrySuit" : 1};



FOCUSRESOURCE = 'high'


TREESTARTDBH = 30
MAXDBH = 144
TREELIFESPAN = [400,600]

# slope of age vs diameter is 1.97 - 2.71 - Gibbons (2009)
TREEGROWRATE = [197, 271]


BOUNDS = [-654.465282154,  2103.81760729, -1301.10671195, 1457.176178]


# mortality rate of 0.006 to 0.024 per year - Gibbons (2009)

#LOW
deathLow = 0.003
deathHigh = 0.010

#High
#deathLow = 0.006
#deathHigh = 0.024

"""
#low
deathLow = 0.003
deathHigh = 0.010

"""

#recruitment stats from Gibbons (2009)
RECRUITMULTIPLIER = 2




################################SCENARIO
#ARTIFICIALINFOPATH = "/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/model-infos/carrying-info-artificials.csv"
ARTIFICIALINFOPATH = "/Users/alexholland/Coding/tree-sim/data/model-infos/carrying-info-artificials.csv"

scene = {}
ARTLIFEVARIATION = 0.01
#ARTSERVICELIFEVARIATION = 0.01
ARTSERVICELIFEVARIATION = 0.00
modelRecruit = True
modelProsthetics = True
existingTrees = False


samplingScenario = -1
mode = -1
samplingType = -1
scenario = -1

def GetScenario(sceneNo):
    global scene
    global samplingScenario
    global mode
    global samplingType
    global scenario

    scene = scenes.GetModes(sceneNo, BUDGET)
    mode = scene["mode"]
    samplingType = scene["samplingType"]

    
    scenario = scene["scenario"]
    samplingScenario = f"{scenario} - {samplingType}"

    print(f'from settings scene is {mode}')


    
def GetNumberInBudget(budget, low, high):
    noStructures = 0
    while budget > 0:
        noStructures = noStructures + 1
        cost = random.uniform(low, high)
        budget = budget - cost
        #print(f'cost is ${cost}')

    print(f'no structures is {noStructures}')
    return noStructures



"""def GetScenario(sceneNo):
    global scene
    global scenario
    global structureType
    global samplingType
    global design

    scene = scenes.GetArtificial(sceneNo, ARTIFICIALINFOPATH, BUDGET)
    scenario = scene["id"]
    structureType = scene["type"]
    samplingType = scene["samplingType"]
    design = scene["oldID"]

    print(f'from settings scene is {scene["artNo"]}')
"""


#not using
ARTPERFMAX = 1
ARTIMPROVE = 1








UPDATEMESSAGE = '######### \t ######### \t ########'


CONSTRICTORDBHLOW = 75
RESOURCEBELOW = 1

#folderPath 
#FOLDERPATH= "/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/data/resources/"
FOLDERPATH = "/Users/alexholland/Coding/tree-sim/data/resource-curves/"
#filesDict 
FILESDICT = {"dead":"dead-branch-loess", "lateral":"lateral-branch-loess", "total":"total-branch-loess", "low":"low-branch-loess", "medium":"medium-branch-loess", "high":"high-branch-loess", "carrySuit" : "carry-suit-loess"}
#resourceGraph 
RESOURCEGRAPH = ["dead","lateral","total","low","medium","high","carrySuit"]

def MakeFolderPath(parentPath, otherInfo) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

    path = parentPath + otherInfo + timestamp + '/'
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


MAXRESOURCES = {
    'total' : 2125,
    'lateral' : 844,
    'dead' : 351,
    'low' : 1813,
    'medium' : 130,
    'high' : 59,
    'carrySuit' : 1}


def GetVariation(mean, variation):
        max = round(mean + (mean * variation))
        min = round(mean - (mean * variation))
        prediction = random.randint(min, max)
        return prediction

    