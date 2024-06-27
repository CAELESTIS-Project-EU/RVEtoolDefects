from RVE_mesher.src.MeshOperations import DetectInterfaces

from RVE_mesher.src.Readers.GmshReader import readMesh
from RVE_mesher.src.Writers.GmshWriter import writeMesh

import numpy

def extrudeBoundaries(T_ei, b1_f, b2_f, b3_f, b4_f, T_fi, nOfLevels, nOfNodes2d):

    nOfEdges1 = b1_f.shape[0]*nOfLevels
    nOfEdges2 = b2_f.shape[0]*nOfLevels
    nOfEdges3 = b3_f.shape[0]*nOfLevels
    nOfEdges4 = b4_f.shape[0]*nOfLevels

    nOfFaces0 = T_ei.shape[0]

    offset0 = 0
    offset1 = nOfEdges1
    offset2 = offset1 + nOfEdges2
    offset3 = offset2 + nOfEdges3
    offset4 = offset3 + nOfEdges4
    offset5 = offset4 + nOfFaces0
    offset6 = offset5 + nOfFaces0


    nOfEdges = nOfEdges1 + nOfEdges2 + nOfEdges3 + nOfEdges4 + 2*nOfFaces0

    T3d_fi = numpy.zeros((nOfEdges,5), dtype='int')

    T3d_fi[offset0:offset1,:] = extrudeBoundary(b1_f, T_fi, nOfLevels, nOfNodes2d, 6)
    T3d_fi[offset1:offset2,:] = extrudeBoundary(b2_f, T_fi, nOfLevels, nOfNodes2d, 5)
    T3d_fi[offset2:offset3,:] = extrudeBoundary(b3_f, T_fi, nOfLevels, nOfNodes2d, 7)
    T3d_fi[offset3:offset4,:] = extrudeBoundary(b4_f, T_fi, nOfLevels, nOfNodes2d, 4)

    T3d_fi[offset4:offset5, :-1] = T_ei[:, -2::-1]
    T3d_fi[offset4:offset5,-1] = 8

    T3d_fi[offset5:offset6,:-1] = T_ei[:,:-1] + (nOfLevels)*nOfNodes2d
    T3d_fi[offset5:offset6,-1] = 9

    return T3d_fi

    pass

def extrudeBoundary(b_f, T_fi, nOfLevels, nOfNodes2d, tag):

    nOfEdges = b_f.shape[0]

    b3d_fi = numpy.zeros((nOfLevels, nOfEdges, 5), dtype='int')
    b3d_fi[:,:,-1] = tag

    nodes0 = numpy.array([0, 1], dtype='int')
    nodes1 = numpy.array([3, 2], dtype='int')

    lRange = numpy.arange(nOfLevels, dtype='int')
    eRange = numpy.arange(nOfEdges, dtype='int')

    b_fi = T_fi[b_f,:2]

    b3d_fi[lRange[:,None,None],eRange[None,:,None], nodes0[None,None,:]] = \
        lRange[:,None,None]*nOfNodes2d + b_fi[None,:,:]

    b3d_fi[lRange[:,None,None],eRange[None,:,None], nodes1[None,None,:]] = \
        (lRange[:,None,None]+1)*nOfNodes2d + b_fi[None,:,:]

    return b3d_fi.reshape(((nOfLevels)*nOfEdges,5))


