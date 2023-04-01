def writeBoundaryCondition(file, bcs_f):

    stream = open(file, 'w')

    stream.write('ON_BOUNDARIES\n')

    f = 1
    for bc in bcs_f:
        stream.write(f'{f} {bc}\n')
        f += 1

    stream.write('END_ON_BOUNDARIES\n')

    stream.close()