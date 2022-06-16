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



JSONOUT = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/outputs/'

RESOURCES = ["dead","lateral","total","low","medium","high"]
TIMEPERIOD = 240
INTERVAL = 30
DENSITYLOW = 4.65
DENSITYHIGH = 4.65
AREA = 440
INITIALTREES = 50
INITIALDBHMIN = 90
INITIALDBHMAX = 130
INITAGEMIN = 200
INITAGEMAX = 400


MODELRECRUIT = True
MODELDEATH = True

BOUNDS = [0,1000]

RESOURCECAPS = {'total' : 1500, 'lateral' : 800, 'dead' : 350, 'high': 20, 'medium' : 130, 'low' : 1500}
FOCUSRESOURCE = 'high'


# mortality rate of 0.006 to 0.024 per year - Gibbons (2009)
DEATHLOW = .006
DEATHHIGH = .024
MAXDBH = 145

#recruitment stats from Gibbons (2009)
RECRUITMULTIPLIER = 2

##artificial
ARTNUMBER = 20
ARTINTERVAL = 3
ARTPERFMIN = 0.01
ARTPERFMAX = 0.3
ARTIMPROVE = 0.01

ARTLIFE = 5

UPDATEMESSAGE = '######### \t ######### \t ########'


CONSTRICTORDBHLOW = 75



#visuals

figXDraw = list()
figYDraw = list()
figZDraw = list()
figHigh = list()
figCol = list()
figTitle = list()

figResource = {}

figProsX = list()
figProsY = list()

fig2HistTree = list()
fig2HistProsthetic = list()
fig2YearsHist = list()

fig3ResPerAgent = list()
fig3ColsPerAgent = list()
fig3YrssPerAgent = list()

fig3ResPerTree = list()
fig3ResPerTree.append(40)

fig3ResPerProsthetic = list()
fig3ResPerProsthetic.append(40)

fig3YrssPerTree = list()
fig3YrssPerTree.append(100)

fig3YrssPerProsthetic = list()
fig3YrssPerProsthetic.append(100)

fig4TreeLocXThisYear = list()
fig4TreeLocYThisYear = list()

figBTitle = list()


rivX = list()
rivY = list()



def Make_FigA():
    fig.suptitle(figTitle[-1], fontsize=16)

    # Create 4x4 Grid
    gs = fig.add_gridspec(nrows=3, ncols=2, height_ratios=[1,1,1], width_ratios=[1,1], wspace = 0.1, hspace = 0.3)

    # Create Three Axes Objects
    axMap = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[2, 1])

    #HEATMAP HIGH + ARTIFICIAL
    heatmap1, xedges1, yedges1 = np.histogram2d(figXDraw, figYDraw,  bins=200, weights= figHigh, density = False)
    extent1 = [xedges1[0], xedges1[-1], yedges1[0], yedges1[-1]]
    #print(extent1)
    #extent1 = [-654.465282154,  2103.81760729, -1301.10671195, 1457.176178]
        
    #circles on prosthetics
    axMap.scatter(figProsX, figProsY, s = 100, c = 'none', edgecolors='white', alpha=.25)

    #river
    axMap.plot(rivX, rivY, linewidth = 0.5, c = '#753183')
    #axMap.scatter(rivX, rivY, s = 15, c = '#753183')
    
    #heatmap
    im = axMap.imshow(heatmap1.T, extent=extent1, origin='lower', cmap = 'viridis', vmin = 0, vmax = RESOURCECAPS[FOCUSRESOURCE])  

    # Define the limits, labels, ticks as required
    axMap.set_xlim([-654.465282154,  2103.81760729])
    axMap.set_ylim([-1301.10671195, 1457.176178])
    axMap.set_xlabel(r' ') # Force this empty !
    #axes[name].set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
    axMap.set_xticklabels([]) # Force this empty

    axMap.set_ylabel(r' ') # Force this empty !
    #axes[name].set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
    axMap.set_yticklabels([]) # Force this empty !

    axMap.set_title('High with Prosthetics')

    axMap.set_facecolor('#440154')
    
    #TOTAL RESOURCES
    pal = sns.color_palette("Set1")
    ax2.stackplot(fig2YearsHist, fig2HistTree, fig2HistProsthetic, labels = ['x', 'y'])
    ax2.set_title('Cumulative High Resources')


    #HEATMAP: DISTRIBUTION OF HIGH RESOURCES PER TREE
    heatmap, xedges, yedges = np.histogram2d(fig3YrssPerTree ,fig3ResPerTree, bins=200, density = False, weights = fig3ResPerTree)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #extentB = [0, 250, 0, 40]
    im = ax3.imshow(heatmap.T, extent=extent, origin='lower', cmap = 'viridis', vmin = 0, vmax = 20)  
    ax3.set_title('Distribution of High Resources Per Natural Trees')


    #HEATMAP: DISTRIBUTION OF HIGH RESOURCES PER PROSTHETIC
    heatmap, xedges, yedges = np.histogram2d(fig3YrssPerProsthetic ,fig3ResPerProsthetic, bins=200, density = False, weights = fig3ResPerProsthetic)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #extentC = [0, 250, 0, 40]
    #extent = [0, 250, 0, 30]
    im = ax4.imshow(heatmap.T, extent=extent, origin='lower', cmap = 'viridis', vmin = 0, vmax = 20)
    ax4.set_title('Distribution of High Resources Per Prosthetics')

    plt.tight_layout()


