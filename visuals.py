from datetime import *
import sys
from tokenize import Name
import math

from matplotlib.axis import XAxis
import yearlyOutput as yrLog
#from settings.setting import *
import geometry as geo
import setting as set

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
from scipy.stats import kde


class VisualOut:
    
    fig = plt.figure(figsize= set.FIGURESIZE)
 

    figXDraw = list()tt
    figYDraw = list()
    figZDraw = list()
    figHigh = list()
    figCol = list()
    figTitle = list()

    figResource = {}
    figAll = {}

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

    streamDicTree = {}
    streamDicArt = {}
    streamTreeDivision = 5
    streamArtificialDivision = 2
    streamMax = 40



    

    def __init__(self):
        plt.ion()  # enable interactivity
        
        riverPts = geo.GeoGetRiverPoint()
        #print(riverPts)
        self.rivX = riverPts[:, 0]
        self.rivY = riverPts[:, 1]

        #print(self.rivX)
        #print(self.rivY)

        ##make timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        #print(timestamp)

        self.outPath = set.VISUALOUT + f'{set.scenario} - {timestamp}/'
        
        if not os.path.isdir(self.outPath):
            os.makedirs(self.outPath)

        #initialise stream graph
        for i in range(int(self.streamMax/self.streamTreeDivision)+1):
            tree = i#f'{i}+a'
            self.streamDicTree.update({tree : []})

        for i in range(int(self.streamMax/self.streamArtificialDivision)+1):
            art = i#f'{i}+t'
            self.streamDicArt.update({art : []})

        

    
    def Make_FigA(self):
        self.fig.suptitle(self.figTitle[-1], fontsize=16)

        # Create 4x4 Grid
        gs = self.fig.add_gridspec(nrows=3, ncols=2, height_ratios=[1,1,1], width_ratios=[1,1], wspace = 0.1, hspace = 0.3)

        # Create Three Axes Objects
        axMap = self.fig.add_subplot(gs[:, 0])
        ax2 = self.fig.add_subplot(gs[0, 1])
        ax3 = self.fig.add_subplot(gs[1, 1])
        ax4 = self.fig.add_subplot(gs[2, 1])

        #HEATMAP HIGH + ARTIFICIAL
        heatmap1, xedges1, yedges1 = np.histogram2d(self.figXDraw, self.figYDraw,  bins=200, weights= self.figHigh, density = False)
        extent1 = [xedges1[0], xedges1[-1], yedges1[0], yedges1[-1]]
        #print(extent1)
        #extent1 = [-654.465282154,  2103.81760729, -1301.10671195, 1457.176178]
            
        #circles on prosthetics
        axMap.scatter(self.figProsX, self.figProsY, s = 100, c = 'none', edgecolors='white', alpha=.25)

        #river
        axMap.plot(self.rivX, self.rivY, linewidth = 0.5, c = '#753183')
        #print(self.rivX)
        #axMap.scatter(rivX, rivY, s = 15, c = '#753183')
        
        #heatmap
        im = axMap.imshow(heatmap1.T, extent=extent1, origin='lower', cmap = 'viridis', vmin = 0, vmax = set.RESOURCECAPS[set.FOCUSRESOURCE])  

        # Define the limits, labels, ticks as required
        axMap.set_xlim([-654.465282154,  2103.81760729])
        axMap.set_ylim([-1301.10671195, 1457.176178])
        axMap.set_xlabel(r' ') # Force this empty !
        #axes[name].set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
        axMap.set_xticklabels([]) # Force this empty

        axMap.set_ylabel(r' ') # Force this empty !
        #axes[name].set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
        axMap.set_yticklabels([]) # Force this empty !

        axMap.set_title(set.scenario)

        axMap.set_facecolor('#440154')
        
        #TOTAL RESOURCES
        #pal = sns.color_palette("Set1")
        
        ax2.stackplot(self.fig2YearsHist, self.fig2HistTree, self.fig2HistProsthetic, labels = ['x', 'y'])
        ax2.set_title('Cumulative High Resources')


        #HEATMAP: DISTRIBUTION OF HIGH RESOURCES PER TREE
        heatmap, xedges, yedges = np.histogram2d(self.fig3YrssPerTree ,self.fig3ResPerTree, bins=200, density = False, weights = self.fig3ResPerTree)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #extentB = [0, 250, 0, 40]
        im = ax3.imshow(heatmap.T, extent=extent, origin='lower', cmap = 'viridis', vmin = 0, vmax = 20)  
        ax3.set_title('Distribution of High Resources Per Natural Trees')

        print(self.fig3ResPerProsthetic)


        #HEATMAP: DISTRIBUTION OF HIGH RESOURCES PER PROSTHETIC
        x = [0]
        y = [0]

        x.extend(self.fig3YrssPerProsthetic)
        y.extend(self.fig3ResPerProsthetic)
        
        heatmap, xedges, yedges = np.histogram2d(x , y, bins=200, density = False, weights = y)

        #heatmap, xedges, yedges = np.histogram2d(self.fig3YrssPerProsthetic ,self.fig3ResPerProsthetic, bins=200, density = False, weights = self.fig3ResPerProsthetic)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #extentC = [0, 250, 0, 40]
        #extent = [0, 250, 0, 30]
        im = ax4.imshow(heatmap.T, extent=extent, origin='lower', cmap = 'viridis', vmin = 0, vmax = 20)
        ax4.set_title('Distribution of High Resources Per Prosthetics')

        plt.tight_layout()


    def Make_FigC(self):
        """heatmap, xedges, yedges = np.histogram2d(figXDraw, figYDraw,  bins=200, weights= figHigh, density = False)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]"""

        set.modifier = 0.3
        
        #HEATMAP HIGH + ARTIFICIAL
        heatmap1, xedges1, yedges1 = np.histogram2d(self.figXDraw, self.figYDraw,  bins=60, weights= self.figHigh, density = False)
        extent1 = [xedges1[0], xedges1[-1], yedges1[0], yedges1[-1]]
        
        #circles on prosthetics
        plt.scatter(self.figProsX, self.figProsY, s = 300, c = 'none', edgecolors='white', alpha=.25, linewidths = 1)

        #river
        plt.plot(self.rivX, self.rivY, linewidth = 2, c = '#753183')

        #heatmap
        im = plt.imshow(heatmap1.T, extent=extent1, origin='lower', cmap = 'viridis', vmin = 0, vmax = set.RESOURCECAPS[set.FOCUSRESOURCE])  

        plt.xlim([-654.465282154,  2103.81760729])
        plt.ylim([-1301.10671195, 1457.176178])

        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        ax.axes.set_facecolor('#440154')

    
    def Make_FigB(self):
        # Create 4x4 Grid

        self.fig.suptitle(self.figBTitle[-1], fontsize=16)
        
        colbarWidth = 0.025
        spaceWidth = 0.1
        gs = self.fig.add_gridspec(nrows=2, ncols=8, height_ratios=[1, 1], width_ratios=[1, colbarWidth, spaceWidth, 1, colbarWidth, spaceWidth, 1, colbarWidth], wspace = 0.2, hspace = 0.2)

        axes = {}
        axes.update({'total' : self.fig.add_subplot(gs[0, 0])})
        axes.update({'lateral' : self.fig.add_subplot(gs[0, 3])})
        axes.update({'dead' : self.fig.add_subplot(gs[0, 6])})
        axes.update({'low' : self.fig.add_subplot(gs[1, 0])})
        axes.update({'medium' : self.fig.add_subplot(gs[1, 3])})
        axes.update({'high' : self.fig.add_subplot(gs[1, 6])})

        bars = {}
        bars.update({'total' : plt.subplot(gs[0,1])})
        bars.update({'lateral' : plt.subplot(gs[0,4])})
        bars.update({'dead' : plt.subplot(gs[0,7])})
        bars.update({'low' : plt.subplot(gs[1,1])})
        bars.update({'medium' : plt.subplot(gs[1,4])})
        bars.update({'high' : plt.subplot(gs[1,7])})

        
        for name in set.RESOURCES:
            heatmap, xedges, yedges = np.histogram2d(self.fig4TreeLocXThisYear, self.fig4TreeLocYThisYear,  bins=200, weights= self.figResource[name], density = False)
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #extent = [-1000, 2000, -1000, 2000]

            im = axes[name].imshow(heatmap.T, extent=extent, origin='lower', cmap = 'viridis', vmin = 0, vmax = set.RESOURCECAPS[name])
            
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

            axes[name].plot(self.rivX, self.rivY, linewidth = 0.4, c = '#753183')
            axes[name].set_xlim([-654.465282154,  2103.81760729])
            axes[name].set_ylim([-1301.10671195, 1457.176178])
            axes[name].set_facecolor('#440154')


            cbax = bars[name]
            cb = Colorbar(ax = cbax, mappable = im, orientation = 'vertical', ticklocation = 'right')
        

        plt.tight_layout()


    ###not working
    def Make_FigAgainSmoothMini(self):

        name = 'high'
        
        # create data
        x = self.figXDraw
        y = self.figYDraw
        
        set.modifier = 0.3

        #print(len(self.figXDraw))
        #print(len(self.figAll['high']))

        w = []


        # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
        nbins=50

        for val in self.figAll[name]:
            if val <= 0:
                val = .1
                w.append(val)


        #print(f"{name} is {w}")

        
        k = kde.gaussian_kde([x,y], weights = w)
        

        
        #xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
        xi, yi = np.mgrid[set.BOUNDS[0]:set.BOUNDS[1]:nbins*1j, set.BOUNDS[2]:set.BOUNDS[3]:nbins*1j]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))


        # Make the plot
        plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto', vmin = 0, vmax = .000002)

        # Change color palette
        #plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto', cmap=plt.cm.Greens_r, vmin = 0, vmax = 20)
        #plt.show()

        #circles on prosthetics
        plt.scatter(self.figProsX, self.figProsY, s = 300, c = 'black', edgecolors='white', alpha=.25, linewidths = 1)

        #river
        plt.plot(self.rivX, self.rivY, linewidth = 2, c = '#753183')

        plt.xlim([-654.465282154,  2103.81760729])
        plt.ylim([-1301.10671195, 1457.176178])

    
    def Make_FigB_Mini(self):

        #set.modifier = 10

        for name in set.RESOURCES:
        
            #print (f'{name} limit is {set.RESOURCECAPS[name]}')
            heatmap1, xedges1, yedges1 = np.histogram2d(self.fig4TreeLocXThisYear, self.fig4TreeLocYThisYear,  bins=60, weights= self.figResource[name], density = False)
            extent1 = [xedges1[0], xedges1[-1], yedges1[0], yedges1[-1]]
            
            #circles on prosthetics
            plt.scatter(self.figProsX, self.figProsY, s = 300, c = 'none', edgecolors='white', alpha=.25, linewidths = 1)

            #river
            plt.plot(self.rivX, self.rivY, linewidth = 2, c = '#753183')

            #heatmap
            im = plt.imshow(heatmap1.T, extent=extent1, origin='lower', cmap = 'viridis', vmin = 0, vmax = set.RESOURCECAPS[name])  

            plt.xlim([-654.465282154,  2103.81760729])
            plt.ylim([-1301.10671195, 1457.176178])

            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
            ax.axes.set_facecolor('#440154')    

            plt.savefig(self.outPath + f'{yrLog.year} - {name} - {set.scenario}.jpg', bbox_inches='tight')

    def Make_Stream(self):

        df = pd.DataFrame(self.streamDicTree)
        
        #print(df)

        ax = plt.gca()
        #fig, ax = plt.subplots(figsize=(10,5))


        # Plot a stackplot - https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/stackplot_demo.html
        ax.stackplot(df.index, df.T, baseline='wiggle', labels=df.columns)

        # Move the legend off of the chart
        ax.legend(loc=(1.04,0))


            
        
        
    def Update(self):

        #####


        self.figXDraw.clear()
        self.figYDraw.clear()
        self.figZDraw.clear()
        self.figProsX.clear()
        self.figProsY.clear()

        self.figHigh.clear()
        self.figCol.clear()
        self.figTitle.clear()
        self.figBTitle.clear()


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

        self.fig2YearsHist.append(yrLog.year)

        self.figResource.clear()
        self.figAll.clear()
        self.fig4TreeLocXThisYear.clear()
        self.fig4TreeLocYThisYear.clear()

        #####

        for resourceN in set.RESOURCES:
            self.figResource.update({resourceN : []})
            self.figAll.update({resourceN : []})

        #strean
        
        yrStreamTree = {}
        yrStreamArt = {}

        for i in range(int(self.streamMax/self.streamTreeDivision)+1):
            tree = i#f'{i}+a'
            yrStreamTree.update({tree : 0})
        

        for i in range(int(self.streamMax/self.streamArtificialDivision)+1):
            art = i#f'{i}+t'
            yrStreamArt.update({art : 0})
        
        
        for tree in yrLog.trees:
            
            if tree.isAlive:
                xT.append(tree.point[0])
                yT.append(tree.point[1])
                zT.append(tree.point[2])

                resourceT.append(tree.resourcesThisYear[set.FOCUSRESOURCE])
                colT.append('blue')

                self.fig3ResPerAgent.append(tree.resourcesThisYear[set.FOCUSRESOURCE])
                self.fig3ColsPerAgent.append('blue')
                self.fig3YrssPerAgent.append(yrLog.year)

                self.fig3ResPerTree.append(tree.resourcesThisYear[set.FOCUSRESOURCE])
                self.fig3YrssPerTree.append(yrLog.year)

                for resourceN in set.RESOURCES:
                    self.figResource[resourceN].append(tree.resourcesThisYear[resourceN])
                    self.figAll[resourceN].append(tree.resourcesThisYear[resourceN])

                self.fig4TreeLocXThisYear.append(tree.point[0])
                self.fig4TreeLocYThisYear.append(tree.point[1])

                if(tree.resourcesThisYear['high'] > 0):
                    #key = self.GetStreamKey(tree.resourcesThisYear['high'], 't')
                    key = self.GetStreamKey(tree.resourcesThisYear['high'], 't')
                    #print(yrStreamTree)
                    yrStreamTree[key] += 1

                



                #self.exportTree['high'].append(tree.resourcesThisYear['high'])
                #self.exportTree['year'].append(tree.age)

                #stream



        for prosthetic in yrLog.artificials:
            if prosthetic.isAlive:    
                xP.append(prosthetic.point[0])
                yP.append(prosthetic.point[1])
                colP.append('red')
                resourceP.append(prosthetic.resourcesThisYear['high'])
                #high.append[tree.resources["high"]]"""

                self.figProsX.append(prosthetic.point[0])
                self.figProsY.append(prosthetic.point[1])

                self.fig3ResPerAgent.append(prosthetic.resourcesThisYear[set.FOCUSRESOURCE])
                self.fig3ColsPerAgent.append('red')
                self.fig3YrssPerAgent.append(yrLog.year)

                self.fig3ResPerProsthetic.append(prosthetic.resourcesThisYear[set.FOCUSRESOURCE])
                self.fig3YrssPerProsthetic.append(yrLog.year)

                for resourceN in set.RESOURCES:
                        self.figAll[resourceN].append(tree.resourcesThisYear[resourceN])

                #self.exportPros['high'].append(prosthetic.resources['high'])
                #self.exportPros['year'].append(self.year)

                #stream

                if prosthetic.resourcesThisYear['high'] >= 0:
                    key = self.GetStreamKey(prosthetic.resourcesThisYear['high'], 'a')
                    yrStreamArt[key] += 1
                    #print("year")
                    #print(yrStreamArt)



        """for i in range(len(xT)):
            print(f"TX {i}\t{xT[i]}")
            print(f"TY {i}\t{yT[i]}")
            print(f"PX {i}\t{xP[i]}")
            print(f"PY {i}\t{yP[i]}")"""
        

        self.figXDraw.extend(xT)
        self.figYDraw.extend(yT)  # or any arbitrary update to your figure's data
        self.figZDraw.extend(zT)
        self.figHigh.extend(resourceT)
        self.figCol.extend(colT)

        self.figXDraw.extend(xP)
        self.figYDraw.extend(yP)  # or any arbitrary update to your figure's data
        #zDraw.extend(zP)
        self.figHigh.extend(resourceP)
        self.figCol.extend(colP)

        self.fig2HistTree.append(sum(resourceT))
        self.fig2HistProsthetic.append(sum(resourceP))

        
        treesAlive = "{:,}".format(yrLog.noTreesAliveThisYear)
        prostheticsAlive = "{:,}".format(yrLog.noArtificialsAliveThisYear)
        
        txt = f"Year: {yrLog.year}       Trees: {treesAlive}        Prosthetics: {prostheticsAlive}        Max DBH: {yrLog.maxDBH}cm       Average Tree:  {yrLog.averageDBH}cm         Max Perf: {yrLog.maxArtPerf}%"

        self.figTitle.append(txt)

        txtB = f"Year: {yrLog.year}          Trees: {treesAlive}"
        self.figBTitle.append(txtB)

        for key in yrStreamTree.keys():
            #print(key)
            self.streamDicTree[key].append(yrStreamTree[key])

        for key in yrStreamArt.keys():
            #print(key)
            self.streamDicArt[key].append(yrStreamArt[key])

        

        #drawnow(self.Make_FigA)
        #drawnow(self.Make_FigB)

        
        
        #drawnow(self.Make_FigAgainSmoothMini)

        #drawnow(self.Make_Stream)

        #drawnow(self.Make_FigB_Mini)

        #drawnow(self.Make_FigC)


        ##DRAWINGOUT - enable this to export images

        #plt.savefig(self.outPath + f'{yrLog.year} - {set.scenario}.jpg', bbox_inches='tight', dpi = 150)
        #print(f'saved fig {self.outPath}')
        
        if set.ISVISOUT: 
            plt.savefig(self.outPath + f'{yrLog.year} - {set.scenario}.png', bbox_inches='tight', dpi = 150)
            print(f'saved fig {self.outPath}')

    def GetStreamKey(self, value, append):
        
        if(value > self.streamMax):
            value = self.streamMax
        val = math.floor(value/self.streamTreeDivision)

        key = val#f'{val}+{append}'
        return key
        
        """if(value > self.streamMax):
            value = self.streamMax
        val = int(value/self.streamDivision)

        key = f'{val}+{append}'
        return key"""
