from Readers.GmshReader import readMesh

import numpy

def obtainBoundaryFaces(T_ei):

    localFaces = numpy.array(
        [
            [0,1],
            [1,2],
            [2,3],
            [3,0]
        ],
        dtype='int'
    )

    nOfElements = T_ei.shape[0]

    T_efi = T_ei[:,localFaces]
    T_Fi = T_efi.reshape(nOfElements*4,2)

    T1_Fi = numpy.sort(T_Fi, axis=1)

    T_fi, F_f, f_F = numpy.unique(T1_Fi, axis=0, return_index=True, return_inverse=True)

    f_ef = f_F.reshape(nOfElements,4)

    e_fe = numpy.zeros((T_fi.shape[0], 2), dtype='int')

    nOfElements = T_ei.shape[0]
    for e in range(nOfElements):
        e_fe[f_ef[e, :], 0] = e
        e_fe[f_ef[nOfElements - e - 1, :], 1] = nOfElements - e - 1

    boundary_f = numpy.where(e_fe[:,0] == e_fe[:,1])[0]
    boundary_F = F_f[boundary_f]

    T_fi = T_Fi[boundary_F]

    return T_fi