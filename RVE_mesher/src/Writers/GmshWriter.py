import numpy

def writeMesh(file, x_id, T_ei, T_fi):

    stream = open(file, 'w')

    writeHeader(stream)

    writePhysicalNames(stream)

    writeNodes(stream, x_id)

    writeElements(stream, T_ei, T_fi)

    stream.close()

def writeHeader(stream):

    stream.write('$MeshFormat\n')
    stream.write('2.2 0 8\n')
    stream.write('$EndMeshFormat\n')

def writePhysicalNames(stream):

    stream.write('$PhysicalNames\n')
    stream.write('10\n')
    stream.write('3 1 "bulk"\n')
    stream.write('3 2 "fibre1"\n')
    stream.write('3 3 "fibre2"\n')
    stream.write('3 4 "cohesive"\n')
    stream.write('2 5 "faces_x0"\n')
    stream.write('2 6 "faces_x1"\n')
    stream.write('2 7 "faces_y0"\n')
    stream.write('2 8 "faces_y1"\n')
    stream.write('$EndPhysicalNames\n')

def writeNodes(stream, x_id):

    stream.write('$Nodes\n')

    nOfNodes = x_id.shape[0]
    stream.write(f'{nOfNodes}\n')
    for i in range(nOfNodes):
        stream.write(f'{i+1} {x_id[i,0]} {x_id[i,1]} {x_id[i,2]}\n')

    stream.write('$EndNodes\n')

def writeElements(stream, T_ei, T_fi):

    stream.write('$Elements\n')

    nOfEdges = T_fi.shape[0]
    nOfQuads = T_ei.shape[0]
    stream.write(f'{nOfEdges+nOfQuads}\n')

    for e in range(nOfEdges):
        stream.write(f'{e+1} 1 2 {T_fi[e, -1]+1} {T_fi[e, -1]+1} {T_fi[e, 0] + 1} {T_fi[e, 1] + 1}\n')

    for f in range(nOfQuads):
        stream.write(f'{nOfEdges+f+1} 3 2 {T_ei[f, -1]+1} {T_ei[f, -1]+1} {T_ei[f, 0] + 1} {T_ei[f, 1] + 1} {T_ei[f, 2] + 1} {T_ei[f, 3] + 1}\n')

    stream.write('$EndElements')
