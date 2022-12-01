import numpy as np
import pandas as pd
import open3d as o3d

from typing import List
from typing import Dict

import time


treeFiles = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/Input Data/fullBranchData.csv'

snagFiles = '/Users/alexholland/OneDrive - The University of Melbourne/_PhD Private/Source FIles/Dissemination/Sustainability/Stats/Input Data/snags/'



minSuit = 1.536 

frames: Dict[str, List[pd.DataFrame]] = {}
suitFrames: Dict[str, List[pd.DataFrame]] = {}
pts: Dict[str, List[o3d.geometry.PointCloud]] = {}
suitPts: Dict[str, List[o3d.geometry.PointCloud]] = {}
carryingVoxels: Dict[str, List[o3d.geometry.VoxelGrid]] = {}
carryingCoords: Dict[str, List[np.ndarray]] = {}


def LoadFrames():
    
    _frames: Dict[str, List[pd.DataFrame]] = {}
    _suitFrames: Dict[str, List[pd.DataFrame]] = {}

    #trees
    _treeFrames: List[pd.DataFrame] = []
    _treeSuitFrames: List[pd.DataFrame] = []

    for i in range(1,17):
        df = pd.read_csv(treeFiles)
        tempTreeFrame = df[df['Tree.ID'] == i]
        tempSuitableFrame = tempTreeFrame[tempTreeFrame['indEst'] >= minSuit]

        _treeFrames.append(tempTreeFrame)
        _treeSuitFrames.append(tempSuitableFrame)
    
    _frames.update({'trees' : _treeFrames})
    _suitFrames.update({'trees' : _treeSuitFrames})

    #snags
    snagEndings = ['snag1.csv','snag2.csv','snag3.csv']
    _snagFrames: List[pd.DataFrame] = []
    _snagSuitFrames: List[pd.DataFrame] = []

    for name in snagEndings:
        temp = pd.read_csv(snagFiles + name)
        tempSnagFrame = temp[temp['type'] == 'all']
        tempSuitSnagFrame = temp[temp['type'] == 'exposed']

        _snagFrames.append(tempSnagFrame)
        _snagSuitFrames.append(tempSuitSnagFrame)

    _frames.update({'snags' : _snagFrames})
    _suitFrames.update({'snags' : _snagSuitFrames})

    #print(_frames)
    #print(_suitFrames)

    #pole


    return (_frames, _suitFrames)

data = LoadFrames()

frames = data[0]
suitFrames = data[1]

print(f'frames output is {frames.keys()}')


def GetCarryingCapacity(_frames, _suitFrames):
    _pts: Dict[str, List[o3d.geometry.PointCloud]] = {}
    _suitPts: Dict[str, List[o3d.geometry.PointCloud]] = {}
    _suitVoxels: Dict[str, List[o3d.geometry.PointCloud]] = {}
    _suitCoords: Dict[str, List[np.ndarray]] = {}

    print(_frames['snags'])

    for test in _frames.keys():
        print(test)
    

    for type in _frames.keys():

        print(type)


        ptsPerStructure = []
        suitPtsPerStructure = []
        voxelGridPerStructure = []
        coordsPerStructure: List[np.ndarray] = []


        for i in range(len(_frames[type])):
            
            #convert dataframes to arrays
            branchArray = _frames[type][i][['x', 'y', 'z']].values
            suitableArray = _suitFrames[type][i][['x', 'y', 'z']].values

            #point cloud of all branches
            branchPtCloud = o3d.geometry.PointCloud()
            branchPtCloud.points = o3d.utility.Vector3dVector(branchArray)

            """branchPtCloud.colors = o3d.utility.Vector3dVector(np.random.uniform(0, .1,
                                                                    size=(len(_frames[i]), 3)))"""

            ptsPerStructure.append(branchPtCloud)

            #just suitable branches
            suitablePtCloud = o3d.geometry.PointCloud()
            suitablePtCloud.points = o3d.utility.Vector3dVector(suitableArray)
            suitablePtCloud.colors = o3d.utility.Vector3dVector(np.random.uniform(0, .1,
                                                                    size=(len(_suitFrames[type][i]), 3)))
            suitPtsPerStructure.append(suitablePtCloud)

            #voxelgrid / carrying capacity
            voxelSize = 4
            voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(suitablePtCloud,
                                                                        voxel_size=voxelSize)
            
            voxelGridPerStructure.append(voxel_grid)
            

            #array of coordinates of voxel grid
            point_cloud_np = np.asarray([voxel_grid.origin + pt.grid_index*voxel_grid.voxel_size for pt in voxel_grid.get_voxels()])
            coordsPerStructure.append(point_cloud_np)
        
        _pts.update({type : ptsPerStructure})
        _suitPts.update({type : suitPtsPerStructure})
        _suitVoxels.update({type : voxelGridPerStructure})
        _suitCoords.update({type : coordsPerStructure})

        


    return (_pts, _suitPts, _suitVoxels, _suitCoords)



data2 = GetCarryingCapacity(frames, suitFrames)


pts = data2[0]

        
print(f'output points are {pts.keys()}')

suitPts = data2[1]
carryingVoxels = data2[2]
carryingCoords = data2[3]
print("success")

            


def MakeVisuals():

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name = "hi", width = 1960, height=1080,  visible=True)

    print (pts.keys())

    for type in pts.keys():
        for i in range(len(pts[type])):
            
            print(f'showing {type} {i} with carrying capacity of {len(carryingCoords[type][i])}')
            pcd = pts[type][i]
            voxel_grid = carryingVoxels[type][i]
    
            #Visualize Point Cloud
            vis.add_geometry(pcd)
            vis.add_geometry(voxel_grid)


            #wireframe
            roption = vis.get_render_option()
            roption.mesh_show_wireframe = True


            #View Controll
            ctr = vis.get_view_control()
            ctr.set_front([0,.5,0])
            ctr.set_up([0,0,1])
            ctr.set_zoom(.75)
            
            # Updates
            """vis.update_geometry(pcd)"""
            vis.poll_events()
            vis.update_renderer()

            time.sleep(1)
            vis.remove_geometry(pcd)
            vis.remove_geometry(voxel_grid)
            #vis.remove_geometry(octree)

MakeVisuals()
