from RVE_mesher.src.Readers.GmshReader import readMesh
from RVE_mesher.src.Writers.GmshWriter import writeMesh

import numpy

def detectInterfaces(x_id, T_fi, a, b):

    b1_f = detectBoundary(x_id, T_fi, 0.0, 1)
    b2_f = detectBoundary(x_id, T_fi, a, 0)
    b3_f = detectBoundary(x_id, T_fi, b, 1)
    b4_f = detectBoundary(x_id, T_fi, 0.0, 0)

    marks_f = numpy.ones(T_fi.shape[0], dtype='bool')
    marks_f[b1_f] = False
    marks_f[b2_f] = False
    marks_f[b3_f] = False
    marks_f[b4_f] = False

    interfaces_f = numpy.where(marks_f)[0]

    return b1_f, b2_f, b3_f, b4_f

def detectBoundary(x_id, T_fi, l, d):

    tol = 1.e-8

    boundaryNodes_i = numpy.where(numpy.abs(x_id[:,d] - l) < tol)[0]

    marks_i = numpy.zeros(x_id.shape[0], dtype='bool')
    marks_i[boundaryNodes_i] = True

    marks_fi = marks_i[T_fi]

    b_f = numpy.where(marks_fi[:,0] & marks_fi[:,1])[0]

    return b_f