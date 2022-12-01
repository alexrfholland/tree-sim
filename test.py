

for i in range(1,17):
    tempTreeFrame = df[df['Tree.ID'] == i]
    frames.append(tempTreeFrame)

    tempSuitableFrame = tempTreeFrame[tempTreeFrame['indEst'] >= minSuit]
    
    suitableTrees.append(tempSuitableFrame)
    
    suitableBranchCloud = tempSuitableFrame[['x', 'y', 'z']].values
    branchCloud = tempTreeFrame[['x', 'y', 'z']].values


    #downpcd = suitableBranchCloud.voxel_down_sample(voxel_size=0.05)

    


    #all branches
    pcdBranches = o3d.geometry.PointCloud()
    pcdBranches.points = o3d.utility.Vector3dVector(branchCloud)
    downBranches = pcdBranches.voxel_down_sample(voxel_size=.1)

    #just suitable branches
    pcdSuit = o3d.geometry.PointCloud()
    pcdSuit.points = o3d.utility.Vector3dVector(suitableBranchCloud)


    

    voxelSize = 4


    #tester
    N = 2000
    pcd = pcdBranches
    """pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()),
              center=pcd.get_center())"""
    pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, .1,
                                                              size=(len(tempTreeFrame), 3)))
                                                              
    print('Displaying input point cloud ...')
    #o3d.visualization.draw([pcd])


    pcdSuit.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1,
                                                              size=(len(tempSuitableFrame), 3)))

    print('Displaying voxel grid ...')
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcdSuit,
                                                                voxel_size=voxelSize)


    voxel_volume = voxel_grid
    point_cloud_np = np.asarray([voxel_volume.origin + pt.grid_index*voxel_volume.voxel_size for pt in voxel_volume.get_voxels()])

    


    downSuit = pcdSuit.voxel_down_sample(voxel_size=10)


    suitablePts.append(downSuit)
    treePts.append(downBranches)

#o3d.visualization.draw_geometries([treePts[12]], mesh_show_wireframe=True)



#o3d.io.write_point_cloud(f'{snagFiles} - Tree 13 suitableVox.xyz', suitablePts[12])
o3d.io.write_point_cloud(f'{snagFiles} - Tree 13 branches.xyz', treePts[12])




"""for name in snagEndings:
    dfsnag = pd.read_csv(snagFiles + name)
    nBranches = dfsnag[dfsnag['type'] == 'exposed'][['x', 'y', 'z']].values
    pcd: o3d.geometry.PointCloud = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(nBranches)
    downpcd = pcd.voxel_down_sample(voxel_size= 10)
    print('!!!!!!!!!!!!!!!!')
    print(f'type is {type(downpcd)}')"""

"""    voxels = downpcd.get_voxels()

    coordList = []

    for vox in voxels:
        index = vox.grid_index
        center = downpcd.get_voxel_center_coordinate(index)
        coordList.append(center)
    print(coordList)"""





    #o3d.io.write_point_cloud(f'{snagFiles} + {name} + test5.xyz', downpcd)

    #o3d.visualization.draw_geometries([downpcd], mesh_show_wireframe=True)

    #o3d.io.write_voxel_grid(f'{snagFiles} + {name} + test.xyz', downpcd, True, False, True)


    






#print(suitableTrees)

def edges_to_lineset(mesh, edges, color):
    ls = o3d.geometry.LineSet()
    ls.points = mesh.vertices
    ls.lines = edges
    ls.paint_uniform_color(color)
    return ls