def Make_FigB():
    # Create 4x4 Grid

    fig.suptitle(figBTitle[-1], fontsize=16)
    
    colbarWidth = 0.025
    spaceWidth = 0.1
    gs = fig.add_gridspec(nrows=2, ncols=8, height_ratios=[1, 1], width_ratios=[1, colbarWidth, spaceWidth, 1, colbarWidth, spaceWidth, 1, colbarWidth], wspace = 0.2, hspace = 0.2)

    axes = {}
    axes.update({'total' : fig.add_subplot(gs[0, 0])})
    axes.update({'lateral' : fig.add_subplot(gs[0, 3])})
    axes.update({'dead' : fig.add_subplot(gs[0, 6])})
    axes.update({'low' : fig.add_subplot(gs[1, 0])})
    axes.update({'medium' : fig.add_subplot(gs[1, 3])})
    axes.update({'high' : fig.add_subplot(gs[1, 6])})

    bars = {}
    bars.update({'total' : plt.subplot(gs[0,1])})
    bars.update({'lateral' : plt.subplot(gs[0,4])})
    bars.update({'dead' : plt.subplot(gs[0,7])})
    bars.update({'low' : plt.subplot(gs[1,1])})
    bars.update({'medium' : plt.subplot(gs[1,4])})
    bars.update({'high' : plt.subplot(gs[1,7])})

    
    for name in RESOURCES:
        heatmap, xedges, yedges = np.histogram2d(fig4TreeLocXThisYear, fig4TreeLocYThisYear,  bins=200, weights= figResource[name], density = False)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #extent = [-1000, 2000, -1000, 2000]

        im = axes[name].imshow(heatmap.T, extent=extent, origin='lower', cmap = 'viridis', vmin = 0, vmax = RESOURCECAPS[name])
        
        # Define the limits, labels, ticks as required
        #axes[name].set_xlim([-1000,2000])
        #axes[name].set_ylim([-1000,2000])
        axes[name].set_xlabel(r' ') # Force this empty !
        #axes[name].set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
        axes[name].set_xticklabels([]) # Force this empty

        axes[name].set_ylabel(r' ') # Force this empty !
        #axes[name].set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
        axes[name].set_yticklabels([]) # Force this empty !


        axes[name].set_title(name)

        axes[name].plot(rivX, rivY, linewidth = 0.4, c = '#753183')
        axes[name].set_xlim([-654.465282154,  2103.81760729])
        axes[name].set_ylim([-1301.10671195, 1457.176178])
        axes[name].set_facecolor('#440154')


        cbax = bars[name]
        cb = Colorbar(ax = cbax, mappable = im, orientation = 'vertical', ticklocation = 'right')
    

    plt.tight_layout()



    













