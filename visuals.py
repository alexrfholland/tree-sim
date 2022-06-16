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


def MakeVisuals():
    
    figXDraw.clear()
    figYDraw.clear()
    figZDraw.clear()
    figProsX.clear()
    figProsY.clear()

    figHigh.clear()
    figCol.clear()
    figTitle.clear()
    figBTitle.clear()
    sizeMultiplier = 3


    xT = []
    yT = []
    zT = []
    resourceT = []
    colT = []


    dbh = []
    high = []

    xP = []
    yP = []
    resourceP = []
    colP = []

    figResource.clear()
    fig4TreeLocXThisYear.clear()
    fig4TreeLocYThisYear.clear()

    for resourceN in RESOURCES:
        figResource.update({resourceN : []})

    for tree in self.trees:
        
        if tree.isAlive:
            xT.append(tree.point[0])
            yT.append(tree.point[1])
            zT.append(tree.point[2])
            #sizeT.append((tree.dbh * tree.dbh) * sizeMultiplier)
            #sizeT.append((tree.dbh * tree.dbh) * sizeMultiplier)
            #print(tree.resources["high"])
            resourceT.append(tree.resourcesThisYear[FOCUSRESOURCE] * sizeMultiplier + 0.001)
            colT.append('blue')
            #print(tree.resourcesThisYear['total'])
            #print(tree.resources["high"][-1])
            #sizeT.append[tree.resources["high"][-1]]

            fig3ResPerAgent.append(tree.resourcesThisYear[FOCUSRESOURCE])
            fig3ColsPerAgent.append('blue')
            fig3YrssPerAgent.append(self.year)

            fig3ResPerTree.append(tree.resourcesThisYear[FOCUSRESOURCE])
            fig3YrssPerTree.append(self.year)

            for resourceN in RESOURCES:
                figResource[resourceN].append(tree.resourcesThisYear[resourceN])

            fig4TreeLocXThisYear.append(tree.point[0])
            fig4TreeLocYThisYear.append(tree.point[1])

            self.exportTree['high'].append(tree.resourcesThisYear['high'])
            self.exportTree['year'].append(tree.age)

    for prosthetic in self.artificials:
        if prosthetic.isAlive:    
            xP.append(prosthetic.point[0])
            yP.append(prosthetic.point[1])
            colP.append('red')
            resourceP.append(prosthetic.resources['high'] * sizeMultiplier)
            #high.append[tree.resources["high"]]"""

            figProsX.append(prosthetic.point[0])
            figProsY.append(prosthetic.point[1])

            fig3ResPerAgent.append(prosthetic.resources[FOCUSRESOURCE])
            fig3ColsPerAgent.append('red')
            fig3YrssPerAgent.append(self.year)

            fig3ResPerProsthetic.append(prosthetic.resources[FOCUSRESOURCE])
            fig3YrssPerProsthetic.append(self.year)

            self.exportPros['high'].append(prosthetic.resources['high'])
            self.exportPros['year'].append(self.year)


    """for i in range(len(xT)):
        print(f"TX {i}\t{xT[i]}")
        print(f"TY {i}\t{yT[i]}")
        print(f"PX {i}\t{xP[i]}")
        print(f"PY {i}\t{yP[i]}")"""
    

    figXDraw.extend(xT)
    figYDraw.extend(yT)  # or any arbitrary update to your figure's data
    figZDraw.extend(zT)
    figHigh.extend(resourceT)
    figCol.extend(colT)

    figXDraw.extend(xP)
    figYDraw.extend(yP)  # or any arbitrary update to your figure's data
    #zDraw.extend(zP)
    figHigh.extend(resourceP)
    figCol.extend(colP)

    fig2HistTree.append(sum(resourceT))
    fig2HistProsthetic.append(sum(resourceP))

    
    treesAlive = "{:,}".format(self.treesAliveThisYear)
    prostheticsAlive = "{:,}".format(noArt)


    txt = f"Year: {self.year} {treesAlive} trees {noArt} Prosthetics Avrg DBH: {averageDBH}cm Max DBH: {maxDBH}cm Avrg Perf: {averageArtPerf}%  Max Perf: {maxArtPerf}%"
    
    txt = f"Year: {self.year}       Trees: {treesAlive}        Prosthetics: {prostheticsAlive}        Max DBH: {maxDBH}cm       Average Tree:  {averageDBH}cm         Max Perf: {maxArtPerf}%"

    figTitle.append(txt)

    txtB = f"Year: {self.year}          Trees: {treesAlive}"
    figBTitle.append(txtB)


    drawnow(Make_FigA)
    #drawnow(Make_FigB)