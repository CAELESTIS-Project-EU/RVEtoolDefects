from Globals.configPaths import outputPath

import numpy

def readBoundaryCondition(file):

    stream = open(file,'r')

    line = stream.readline()

    if line != 'ON_BOUNDARIES\n':
        print('Wrong format for fix.bou')

    bcs_list = []
    ended = False
    while not ended:
        line = stream.readline()

        if line == 'END_ON_BOUNDARIES\n':
            ended = True
        else:
            bcs_list.append(int(line.split()[1]))


    bcs = numpy.array(bcs_list)

    map = numpy.array([0,1,2,3,4,1,2,3,4,5,6], dtype = 'int')

    bcs = map[bcs]

    return bcs




if __name__ == '__main__':

    case = 'oneFibre'

    readBoundaryCondition(f'{outputPath}/{case}_3d.fix.bou')