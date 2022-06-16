import yearlyOutput as yrLog
from settings.setting import *
from tabulate import tabulate
import termplotlib as tpl

import numpy as np


def TextOut():
    
    
    #print(f'no trees alive this year is {yrLog.noTreesAliveThisYear}')


    noTree = yrLog.noTreesAliveThisYear
    noArt = yrLog.noArtificialsAliveThisYear
    dbhSpan = range(TREESTARTDBH, MAXDBH)

    #print(noTree)


    row1 = []
    row2 = []
    row2a = []
    row3 = []
    row4 = []

    if noTree > 0:
        row1 = ['Natural Trees', f'{noTree} trees']
        row2 = ['Per Tree', f'Avrg DBH: {yrLog.averageDBH}cm']
        row2a = ['Max', f'Max DBH: {yrLog.maxDBH}cm']

        for name in RESOURCES:
            met0 = round(sum(yrLog.yrTreeResources[name]))
            met1= "{:,}".format(met0)
            met2 = "{:,}".format(round(met0/noTree))

            maxRes = max(yrLog.yrTreeResources[name])
            #if name == 'high':
                #print(f'Year: {self.year} \t totalHigh: {met0} \t maxHigh: {maxRes}m \t meanHigh: {met2}m')

            row1.append(f"{met1}m")
            row2.append(f"{met2}m/tree")
            row2a.append(f'{maxRes}m')

    if noArt > 0:
        averageArtPerf = "{:.2f}".format(sum(yrLog.yrArtPerf)/noArt)
        maxArtPerf = "{:.2f}".format(max(yrLog.yrArtPerf))

        row3 = ['Prosthetic Structures ', f'{noArt} structures' ]
        row4 = ['Per Artificial', f'Avrg Perf: {averageArtPerf}%, Max Perf: {maxArtPerf}%']

        for name in RESOURCES:

            artMet0 = round(sum(yrLog.yrArtResources[name]))
            artMet1= "{:,}".format(artMet0)
            artMet2 = "{:,}".format(round(artMet0/noArt))

            row3.append(f"{artMet1}m")
            row4.append(f"{artMet2}m/structure")

    row5 = ["-------------------------------------------"]

    row6 = [yrLog.recruitMessage]
    row7 = [yrLog.builtMesssage]

    heads = [f"Year: {yrLog.year}", 'Habitat Structures']
    heads.extend(RESOURCES)
    if yrLog.isRecruit:
        row6 = [UPDATEMESSAGE]
    if yrLog.isBuilt:
        row7 = [UPDATEMESSAGE]

    
    #print([row1, row2, row2a, row3, row4, row5, row6, row7])
    print(tabulate([row1, row2, row2a, row3, row4, row5, row6, row7],headers = heads))
    print("")            

    sample = yrLog.yrDBHS
    sample.extend([0,145])
    counts, bin_edges = np.histogram(sample, bins=75)
    fig = tpl.figure()
    fig.hist(counts, dbhSpan, grid=[15, 25], force_ascii=False)
    fig.show()