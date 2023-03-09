import simulationcore as sim
import resourcecurves as resources
import geometry as geo
import setting as settings
import pandas as pd
from datetime import *

from codetiming import Timer

import yearlyOutput as yearLog


resources.GetResourceCurves()
geo.GetGeometry()


outputFilePath = settings.MakeFolderPath(settings.SUSTAINABILITY, f'model-outputs/')



def ExportYrLog2(filePath, modelRun, exporter):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

    dfTotals = pd.DataFrame(exporter)
    path = f'{filePath}-{timestamp}-{settings.scenario}-{modelRun}.csv'
    print(f'model runn {modelRun} ended, saving {len(dfTotals)} structures to {path}')
    dfTotals.to_csv(path)

@Timer(name = "Finished running model in {:.2f} seconds")
def Go(runThese):
    #for sceneNo in range(0,len(pd.read_csv(settings.ARTIFICIALINFOPATH))):
        
        for sceneNo in runThese:
            settings.GetScenario(sceneNo)

            #print(settings.scene)
            for i in range(0,25):
            #for i in range(0,23):

                yearLog.Reset()
                simulation = sim.Model(i, sceneNo)

                print(f'{settings.samplingScenario} SCENARIO done')

                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                filePath = settings.WINDOWSOUT

                "exported!"
                #SUSTAINABILITY STUFF
                #yearLog.ExportYrLog(outputFilePath, i)
                ExportYrLog2(f'{outputFilePath}', i, simulation.sustainabilityExports)


def GoWithSpatial(strategy):
    #for sceneNo in range(0,len(pd.read_csv(settings.ARTIFICIALINFOPATH))):
        
        settings.GetScenario(strategy)

        yearLog.Reset()
        simulation = sim.Model(1,strategy)

        print(f'{settings.samplingScenario} STRATEGY done')

        simulation.spatials.ExportFrame(settings.SPATIALDATAPATH)




#order = [8,7,6,5,4,1,2,3]
#order = [1]
#order = [2] ## only got 2
order = [3]
#order = [4] ##
#order = [5] ##
#order = [6] ##
#order = [7] #current
#order = [8] #may have aleady been done?


#Go(order)
GoWithSpatial(int(input('What Scenario?')))∏