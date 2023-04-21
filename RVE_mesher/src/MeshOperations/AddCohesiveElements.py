from MeshOperations import DetectMaterials, GlobalMeshFaces

from Readers.GmshReader import readMesh

import numpy

def addCohesiveElements(x_id, T_ei, T_fi, faces_ef, e_fe, markedFaces_f, interfaces_f):

    x_jd, mapIJ_i = createNewNodesAndMapping(x_id, T_fi, interfaces_f)

    T_qj, type_q = createCohesiveElements(T_ei, faces_ef, e_fe, markedFaces_f, mapIJ_i)

    return x_jd, T_qj, type_q

def createNewNodesAndMapping(x_id, T_fi, interfaces_f):

    nOfEdgeNodes = 2
    interfaceNodes_fi = T_fi[interfaces_f,:nOfEdgeNodes]
    interfaceNodes_i = numpy.unique(interfaceNodes_fi.ravel())

    nOfNewNodes = interfaceNodes_i.shape[0]
    x_jd = numpy.zeros((x_id.shape[0] + nOfNewNodes, 3))
    x_jd[0:x_id.shape[0], :] = x_id

    nOfNodes = x_id.shape[0]

    mapIJ_i = numpy.arange(nOfNodes+nOfNewNodes, dtype='int')
    mapIJ_i[interfaceNodes_i] = numpy.arange(nOfNodes, nOfNodes+nOfNewNodes, dtype='int')

    x_jd[mapIJ_i[interfaceNodes_i],:] = x_id[interfaceNodes_i,:]

    return x_jd, mapIJ_i

def createCohesiveElements(T_ei, faces_ef, e_fe, interfaces_f, mapIJ_i):

    nOfInterfaces = interfaces_f.shape[0]

    localFaces_fi=numpy.array(
        [[0, 1],
         [1, 2],
         [2, 3],
         [3, 0]
         ],
        dtype='int'
    )

    nOfElements = T_ei.shape[0]

    T_qj = numpy.zeros((nOfElements + nOfInterfaces, 5), dtype='int')

    T_qj[0:nOfElements, :] = T_ei

    cohesiveMaterial = 3
    T_qj[nOfElements:,-1] = cohesiveMaterial

    for f in range(nOfInterfaces):
        face = interfaces_f[f]

        adjacentElements_e = e_fe[f, :]
        material_e = T_ei[adjacentElements_e,-1]
        perm_e = numpy.argsort(material_e)
        adjacentElements_e = adjacentElements_e[perm_e]
        # We now have first the bulk element (material 0) and then the fibre element(material != 0)

        localFaces_ef = faces_ef[adjacentElements_e,:]
        localFaces_e = numpy.where(localFaces_ef == face)[1]

        adjacentElements_ei = T_ei[adjacentElements_e, :]
        localFaces_ei = numpy.zeros((2,2), dtype='int')
        localFaces_ei[0,:] = adjacentElements_ei[0, localFaces_fi[localFaces_e[0],:]]
        localFaces_ei[1,:] = adjacentElements_ei[1, localFaces_fi[localFaces_e[1],:]]

        T_qj[nOfElements+f,0:2] = localFaces_ei[1,:]
        T_qj[nOfElements+f,2:4] = mapIJ_i[localFaces_ei[0,:]]

    fibres_e = numpy.where((T_qj[:,-1] != 0) & (T_qj[:,-1] != cohesiveMaterial))[0]
    T_qj[fibres_e,:] = mapIJ_i[T_qj[fibres_e,:]]

    type_q = numpy.zeros(T_qj.shape[0], dtype='int')
    type_q[T_ei.shape[0]:] = 7

    return T_qj, type_q