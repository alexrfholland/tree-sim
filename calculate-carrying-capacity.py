import numpy as np
import pandas as pd
import open3d as o3d

from typing import List
from typing import Dict

import time


treeFiles = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/Input Data/fullBranchData.csv'
artificialFiles = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/Input Data/snags/'

out = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/carrying/'

imageOut = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Images/'


measure = 'suitable'
#measure = 'deadlat'



minSuit = 1.536
voxelSize = 10

carrying = {
    'treeSize' : [],
    'carryUnits' : [],
    'samplingSize' : [],
    'type' : [],
    'id' : [],
    'number-id' : [],
    'suitLengths' : [],
    'totalLengths' : []}

def GetCapacities(min, size, da):

    frames: Dict[str, List[pd.DataFrame]] = {}
    suitFrames: Dict[str, List[pd.DataFrame]] = {}
    pts: Dict[str, List[o3d.geometry.PointCloud]] = {}
    suitPts: Dict[str, List[o3d.geometry.PointCloud]] = {}
    carryingVoxels: Dict[str, List[o3d.geometry.VoxelGrid]] = {}
    carryingCoords: Dict[str, List[np.ndarray]] = {}

    treeDBH = []


    def LoadFrames():
        
        _frames: Dict[str, List[pd.DataFrame]] = {}
        _suitFrames: Dict[str, List[pd.DataFrame]] = {}

        #trees
        _treeFrames: List[pd.DataFrame] = []
        _treeSuitFrames: List[pd.DataFrame] = []

        for i in range(1,17):
            df = pd.read_csv(treeFiles)
            tempTreeFrame = df[df['Tree.ID'] == i]
            
            
            #are we basing these off suitable branches or dead laterals?


            if(measure == 'suitable'):
                tempSuitableFrame = tempTreeFrame[tempTreeFrame['indEst'] >= min]
            else:
                _tempSuitableFrame = tempTreeFrame[tempTreeFrame["Branch.angle"] <=20]
                tempSuitableFrame = _tempSuitableFrame[_tempSuitableFrame["Branch.type"] == "dead"]

            #print(f'{len(tempTreeFrame)} regular branches and {len(tempSuitableFrame)} suitable branches')



            _treeFrames.append(tempTreeFrame)
            _treeSuitFrames.append(tempSuitableFrame)

            treeDBH.append(tempTreeFrame.iloc[2]["DBH"])

        
        _frames.update({'trees' : _treeFrames})
        _suitFrames.update({'trees' : _treeSuitFrames})

        #snags
        snagEndings = ['snag1.csv','snag2.csv','snag3.csv']
        _snagFrames: List[pd.DataFrame] = []
        _snagSuitFrames: List[pd.DataFrame] = []

        for name in snagEndings:
            temp = pd.read_csv(artificialFiles + name)
            tempPoleFrame = temp[temp['type'] == 'all']
            tempSuitPoleFrame = temp[temp['type'] == 'exposed']

            _snagFrames.append(tempPoleFrame)
            _snagSuitFrames.append(tempSuitPoleFrame)

        _frames.update({'snags' : _snagFrames})
        _suitFrames.update({'snags' : _snagSuitFrames})

        #poles
        poleEndings = ['pole1.csv','pole2.csv']
        _poleFrames: List[pd.DataFrame] = []
        _poleSuitFrames: List[pd.DataFrame] = []

        for name in poleEndings:
            temp = pd.read_csv(artificialFiles + name)
            tempPoleFrame = temp[temp['type'] == 'all']
            tempSuitPoleFrame = temp[temp['type'] == 'exposed']

            _poleFrames.append(tempPoleFrame)
            _poleSuitFrames.append(tempSuitPoleFrame)

        _frames.update({'poles' : _poleFrames})
        _suitFrames.update({'poles' : _poleSuitFrames})


        #print(_frames)
        #print(_suitFrames)

        #pole


        return (_frames, _suitFrames)

    data = LoadFrames()

    frames = data[0]
    suitFrames = data[1]



    def GetCarryingCapacity(_frames, _suitFrames):
        _pts: Dict[str, List[o3d.geometry.PointCloud]] = {}
        _suitPts: Dict[str, List[o3d.geometry.PointCloud]] = {}
        _suitVoxels: Dict[str, List[o3d.geometry.PointCloud]] = {}
        _suitCoords: Dict[str, List[np.ndarray]] = {}

        count = 0


        for type in _frames.keys():

            ptsPerStructure = []
            suitPtsPerStructure = []
            voxelGridPerStructure = []
            coordsPerStructure: List[np.ndarray] = []


            
            colHeads = {'trees' : 'Branch.length', 'snags' : 'length', 'poles' : 'length'}
            for i in range(len(_frames[type])):
    

                
                #convert dataframes to arrays
                branchArray = _frames[type][i][['x', 'y', 'z']].values
                suitableArray = _suitFrames[type][i][['x', 'y', 'z']].values

                #point cloud of all branches
                branchPtCloud = o3d.geometry.PointCloud()
                branchPtCloud.points = o3d.utility.Vector3dVector(branchArray)
                """branchPtCloud.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1,
                                                                        size=(len(_frames[type][i]), 3)))"""
                
                #col = 0.7

                col = np.array([0.7,0.7,0.7])

                if type == "trees":
                    col = np.array([0.9451,0.8980,0.4510])
                
                if type == "snags":
                    col = np.array([0.7176,0.2824,0.4510])

                if type == "poles":
                    col = np.array([0.6,0.2,0.3])
                
                colSet = np.full((len(_frames[type][i]), 3), col)
                branchPtCloud.colors = o3d.utility.Vector3dVector(colSet)
          

                ptsPerStructure.append(branchPtCloud)

                #just suitable branches
                suitablePtCloud = o3d.geometry.PointCloud()
                suitablePtCloud.points = o3d.utility.Vector3dVector(suitableArray)
                suitablePtCloud.colors = o3d.utility.Vector3dVector(np.random.uniform(0, .1,
                                                                        size=(len(_suitFrames[type][i]), 3)))
                suitPtsPerStructure.append(suitablePtCloud)

                #voxelgrid / carrying capacity
                voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(suitablePtCloud,
                                                                            voxel_size=size)
                
                voxelGridPerStructure.append(voxel_grid)
                

                #array of coordinates of voxel grid
                point_cloud_np = np.asarray([voxel_grid.origin + pt.grid_index*voxel_grid.voxel_size for pt in voxel_grid.get_voxels()])
                coordsPerStructure.append(point_cloud_np)

                #add to database
                
                
                #carrying capacity stats
                da['carryUnits'].append(len(point_cloud_np))
                da['samplingSize'].append(size)
                da['type'].append(type)
                da['id'].append(f'{type}-{i}')
                da['number-id'].append(count)


                #structure level stats (tree dbh, total meters and total suit meters)
                count = count + 1

                datas = _suitFrames[type][i]
                suitmeters = datas.loc[:,colHeads[type]]
                totalSuitMeters = sum(suitmeters)

                datas = _frames[type][i]
                meters = datas.loc[:,colHeads[type]]
                totalMeters = sum(meters)
                
                da['suitLengths'].append(totalSuitMeters)
                da['totalLengths'].append(totalMeters)
                
                if type == 'trees':
                    da['treeSize'].append(treeDBH[i])
                else:
                    da['treeSize'].append('NA')

            _pts.update({type : ptsPerStructure})
            _suitPts.update({type : suitPtsPerStructure})
            _suitVoxels.update({type : voxelGridPerStructure})
            _suitCoords.update({type : coordsPerStructure})

        return (_pts, _suitPts, _suitVoxels, _suitCoords)



    data2 = GetCarryingCapacity(frames, suitFrames)


    pts = data2[0]

            

    suitPts = data2[1]
    carryingVoxels = data2[2]
    carryingCoords = data2[3]

                


    def MakeVisuals():

        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name = "hi", width = 1960, height=1080,  visible=True)


        for type in pts.keys():
            for i in range(len(pts[type])):
                
                print(f'{measure}: showing {type} {i} at resolution {size} with carrying capacity of {len(carryingCoords[type][i])}')
                pcd = pts[type][i]
                voxel_grid = carryingVoxels[type][i]
                suits = suitPts[type][i]

        
                #Visualize Point Cloud
                vis.add_geometry(pcd)
                vis.add_geometry(suits)
                vis.add_geometry(voxel_grid)


                #wireframe
                roption = vis.get_render_option()
                roption.mesh_show_wireframe = True


                #View Controll
                ctr = vis.get_view_control()
                ctr.set_front([.5,.5,0])
                ctr.set_up([0,0,1])
                #ctr.set_zoom(.75)
                
                # Updates
                """vis.update_geometry(pcd)"""
                vis.poll_events()
                vis.update_renderer()

                time.sleep(.1)
                vis.remove_geometry(pcd)
                vis.remove_geometry(voxel_grid)
                vis.remove_geometry(suits)
                

                file = f'{imageOut}size-{size}-{type}-{i}.png'

                vis.capture_screen_image(file)


    #MakeVisuals()





for i in range(2,200):
    voxSize = i/10
    print(f'setting voxel size {voxSize}')
    GetCapacities(minSuit, voxSize, carrying)

d = pd.DataFrame.from_dict(carrying)
d.to_csv(f'{out} carrying capacity measures - {measure}.csv')
