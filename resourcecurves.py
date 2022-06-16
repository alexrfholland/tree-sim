import csv
import os
import numpy as np
from pyparsing import dblSlashComment
from scipy import rand
from scipy.interpolate import interp1d

import script.setting as settings
#from setting import *


# generate random integer values
from random import seed
from random import randint

# seed random number generator
seed(1)

## generate resource curves


DPREDICTIONS = {}
DLOWS = {}
DUPS= {}
DSTANDARDS = {}

resourceTitle = 'test'


print(settings.TIMEPERIOD)

print('start')

print(FILESDICT)



for name in settings.FILESDICT.keys():
    

    
    dbhs = []
    predictions = []
    lowers = []
    uppers = []
    sds = []

    resource = name

    pathAll = settings.FOLDERPATH + settings.FILESDICT[resource] + '.csv'

    with open(settings.FOLDERPATH + settings.FILESDICT[resource] +'.csv') as file:
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

    print(DPREDICTIONS)