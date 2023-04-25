def writePeriodicConditions(file, pbcs_i):

    stream = open(file, 'w')

    stream.write('LMAST\n')

    nOfPbcs = pbcs_i.shape[0]
    for i in range(nOfPbcs):
        stream.write(f'{pbcs_i[i,0]+1} {pbcs_i[i,1]+1} \n')

    stream.write('END_LMAST\n')

    stream.close()