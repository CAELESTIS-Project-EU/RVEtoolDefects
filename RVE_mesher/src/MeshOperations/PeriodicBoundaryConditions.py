import numpy

def periodicBoundaryConditions(x_id, a, b, tol = 1.e-8):

    e42_i = leftRightBoundaryCondition(x_id, a, b, tol)
    e31_i = frontBackBoundaryCondition(x_id, b, tol)

    v41_i = numpy.array([[e42_i[0,0], e42_i[0,1]]], dtype = 'int32')
    v42_i = numpy.array([[e42_i[0,0], e42_i[-1,1]]], dtype = 'int32')
    v43_i = numpy.array([[e42_i[0,0], e42_i[-1,0]]], dtype = 'int32')

    f1_i = numpy.where(
        (x_id[:,0] > tol) &
        (x_id[:,0] - a < -tol) &
        (x_id[:,1] > tol) &
        (x_id[:,1] - b < -tol)
    )[0]

    x_id[e42_i[:,0],0] = 0.0
    x_id[e42_i[:,1],0] = a
    x_id[e42_i[:,1],1] = x_id[e42_i[:, 0], 1]

    x_id[e31_i[:,0],1] = 0.0
    x_id[e31_i[:,1],1] = b
    x_id[e31_i[:, 1], 0] = x_id[e31_i[:,0],0]

    return f1_i, e42_i[1:-1,:], e31_i[1:-1,:], v41_i, v42_i, v43_i

def leftRightBoundaryCondition(x_id, a, b, tol):

    leftNodes_i = numpy.where(numpy.abs(x_id[:,0]) < tol)[0]
    rightNodes_i = numpy.where(numpy.abs(x_id[:,0] - a) < tol)[0]

    left_id = x_id[leftNodes_i, :]
    right_id = x_id[rightNodes_i, :]

    leftPerm_i = numpy.argsort(left_id[:,1])
    rightPerm_i = numpy.argsort(right_id[:,1])

    nOfLeftNodes = leftNodes_i.size
    nOfRightNodes = rightNodes_i.size

    if nOfLeftNodes != nOfRightNodes:
        print(f'Error!! nOfLeftNodes: {nOfLeftNodes} != nOfRightNodes: {nOfRightNodes}')

    leftRightBoundaryCondition = numpy.empty((nOfLeftNodes, 2), dtype='int')
    leftRightBoundaryCondition[:,0] = leftNodes_i[leftPerm_i]
    leftRightBoundaryCondition[:,1] = rightNodes_i[rightPerm_i]

    leftNodes_id = x_id[leftRightBoundaryCondition[:,0], :]
    cohesiveNodes_i = numpy.where(leftNodes_id[1:,1] == leftNodes_id[0:-1,1])[0]

    for cohesiveNode in cohesiveNodes_i:
        if leftRightBoundaryCondition[cohesiveNode,0] > leftRightBoundaryCondition[cohesiveNode+1,0]:
            temp = leftRightBoundaryCondition[cohesiveNode+1,0]
            leftRightBoundaryCondition[cohesiveNode+1,0] = leftRightBoundaryCondition[cohesiveNode, 0]
            leftRightBoundaryCondition[cohesiveNode, 0] = temp

        if leftRightBoundaryCondition[cohesiveNode, 1] > leftRightBoundaryCondition[cohesiveNode + 1, 1]:
            temp = leftRightBoundaryCondition[cohesiveNode+1,1]
            leftRightBoundaryCondition[cohesiveNode+1,1] = leftRightBoundaryCondition[cohesiveNode,1]
            leftRightBoundaryCondition[cohesiveNode,1] = temp

    return leftRightBoundaryCondition

def frontBackBoundaryCondition(x_id, b, tol):

    frontNodes_i = numpy.where(numpy.abs(x_id[:,1]) < tol)[0]
    backNodes_i = numpy.where(numpy.abs(x_id[:,1] - b) < tol)[0]

    front_id = x_id[frontNodes_i, :]
    back_id = x_id[backNodes_i, :]

    frontPerm_i = numpy.argsort(front_id[:,0])
    backPerm_i = numpy.argsort(back_id[:,0])

    nOfFrontNodes = frontNodes_i.size
    nOfBackNodes = backNodes_i.size

    if nOfFrontNodes != nOfBackNodes:
        print(f'Error!! nOfFrontNodes: {nOfFrontNodes} != nOfBackNodes: {nOfBackNodes}')

    frontBackBoundaryCondition = numpy.empty((nOfFrontNodes, 2), dtype='int')
    frontBackBoundaryCondition[:,0] = frontNodes_i[frontPerm_i]
    frontBackBoundaryCondition[:,1] = backNodes_i[backPerm_i]

    frontNodes_id = x_id[frontBackBoundaryCondition[:,0], :]
    cohesiveNodes_i = numpy.where(frontNodes_id[1:,0] == frontNodes_id[0:-1,0])[0]

    for cohesiveNode in cohesiveNodes_i:
        if frontBackBoundaryCondition[cohesiveNode, 0] > frontBackBoundaryCondition[cohesiveNode + 1, 0]:
            temp = frontBackBoundaryCondition[cohesiveNode + 1, 0]
            frontBackBoundaryCondition[cohesiveNode + 1, 0] = frontBackBoundaryCondition[cohesiveNode, 0]
            frontBackBoundaryCondition[cohesiveNode, 0] = temp

        if frontBackBoundaryCondition[cohesiveNode, 1] > frontBackBoundaryCondition[cohesiveNode + 1, 1]:
            temp = frontBackBoundaryCondition[cohesiveNode + 1, 1]
            frontBackBoundaryCondition[cohesiveNode + 1, 1] = frontBackBoundaryCondition[cohesiveNode, 1]
            frontBackBoundaryCondition[cohesiveNode, 1] = temp

    return frontBackBoundaryCondition