plt.ion()  # enable interactivity
fig = plt.figure(figsize=(16, 9))





"""
x = [10.0,3,2,.1,24]
y = [10.0,3,2,.1,24]
z = [10.0,3,2,.1,24]

def make_fig():
    
    ax.scatter3D(xDraw, yDraw, zDraw, color = "green")
    plt.title("simple 3D scatter plot")
    plt.show()
    #plt.ylim(bottom=0, top = 1000)
    #plt.xlim(left=0, right = 1000)



# Creating figure
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(1, 1, 1, color = "green")"""

 
# Creating plot



 
# show plot
#plt.show()





## generate resource curves
folderPath = "/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/data/resources/"
filesDict = {"dead":"dead-branch-loess", "lateral":"lateral-branch-loess", "total":"total-branch-loess", "low":"low-branch-loess", "medium":"medium-branch-loess", "high":"high-branch-loess"}
resourceGraph = ["dead","lateral","total","low","medium","high"]

yMax = 240

DPREDICTIONS = {}
DLOWS = {}
DUPS= {}
DSTANDARDS = {}

resourceTitle = 'test'

print('start')

for name in filesDict.keys():
    

    dbhs = []
    predictions = []
    lowers = []
    uppers = []
    sds = []

    resource = name

    pathAll = folderPath + filesDict[resource] + '.csv'


    with open(folderPath + filesDict[resource] +'.csv') as file:
        csvreader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        header = next(csvreader)
        for row in csvreader:
            ##print(f'DBH: {row[1]} \t Prediction: {row[2]} \t lower: {row[3]} \t upper: {row[4]}'  )
            dbhwidth = row[1]
            prediction = row[2]
            lower = row[3]
            upper = row[4]
            sd = row[5]

            dbhs.append(dbhwidth)
            predictions.append(prediction)
            lowers.append(lower)
            uppers.append(upper)
            sds.append(sd)


    x = dbhs
    y = predictions

    ##create resource functions

    fpred = interp1d(x, predictions)
    flow = interp1d(x, lowers)
    fup = interp1d(x, uppers)
    fsd = interp1d(x, sds)


    #add to dictionaries
    DPREDICTIONS.update({name: fpred})
    DLOWS.update({name: flow})
    DUPS.update({name: fup})
    DSTANDARDS.update({name: fsd})


class Geoms:
    filePath = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/spatial data/10k pts barrer2b.csv'
    #river = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/spatial data/River Points.csv'
    river = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/spatial data/River Points.csv'
    count = 0
  
    def __init__(self):
        
        with open(self.filePath) as file_name:
            array = np.loadtxt(file_name, delimiter=",")

        self.points = array

        with open(self.river) as file_name:
            array = np.loadtxt(file_name, delimiter=",")

        self.riverPts = array

        
        
    def GetPoint(self):

        if(self.count > len(self.points) - 1):
            self.count = 0

        pt = self.points[self.count]
        self.count += 1
        return pt



class TreeAgent:
#relationship between age and diameter is 1.97-2.71


    age = 0.0
    exactDbh = 30.0
    dbh = int(round(exactDbh))
    isAlive = True
    lifespan = randint(400,600)
    error = ['penis']

    resources = {}
    resourcesThisYear = {}

    def __init__(self, geo):

        self.resources = {}
        self.resourcesThisYear = {}
        self.point = self.SetPoint(geo)



       
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
        
        # slow of age vs diameter is 1.97 - 2.71 - Gibbons (2009)
        growRate = randint(197, 271) / 100
        
        return 1 * (1 / growRate)

    """def SetPoint(self):
        x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        z = random.uniform(50, 100)

        return [x,y,z]"""

    def SetPoint(self, geo):

        _point = geo.GetPoint()
        return _point



