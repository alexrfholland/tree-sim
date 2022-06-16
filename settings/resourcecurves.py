import os
import csv

# generate random integer values
from scipy.interpolate import interp1d

#import script.settings.setting as settings
from settings.setting import *


DPREDICTIONS = {}
DLOWS = {}
DUPS= {}
DSTANDARDS = {}

def GetResourceCurves():

    for name in FILESDICT.keys():
        
        dbhs = []
        predictions = []
        lowers = []
        uppers = []
        sds = []

        resource = name

        pathAll = FOLDERPATH + FILESDICT[resource] + '.csv'

        with open(FOLDERPATH + FILESDICT[resource] +'.csv') as file:
            csvreader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
            header = next(csvreader)
            for row in csvreader:
                #print(f'DBH: {row[1]} \t Prediction: {row[2]} \t lower: {row[3]} \t upper: {row[4]}'  )
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

    print('Generated resource curves')