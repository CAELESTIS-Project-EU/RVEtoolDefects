import numpy

def set2DBoundaries(b1_f, b2_f, b3_f, b4_f, T_fi):
    nOfFaces = b1_f.shape[0] + b2_f.shape[0] + b3_f.shape[0] + b4_f.shape[0]
    Tb_fi = numpy.zeros((nOfFaces,3), dtype='int')

    offset = 0
    nOfFaces1 = b1_f.shape[0]
    nOfFaces2 = b2_f.shape[0]
    nOfFaces3 = b3_f.shape[0]
    nOfFaces4 = b4_f.shape[0]

    Tb_fi[offset:offset + nOfFaces1, :2] = T_fi[b1_f,:]
    Tb_fi[offset:offset + nOfFaces1, 2] = 6

    offset += nOfFaces1
    Tb_fi[offset:offset + nOfFaces2, :2] = T_fi[b2_f, :]
    Tb_fi[offset:offset + nOfFaces2, 2] = 5

    offset += nOfFaces2
    Tb_fi[offset:offset + nOfFaces3, :2] = T_fi[b3_f, :]
    Tb_fi[offset:offset + nOfFaces3, 2] = 7

    offset += nOfFaces3
    Tb_fi[offset:offset + nOfFaces4, :2] = T_fi[b4_f, :]
    Tb_fi[offset:offset + nOfFaces4, 2] = 4

    return Tb_fi