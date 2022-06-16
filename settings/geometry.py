import numpy as np

from settings.setting import *
from settings.resourcecurves import *

geoRandomPointsPath = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/spatial data/10k pts barrer2b.csv'
river = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/spatial data/River Points.csv'
count = 0
points = []

def GetGeometry():
    global points
    global riverPts
    
    with open(geoRandomPointsPath) as file_name:
        points = np.loadtxt(file_name, delimiter=",")
    print('Geometry imported')


def GeoGetPoint():
    global count

    if(count > len(points) - 1):
        count = 0
        print('reached pt threshold, resetting')

    pt = points[count]
    count += 1

    if DEBUG:
        print(f'count is {count} \t point grabbed {pt}')
    return pt

def GeoGetRiverPoint():
    with open(river) as file_name:
        riverPts = np.loadtxt(file_name, delimiter=",")
        print(f'imported {len(riverPts)} river points!')

    print(f'returned {len(riverPts)} river points!')
    return riverPts