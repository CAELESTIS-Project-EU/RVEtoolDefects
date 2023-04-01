from Globals.configPaths import *

from Readers.GmshReader import readMesh

from MeshOperations import PeriodicBoundaryConditions
from Extrusion.ExtrudeMesh import extrudeMesh

import numpy

def extrudeBoundaryConditions(f1_i, e42_i, e31_i, v41_i, v42_i, v43_i, nOfNodes, nOfLevels):

    v3d41_i = v41_i
    v3d42_i = v42_i
    v3d43_i = v43_i
    v44_i = v41_i.copy()
    v44_i[0,1] = v44_i[0,0]
    v3d45_i = oppositeVertexCondition(v41_i, nOfNodes, nOfLevels)
    v3d46_i = oppositeVertexCondition(v42_i, nOfNodes, nOfLevels)
    v3d47_i = oppositeVertexCondition(v43_i, nOfNodes, nOfLevels)
    v3d48_i = oppositeVertexCondition(v44_i, nOfNodes, nOfLevels)

    e3d85_i = extrudeVertexCondition(v41_i, nOfNodes, nOfLevels)
    e3d86_i = extrudeVertexCondition(v42_i, nOfNodes, nOfLevels)
    e3d87_i = extrudeVertexCondition(v43_i, nOfNodes, nOfLevels)
    e3d410_i = oppositeEdgeCondition(e42_i, nOfNodes, nOfLevels)
    e44_i = e42_i.copy()
    e44_i[:,1] = e44_i[:,0]
    e3d412_i = oppositeEdgeCondition(e44_i, nOfNodes, nOfLevels)
    e3d42_i = e42_i.copy()
    e3d39_i = oppositeEdgeCondition(e31_i, nOfNodes, nOfLevels)
    e33_i = e31_i.copy()
    e33_i[:,1] = e33_i[:,0]
    e3d311_i = oppositeEdgeCondition(e33_i, nOfNodes, nOfLevels)
    e3d31_i = e31_i.copy()

    f3d42_i = extrudeEdgeCondition(e42_i, nOfNodes, nOfLevels)
    f3d31_i = extrudeEdgeCondition(e31_i, nOfNodes, nOfLevels)
    f3d56_i = oppositeFaceCondition(f1_i, nOfNodes, nOfLevels)

    unsortedPbc_i = numpy.concatenate(
        [
            v3d41_i,  ## vertices condition
            v3d42_i,
            v3d43_i,
            v3d45_i,
            v3d46_i,
            v3d47_i,
            v3d48_i,
            e3d42_i,   ## edges conditions
            e3d410_i,
            e3d412_i,
            e3d31_i,
            e3d39_i,
            e3d311_i,
            e3d85_i,
            e3d86_i,
            e3d87_i,
            f3d31_i,
            f3d42_i,
            f3d56_i
        ]
    )

    permutation = numpy.argsort(unsortedPbc_i[:,1])

    pbc_i = numpy.zeros(unsortedPbc_i.shape, dtype='int')
    pbc_i[:,0] = unsortedPbc_i[permutation,1]
    pbc_i[:,1] = unsortedPbc_i[permutation,0]

    return pbc_i

def extrudeVertexCondition(v_i, nOfNodes, nOfLevels):

    lRange = numpy.arange(1,nOfLevels, dtype='int')

    e_i = nOfNodes*lRange[:,None, None] + v_i[None,:,:]
    e_i = e_i.reshape((nOfLevels-1), 2)

    return e_i

def extrudeEdgeCondition(e_i, nOfNodes, nOfLevels):

    lRange = numpy.arange(1, nOfLevels, dtype='int')

    f_i = nOfNodes*lRange[:,None,None] + e_i[None,:,:]
    f_i = f_i.reshape(e_i.shape[0]*(nOfLevels-1), 2)

    return f_i

def oppositeVertexCondition(v_i, nOfNodes, nOfLevels):
    offset = nOfNodes * (nOfLevels)

    v3d_i = numpy.copy(v_i)
    v3d_i[0,1] += offset

    return v3d_i

def oppositeEdgeCondition(e_i, nOfNodes, nOfLevels):
    offset = nOfNodes * (nOfLevels)

    e3d_i = numpy.copy(e_i)
    e3d_i[:, 1] += offset

    return e3d_i

def oppositeFaceCondition(f_i, nOfNodes, nOfLevels):

    offset = nOfNodes * (nOfLevels)

    f3D_i = numpy.zeros((f_i.shape[0], 2), dtype='int')
    f3D_i[:,0] = f_i
    f3D_i[:,1] = f_i + offset

    return f3D_i

if __name__ == '__main__':

    case = 'RVE_10_10_1'
    # case = 'oneFibre'

    RVE = numpy.load(f'{dataPath}/{case}.npz')
    a = RVE['a']
    b = RVE['b']

    x_id, T_ei, T_fi = readMesh(f'{outputPath}/{case}.msh')

    nOfNodes = x_id.shape[0]
    nOfLevels = 2

    x3d_id, T3d_ei = extrudeMesh(x_id, T_ei, 1.0, nOfLevels)

    f1_i, e42_i, e31_i, v41_i, v42_i, v43_i = \
        PeriodicBoundaryConditions.periodicBoundaryConditions(x_id, a, b)

    extrudeBoundaryConditions(f1_i, e42_i, e31_i, v41_i, v42_i, v43_i, nOfNodes, nOfLevels)
