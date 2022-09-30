import pandas
import settings.setting as settings
import settings.scenarios as scenario
scenario.UpdateForScenarios()
import settings.resourcecurves as resources
import settings.geometry as geo
import simulationcore as sim
import pandas as pd
from datetime import *

import json

print (f'death now is {settings.deathHigh}')
print (f'allow prosthetics  is {settings.modelProsthetics}')


resources.GetResourceCurves()
geo.GetGeometry()

simulation = sim.Model()
simulation.GetStats()

print(simulation.vis.streamDicTree)

print(f'{settings.scenario} scenario done')

test = (1, 2, 3)

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#filePath = f'{settings.CSVOUT}{timestamp} - {settings.scenario}'
filePath = settings.WINDOWSOUT

#df = simulation.GetTreeDataFrame()
#df.to_pickle(filePath + 'treeDF.pk1')
#print(df)


#df.to_parquet(filePath + 'treeDF.parquet', engine='fastparquet')


with open(f'{filePath}trees.json', 'w') as file:
    json.dump(simulation.logAllTrees2, file, indent = 4)

with open(f'{filePath}artificials.json', 'w') as file:
    json.dump(simulation.logAllArtificials2, file, indent = 4)





"""filePath = settings.MakeFolderPath(settings.CSVOUT, f'total resources stats per year - {settings.scenario}')
dfTree = pd.DataFrame(simulation.vis.streamDicTree)
dfArticial = pd.DataFrame(simulation.vis.streamDicArt)

print('done')
print(dfTree)
print(dfArticial)


dfTree.to_csv(filePath + f"tree total resources - {settings.scenario}.csv")
dfArticial.to_csv(filePath + f"artificial total resources - {settings.scenario}.csv")"""