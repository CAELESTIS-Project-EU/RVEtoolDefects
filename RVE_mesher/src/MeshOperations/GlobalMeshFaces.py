from Globals.configPaths import *

from Readers.GmshReader import readMesh

import numpy

def globalMeshFaces(T_ei, T_fi):

    localFaces = numpy.array(
        [
            [0,1],
            [1,2],
            [2,3],
            [3,0]
        ]
        ,dtype='int'
    )

    f0_Fi = numpy.zeros((T_ei.shape[0]*4 + T_fi.shape[0],2), dtype='int')

    f0_Fi[0:T_ei.shape[0]*4,:] = T_ei[:,localFaces].reshape(T_ei.shape[0]*4,2)
    f0_Fi[T_ei.shape[0]*4:,:] = T_fi[:,0:2]

    f_Fi = numpy.sort(f0_Fi, axis=1)

    f_fi, faces_F = numpy.unique(f_Fi, axis=0, return_inverse=True)
    faces_ef = faces_F[0:T_ei.shape[0]*4].reshape(T_ei.shape[0],4)
    markedFaces_f = faces_F[T_ei.shape[0]*4:]

    e_fe = numpy.zeros((f_fi.shape[0],2), dtype='int')

    nOfElements = T_ei.shape[0]
    for e in range(nOfElements):
        e_fe[faces_ef[e,:],0] = e
        e_fe[faces_ef[nOfElements - e - 1,:],1] = nOfElements - e - 1

    e_fe = e_fe[markedFaces_f, :]

    interfaces_f = numpy.where(e_fe[:,0] != e_fe[:,1])[0]

    e_fe = e_fe[interfaces_f,:]

    return faces_ef, e_fe, markedFaces_f[interfaces_f], interfaces_f

if __name__ == '__main__':
    case = 'RVE_10_10_1'

    RVE = numpy.load(f'{dataPath}/{case}.npz')
    a = RVE['a']
    b = RVE['b']

    x_id, T_ei, T_fi = readMesh(f'{outputPath}/{case}.msh')

    faces_ef, e_fe, markedFaces_f, interfaces_f, T2_fi = globalMeshFaces(T_ei, T_fi)

    pass