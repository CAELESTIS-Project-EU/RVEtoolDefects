from Globals.configPaths import *

from Readers.GmshReader import readMesh
from Writers.GmshWriter import writeMesh

import numpy

def removeOuterElements(x_id, T_ei, T_fi, a, b):

    mask_i = markNodes(x_id, a, b)
    newNodes_j = numpy.where(mask_i)[0]
    x_jd = x_id[newNodes_j, :]

    permItoJ = numpy.zeros(x_id.shape[0], dtype='int')
    permItoJ[newNodes_j] = numpy.arange(x_jd.shape[0], dtype='int')

    jRange= numpy.arange(5, dtype='int')

    mask_f = markElements(mask_i, T_fi)
    newEdges_f = numpy.where(mask_f)[0]
    T_fj = permItoJ[T_fi[newEdges_f[:, None], jRange[None, :3]]]
    T_fj[:,-1] = T_fi[newEdges_f, -1]

    mask_e = markElements(mask_i, T_ei)
    newQuads_f = numpy.where(mask_e)[0]
    T_ej = permItoJ[T_ei[newQuads_f[:, None], jRange[None, :]]]
    T_ej[:,-1] = T_ei[newQuads_f, -1]

    return x_jd, T_ej, T_fj

def markNodes(x_id, a, b):

    eps = 1.e-8

    mask_i = numpy.ones(x_id.shape[0], dtype='bool')

    I = numpy.where(x_id[:, 0] > a + eps)[0]
    mask_i[I] = False

    I = numpy.where(x_id[:, 0] < -eps)[0]
    mask_i[I] = False

    I = numpy.where(x_id[:, 1] > b + eps)[0]
    mask_i[I] = False

    I = numpy.where(x_id[:, 1] < -eps)[0]
    mask_i[I] = False

    return mask_i

def markElements(mask_i, T_ei):

    mask_ei = mask_i[T_ei[:,:-1]]

    I_e = numpy.where(mask_ei == False)[0]

    nOfElements = T_ei.shape[0]
    mask_e = numpy.ones(nOfElements, dtype='bool')

    mask_e[I_e] = False

    return mask_e

if __name__ == '__main__':

    case = 'RVE_10_10_1'

    RVE = numpy.load(f'{dataPath}/{case}.npz')
    a = RVE['a']
    b = RVE['b']

    x_id, T_ei, T_fi = readMesh(f'{outputPath}/{case}.msh')

    x_jd, T_ej, T_fj = removeOuterElements(x_id, T_ei, T_fi, a, b)

    writeMesh(f'{outputPath}/{case}_repaired.msh', x_jd, T_ej, T_fj)