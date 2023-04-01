from Globals.configPaths import *

from Readers.GmshReader import readMesh
from Writers.GmshWriter import writeMesh

import numpy

def detectMaterials(fibres, x_id, T_ei):

    # minMaterialId = T_ei[:,-1].min()
    # maxMaterialId = T_ei[:,-1].max()
    #
    # # print(minMaterialId, maxMaterialId)
    #
    # materialMap = numpy.zeros(maxMaterialId+1, dtype='int')

    nOfElements = T_ei.shape[0]

    nOfFibres = fibres.shape[0]

    for e in range(nOfElements):

        material = 0

        c_d = (x_id[T_ei[e, :-1], :]).sum(0) / 4.0

        for fibre in range(nOfFibres):
            x = fibres[fibre, 1]
            y = fibres[fibre, 2]
            r = fibres[fibre, -1]

            signedD = (x - c_d[0])**2 + (y - c_d[1])**2 - r*r

            if signedD < 0.0:
                material = fibres[fibre, 4]+1
                break

        T_ei[e,-1] = material


    # minMaterialId = T_ei[:, -1].min()
    # maxMaterialId = T_ei[:, -1].max()
    #
    # print(minMaterialId, maxMaterialId)
    #
    # print(materialMap)

    return T_ei



if __name__ == '__main__':
    case = 'RVE_10_10_1'

    RVE = numpy.load(f'{dataPath}/{case}.npz')
    fibres = RVE['Fibre_pos']

    x_id, T_ei, T_fi = readMesh(f'{outputPath}/{case}_repaired.msh')

    T_fi = detectMaterials(fibres, x_id, T_fi)

    writeMesh(f'{outputPath}/{case}_materials.msh', x_id, T_ei, T_fi)