class ArtificialAgent:
    performance = 0
    lifespan = ARTLIFE
    resources = {}
    resourcesThisYear = {}
    age = 0
    constrictor = 1
    isAlive = True


    def __init__(self, perf, geo):
        
        self.performance = perf
        self.point = self.SetPoint(geo)
        self.resources = {}

        for resource in RESOURCES:
                  
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

    geo = Geoms()

    

    
    @Timer(name = "Finished running model in {:.2f} seconds")
    def __init__(self):
        self.year = 0

        rivX.extend(self.geo.riverPts[:,0])
        rivY.extend(self.geo.riverPts[:,1])


        for name in RESOURCES:
            self.artResources.update({name : []}) 


        for i in range (round(self.size * self.density)):
            tree = TreeAgent(self.geo)
            self.trees.append(tree)
        
        for j in range(self.timeperiod):
            self.Cycle()
            self.year += 1

    @Timer(name = "Year in {:.2f} seconds")
    def Cycle(self):

        fig2YearsHist.append(self.year)

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



        #plt.plot(self.previousDotsX, self.previousDotsY, 'o', color = 'grey', markersize = 0.5, markeredgewidth = 0)

        #constrictor = self.GetConstrictor(self.year)

        


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

        ##iterate through list

       

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
                    
                    if j < 0.5:
                        n = 0
                        j = 0
                    if j > yMax:
                        n = yMax
                    else:
                        n = j
                    
                    resourceMetersAtThisDBH.append(float(j))

                    treesPerDBH[dbh][i].resources[resource].append(j)
                    treesPerDBH[dbh][i].resourcesThisYear.update({resource : float(j)})
                    #treesPerDBH[dbh][i].resourcesThisYear.update({resource : i})
                    
                    #treesPerDBH[dbh][i].resourcesThisYear[resource] = j

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
                    #treesPerDBH[dbh][j].resources[resource].append(j)
            
                
                    yplot.append(n)
                    xplot.append(dbh)


                    #print(f'Year: {self.year} \t DBH: {dbh}  \t Trees Alive: {self.treesAliveThisYear} \t Resource: {resource} \t Amount: {j}m')


                    if resource == 'high':
                        self.previousDotsY.append(n)
                        self.previousDotsX.append(dbh)
    

                    if resource == 'high':
                        col = 'green'

                    if resource == 'medium':
                        col = 'blue'

                
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
                

 
                #plt.plot(xplot, yplot, 'o', alpha = 0.1, color = col, markeredgewidth = 0)







        



        #plot lengts acros DB 
        #plt.title(f'Year: {self.year}   Trees Alive: {self.treesAliveThisYear}   Constrictor: {constrictor}')
        """plt.title(f'Year: {self.year}   Trees Alive: {self.treesAliveThisYear}')"""




        #plt.plot(xplot, yplot, 'o', alpha = 0.01, color = 'black', markeredgewidth = 0)

        #plt.plot(dbhSpan, lengthsAcrossDBH, 'o', DBHdist.keys, fpred(dbhSpan), '-', DBHdist.keys, flow(dbhSpan), '--', DBHdist.keys, fup(dbhSpan), '--', alpha = 0.01, color = 'black', markeredgewidth = 0)
        """plt.ylim(bottom=-1, top = yMax)
        plt.xlim(left=0, right = 130)
        plt.xlabel = 'years'
        plt.xlabel = 'branch meters'"""


        #plt.show()


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

        #print(tabulate([row1, row2, row2a, row3, row4, row5, row6, row7],headers = heads))
        #print('')
                



        sample = yrDBHS
        sample.extend([0,145])
        counts, bin_edges = np.histogram(sample, bins=75)
        fig = tpl.figure()
        fig.hist(counts, dbhSpan, grid=[15, 25], force_ascii=False)
        fig.show()


        bins = 20
        #tplt.hist(data1, bins, label="mean 0")
        #tplt.hist(data2, bins, label="mean 3")
        
        #tplt.clear_data()

       
        #tplt.sleep(0.01)

        tplt.hist(sample, bins)
        tplt.xlim(0,145)
        tplt.ylim(0,1000)


      
        tplt.canvas_color()
        tplt.title("Histogram Plot")
        tplt.xfrequency(10)
        #tplt.show()


  

        







        #ax.scatter3D(xDraw, yDraw, zDraw, s = anSize, color = "green")
        #plt.show()



        #drawnow(plt.plot())
        





        """tplt.cld()
        tplt.clt()
        tplt.clc()
        
        tplt.scatter(xT, yT, color = 'white')
        tplt.scatter(xP, yP, color = 'red')
        tplt.xlim(0,1000)
        tplt.ylim(0,1000)
        tplt.title(titl)
        tplt.show()"""


        


        #print(f"Year: {self.year} \t Trees Alive: {self.treesAliveThisYear} \t Total: {round(sum(yrResources['total']))}m \t Lateral: {round(sum(yrResources['lateral']))}m \t Dead: {round(sum(yrResources['dead']))}m \t low: {round(sum(yrResources['low']))}m \t Medium: {round(sum(yrResources['medium']))}m \t High: {round(sum(yrResources['high']))}m")
        #print(f"")
        
   
    def Recruit(self):
        recruitment = round(random.uniform(2, 3) * AREA)

        for z in range (recruitment):
            tree = TreeAgent(self.geo)
            self.trees.append(tree)

        return(f"Last recruit Year: {self.year}, {recruitment} trees")

    
    def Build(self):
        self.artPerf += ARTIMPROVE
        if self.artPerf >= ARTPERFMAX:
            self.artPerf = ARTPERFMAX

        for a in range(ARTNUMBER):
            artificial = ArtificialAgent(self.artPerf, self.geo)
            self.artificials.append(artificial)

        percent = "{:.2f}".format(self.artPerf)
        return (f"Last built Year: {self.year}, {ARTNUMBER} prosthetics @{percent}")
        
    
    def GetConstrictor(self, year):
        
        minYr = 0 
        maxYr = 100
        minConstrictor = 1
        maxConstrictor = 5000
        inConstrictorVal = ( (year - minYr) / (maxYr - minYr) ) * (maxConstrictor - minConstrictor) + minConstrictor

        constrictorVal = maxConstrictor - inConstrictorVal

        maxTrunc = 5000
        minTrunc = 1

        if constrictorVal > maxTrunc:
            constrictorVal = maxTrunc
        if constrictorVal < minTrunc:
            constrictorVal = minTrunc

        return constrictorVal

        '''print(f'Year: {year} \t Constrictor Value: {constrictor}')'''

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





## run model

            
sim = Model()

"""dfTrees = pd.DataFrame(sim.exportTree)
dfPros = pd.DataFrame(sim.exportPros)
dfTrees.to_csv(JSONOUT + 'trees.csv')
dfPros.to_csv(JSONOUT + 'prosthetics.csv')"""





with open(JSONOUT + 'resources.json', 'w', encoding='utf-8') as f:
    json.dump(sim.treeResources, f, ensure_ascii=False, indent=4)

with open(JSONOUT + 'resourcesSortedByDBH.json', 'w', encoding='utf-8') as f:
    json.dump(sim.resourcesSortedByDBH, f, ensure_ascii=False, indent=4)

with open(JSONOUT + 'ages.json', 'w', encoding='utf-8') as f:
    json.dump(sim.snapTotalAlive, f, ensure_ascii=False, indent=4)


#print sum(sim.resources[20]['dead'])


print('done')





