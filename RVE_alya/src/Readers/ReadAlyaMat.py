import numpy

def readAlyaMat(file):

    stream = open(file,'r')

    line = stream.readline()

    mat_list = []
    ended = False
    while not ended:
        line = stream.readline()

        if line == 'END_MATERIALS\n':
            ended = True
        else:
            mat_list.append(int(line.split()[1]))

    mat_array = numpy.array(mat_list)
    
    return max(mat_array)
