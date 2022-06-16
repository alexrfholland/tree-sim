
from tabulate import tabulate
import termplotlib as tpl
from settings.setting import *

import numpy as np


treesAliveThisYear
yrAliveArt

yrDBHS
yrTreeResources
yrArtPerf
yrArtResources

isRecruit
isBuilt

recruitMessage
builtMesssage

year


def YrOutputLog(_treesAliveThisYear, _yrAliveArt, _yrDBHS, _yrTreeResources, _yrArtPerf, _yrArtResources, _isRecruit, _isBuilt, _recruitMessage, _builtMesssage, _year):
    dbhSpan = range(TREESTARTDBH,MAXDBH)
    global treesAliveThisYear
    global yrAliveArt
    global yrDBHS
    global yrTreeResources
    global yrArtPerf
    global yrArtResources
    global isRecruit
    global isBuilt
    global recruitMessage
    global builtMesssage
    global year

    treesAliveThisYear = _treesAliveThisYear
    yrAliveArt = _yrAliveArt

    yrDBHS = _yrDBHS
    yrTreeResources = _yrTreeResources
    yrArtPerf = _yrArtPerf
    yrArtResources = _yrArtResources

    isRecruit = _isRecruit
    isBuilt = _isBuilt
    
    recruitMessage = _recruitMessage
    builtMesssage = _builtMesssage

    year = _year




    no = int(treesAliveThisYear)
    noArt = int(len(yrAliveArt))

    row1 = []
    row2 = []
    row2a = []
    row3 = []
    row4 = []

    if no > 0:
        averageDBH = round(sum(yrDBHS)/len(yrDBHS))
        maxDBH = max(yrDBHS)
        row1 = ['Natural Trees', f'{no} trees']
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

    row6 = [recruitMessage]
    row7 = [builtMesssage]

    heads = [f"Year: {year}", 'Habitat Structures']
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