from agentartificial import ArtificialAgent
from agenttree import TreeAgent
from typing import List
from typing import Dict 
from datetime import *
import pandas as pd



class spatialExporter:
    
    trees: List[TreeAgent] = []
    artificials: List[ArtificialAgent] = []
    resources = ['total', 'dead', 'lat', 'high']  


    

    def __init__(self, _scene):
        self.scene = _scene
        
        self.sustainabilityExports = {
        "strategyNo" : [],
        "strategy" : [],
        "mode" : [],
        "year" : [],
        "x" : [],
        "y" : [],
        "treeHigh" : [],
        "total" : [],
        "dead" : [],
        "lateral" : [],
        "high" : []}        

    def GetYearlyTotalsSustain(self, trees: List[TreeAgent], artificials: List[ArtificialAgent], year):
            
        treeCount = 0
        artificialCount = 0

        for agent in artificials:
            if agent.isAlive:
                self.AddAgentToDataFrame(agent.point[0],
                              agent.point[1],
                              0,
                              agent.resourcesThisYear["total"],
                              agent.resourcesThisYear["dead"],
                              agent.resourcesThisYear["lateral"],
                              agent.resourcesThisYear["high"],
                              year)
                artificialCount = artificialCount + 1
                
        for agent in trees:
            if agent.isAlive:
                self.AddAgentToDataFrame(agent.point[0],
                              agent.point[1],
                              agent.resourcesThisYear["high"],
                              agent.resourcesThisYear["total"],
                              agent.resourcesThisYear["dead"],
                              agent.resourcesThisYear["lateral"],
                              agent.resourcesThisYear["high"],
                              year)
                treeCount = treeCount + 1
                
        print(f"added {treeCount} trees and {artificialCount} artificials to file")


    def AddAgentToDataFrame(self, x, y, treeHigh, total, dead, lat, high, year):
        self.sustainabilityExports["strategyNo"].append(self.scene["no"])
        self.sustainabilityExports["strategy"].append(self.scene["scenario"])
        self.sustainabilityExports["mode"].append(self.scene["mode"])
        self.sustainabilityExports["year"].append(year)
        self.sustainabilityExports["x"].append(x)
        self.sustainabilityExports["y"].append(y)
        self.sustainabilityExports["treeHigh"].append(treeHigh)
        self.sustainabilityExports["total"].append(total)
        self.sustainabilityExports["dead"].append(dead)
        self.sustainabilityExports["lateral"].append(lat)
        self.sustainabilityExports["high"].append(high)

    def ExportFrame(self, filePath):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        dfKDELocs = pd.DataFrame(self.sustainabilityExports)

        path = f"{filePath}-{self.scene['no']}-{timestamp}-{self.scene['scenario']}.parquet"
        print(f"model run {self.scene['scenario']} ended, saving {len(dfKDELocs)} structures to {path}")
        dfKDELocs.to_parquet(path)
