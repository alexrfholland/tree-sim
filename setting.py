from datetime import *
import sys, os
from tokenize import Name
import scenes

#find DRAWINGOUTPUT to see where to enable images

JSONOUT = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/outputs/'
#VISUALOUT = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/outputs/images/'
#CSVOUT = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/outputs/csvs/'
#CSVOUT = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Chapter 1 Ethics/Sim/Outputs/Data/'


SUSTAINABILITY  = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/'
VISUALOUT = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Chapter 1 Ethics/Sim/Outputs/Images'
WINDOWSOUT = '/Users/alexholland/Documents/Windows Files/Sim Exports/'
#FIGURESIZE = [5,5]
FIGURESIZE = [16,9]

DEBUG = False

ISVISOUT = False

RESOURCES = ["dead","lateral","total","low","medium","high"]
TIMEPERIOD = int(input('How many years?' )) #240
SCENENAME = str(input('What Scenario?'))
BUDGETSPLIT = float(input('Budget Split?' )) #240

BUDGET = 554400 * BUDGETSPLIT

scene = scenes.SetScenarios(SCENENAME)


INTERVAL = 30
DENSITYLOW = 4.65
DENSITYHIGH = 4.65
AREA = 440
INITIALTREES = 50
INITIALDBHMIN = 90
INITIALDBHMAX = 130
INITAGEMIN = 200
INITAGEMAX = 400

scenario = scene['scenario']

print(scene['isRecruit'])

modelRecruit = scene['isRecruit']
modelProsthetics = scene['isArtificials']
existingTrees = scene['isExistingTrees']

MODELDEATH = True


modifier = 0.6
#modifier = 1
RESOURCECAPS = {'total' : 1500 * modifier, 'lateral' : 800 * modifier, 'dead' : 350 * modifier, 'high': 20 * modifier, 'medium' : 130 * modifier, 'low' : 1500 * modifier}
FOCUSRESOURCE = 'high'


TREESTARTDBH = 30
MAXDBH = 144
TREELIFESPAN = [400,600]

# slope of age vs diameter is 1.97 - 2.71 - Gibbons (2009)
TREEGROWRATE = [197, 271]


BOUNDS = [-654.465282154,  2103.81760729, -1301.10671195, 1457.176178]


# mortality rate of 0.006 to 0.024 per year - Gibbons (2009)
deathLow = 0.003#.006
deathHigh = 0.010#.024


#recruitment stats from Gibbons (2009)
RECRUITMULTIPLIER = 2

##artificial
ARTNUMBER = round(BUDGET/scene['cost'])
ARTINTERVAL = scene['serviceLife']
ARTPERFMIN = scene['performance']
ARTPERFMAX = scene['maxPerformance']
ARTIMPROVE = scene['improveRate']
ARTLENGTH = scene['length']
ARTDEADLATERAL = scene['deadlateral']

print(f'scene is {scene}')

ARTLIFE = scene['serviceLife']
ARTLIFEVARIATION = scene['lifeVariation']

UPDATEMESSAGE = '######### \t ######### \t ########'


CONSTRICTORDBHLOW = 75
RESOURCEBELOW = 0.5

#folderPath 
FOLDERPATH= "/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/data/resources/"
#filesDict 
FILESDICT = {"dead":"dead-branch-loess", "lateral":"lateral-branch-loess", "total":"total-branch-loess", "low":"low-branch-loess", "medium":"medium-branch-loess", "high":"high-branch-loess"}
#resourceGraph 
RESOURCEGRAPH = ["dead","lateral","total","low","medium","high"]

def MakeFolderPath(parentPath, otherInfo) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    path = parentPath + otherInfo + timestamp + '/'
    if not os.path.isdir(path):
        os.makedirs(path)
    return path
