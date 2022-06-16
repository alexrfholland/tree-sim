import settings.setting as settings
import settings.resourcecurves as resources
import settings.geometry as geo
import simulationcore as sim
import settings.scenarios as scenario

scenario.UpdateForScenarios()

print (f'death now is {settings.deathHigh}')
print (f'allow prosthetics  is {settings.modelProsthetics}')


resources.GetResourceCurves()
geo.GetGeometry()

simulation = sim.Model()

print(simulation.noTreesAtKeyLifeStages)

print('done')