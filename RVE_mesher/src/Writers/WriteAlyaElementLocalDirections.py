def writeElementLocalDirections(file, nOfElements):

    stream = open(file, 'w')

    stream.write('FIELD = 1\n')

    for e in range(1,nOfElements+1):

        stream.write(f'{e} 0.0 0.0 1.0  1.0 0.0 0.0  0.0 1.0 0.0 \n')

    stream.write('END_FIELD')

    stream.close()

