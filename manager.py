import pandas
import setting as settings
#import settings.scenes as SCENARIO
#SCENARIO.UpdateForSCENARIOs()
import resourcecurves as resources
import geometry as geo
import simulationcore as sim
import pandas as pd
from datetime import *

import yearlyOutput as yearLog

import json

print (f'death now is {settings.deathHigh}')
print (f'allow prosthetics  is {settings.modelProsthetics}')
print(f'art perf is {settings.ARTPERFMIN}')



resources.GetResourceCurves()
geo.GetGeometry()

simulation = sim.Model()
simulation.GetStats()


print(f'{settings.scenario} SCENARIO done')

test = (1, 2, 3)

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#filePath = f'{settings.CSVOUT}{timestamp} - {settings.SCENARIO}'
filePath = settings.WINDOWSOUT

df = simulation.GetTreeDataFrame()
#df.to_pickle(filePath + 'treeDF.pk1')
#print(df)

#SUSTAINABILITY STUFF
yearLog.ExportYrLog()


df.to_parquet(filePath + 'treeDF.parquet', engine='fastparquet')
print(f'saved {df}')

"""with open(f'{filePath}trees.json', 'w') as file:
    json.dump(simulation.logAllTrees2, file, indent = 4)

with open(f'{filePath}artificials.json', 'w') as file:
    json.dump(simulation.logAllArtificials2, file, indent = 4)

"""

"""filePath = settings.MakeFolderPath(settings.CSVOUT, f'total resources stats per year - {settings.SCENARIO}')
dfTree = pd.DataFrame(simulation.vis.streamDicTree)240

dfArticial = pd.DataFrame(simulation.vis.streamDicArt)

print('done')
print(dfTree)
print(dfArticial)


dfTree.to_csv(filePath + f"tree total resources - {settings.SCENARIO}.csv")
dfArticial.to_csv(filePath + f"artificial total resources - {settings.SCENARIO}.csv")"""