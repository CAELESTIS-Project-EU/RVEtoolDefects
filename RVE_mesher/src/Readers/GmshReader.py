# from numba import jit

import numpy

def readMesh(file):

    stream = open(file, 'r')

    finishedReading = False
    while not finishedReading:

        sectionName = stream.readline().strip()
        # print(sectionName)

        if sectionName == '$MeshFormat':
            readMeshFormat(stream)
        elif sectionName == '$Nodes':
            x_id = readNodes(stream)
        elif sectionName == '$Elements':
            T_fi, T_ei = readElements(stream)
        else:
            break

    return x_id, T_ei, T_fi

def readMeshFormat(stream):
    meshFormat = stream.readline().strip()
    # print(meshFormat)
    stream.readline().strip()

def readNodes(stream):
    nOfNodes = int(stream.readline().strip())
    # print(nOfNodes)

    nodes = numpy.fromfile(stream,float,nOfNodes*4,sep=' ').reshape(nOfNodes, 4)[:,1:].copy()

    stream.readline().strip()

    return nodes

def readElements(stream):
    nOfElements = int(stream.readline().strip())

    # print(nOfElements)

    edgesList = []
    quadsList = []

    for iElement in range(nOfElements):
        element = stream.readline().strip().split()
        type = int(element[1])

        if type == 1:
            edge = [int(i) for i in element[-3:]]
            edgesList.append(edge)
        elif type == 3:
            quad = [int(i) for i in element[-5:]]
            quadsList.append(quad)

    nOfEdges = len(edgesList)
    T_fi = numpy.zeros((nOfEdges, 3), dtype='int')
    for iEdge in range(nOfEdges):
        T_fi[iEdge,:2] = edgesList[iEdge][1:]
        T_fi[iEdge,:2] -= 1
        T_fi[iEdge,-1] = edgesList[iEdge][0]

    nOfQuads = len(quadsList)
    T_ei = numpy.zeros((nOfQuads, 5), dtype='int')
    for iQuad in range(nOfQuads):
        T_ei[iQuad,:4] = quadsList[iQuad][1:]
        T_ei[iQuad,:4] -= 1
        T_ei[iQuad,-1] = quadsList[iQuad][0]

    stream.readline()

    return T_fi, T_ei

if __name__ == '__main__':

    from Globals.configPaths import outputPath

    case = 'RVE_10_10_1'

    readMesh(f'{outputPath}/{case}.msh')