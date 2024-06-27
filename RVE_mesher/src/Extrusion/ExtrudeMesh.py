from RVE_mesher.src.Readers.GmshReader import readMesh

from RVE_mesher.src.Writers.Gmsh3dWriter import gmsh3DWriter

import numpy

def extrudeMesh(x_id, T_ei, c, nOfLevels):

    nOf2dNodes, dim =  x_id.shape

    x3d_lid = numpy.zeros((nOfLevels+1, nOf2dNodes, dim))
    x3d_lid[:,:,:] = x_id[None,:,:]
    x3d_lid[:,:,2] = numpy.linspace(0,c,nOfLevels+1)[:,None]

    nOf2dElements = T_ei.shape[0]
    T3d_lei = numpy.zeros((nOfLevels, nOf2dElements, 9), dtype='int')

    nodes0 = numpy.array([0,1,5,4], dtype='int')
    nodes1 = numpy.array([3,2,6,7], dtype='int')
    lRange = numpy.arange(nOfLevels, dtype='int')
    eRange = numpy.arange(nOf2dElements, dtype='int')

    T3d_lei[lRange[:,None,None],eRange[None,:,None],nodes0[None,None,:]] = \
        (lRange[:,None,None]+1)*nOf2dNodes + T_ei[None,:,:-1]

    T3d_lei[lRange[:,None,None],eRange[None,:,None],nodes1[None,None,:]] =\
        lRange[:,None,None]*nOf2dNodes + T_ei[None,:,:-1]

    T3d_lei[:,:,-1] = T_ei[None,:,-1]

    x3d_id = x3d_lid.reshape(((nOfLevels+1)*nOf2dNodes, dim))
    T3d_ei = T3d_lei.reshape((nOfLevels*nOf2dElements, 9))

    return x3d_id, T3d_ei