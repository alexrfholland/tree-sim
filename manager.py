import pandas
#import settings.scenes as SCENARIO
#SCENARIO.UpdateForSCENARIOs()
import simulationcore as sim
import resourcecurves as resources
import geometry as geo
import setting as settings
import pandas as pd
from datetime import *

from codetiming import Timer

import yearlyOutput as yearLog

import json
1

resources.GetResourceCurves()
geo.GetGeometry()


outputFilePath = settings.MakeFolderPath(settings.SUSTAINABILITY, f'model-outputs/')

@Timer(name = "Finished running model in {:.2f} seconds")
def Go():
    for sceneNo in range(0,len(pd.read_csv(settings.ARTIFICIALINFOPATH))):
    #for sceneNo in range(0,1):

        df = pd.read_csv(settings.ARTIFICIALINFOPATH)
        sampling = df['samplingType'][sceneNo]
        design = df['id'][sceneNo]
        print(design)

        if sampling != "linear":
            
            settings.GetScenario(sceneNo)
            #print(settings.scene)
            for i in range(0,1):

                yearLog.Reset()
                simulation = sim.Model(i, sceneNo)

                print(f'{settings.samplingScenario} SCENARIO done')

                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                filePath = settings.WINDOWSOUT

                #SUSTAINABILITY STUFF
                yearLog.ExportYrLog(outputFilePath, i)


def Go2():
    #for sceneNo in range(0,len(pd.read_csv(settings.ARTIFICIALINFOPATH))):
    for sceneNo in range(0,1):
            
        settings.GetScenario(sceneNo)

        #print(settings.scene)
        for i in range(0,1):

            yearLog.Reset()
            simulation = sim.Model(i, sceneNo)

            print(f'{settings.samplingScenario} SCENARIO done')

            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filePath = settings.WINDOWSOUT

            #SUSTAINABILITY STUFF
            yearLog.ExportYrLog(outputFilePath, i)

def Go3(maxScene):
    #for sceneNo in range(0,len(pd.read_csv(settings.ARTIFICIALINFOPATH))):
        
        for sceneNo in range (1, maxScene):
            settings.GetScenario(sceneNo)

            #print(settings.scene)
            for i in range(0,1):

                yearLog.Reset()
                simulation = sim.Model(i, sceneNo)

                print(f'{settings.samplingScenario} SCENARIO done')

                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                filePath = settings.WINDOWSOUT

                "exported!"
                #SUSTAINABILITY STUFF
                yearLog.ExportYrLog(outputFilePath, i)


#Go3(int(input("scene number?")))

for i in range (1,9):
    Go3(i)



#df.to_parquet(filePath + 'treeDF.parquet', engine='fastparquet')
#print(f'saved {df}')

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