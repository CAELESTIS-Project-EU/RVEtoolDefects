import numpy

def readAlyaCha(file):

    stream = open(file,'r')

    line = stream.readline()

    cha_list = []
    ended = False
    while not ended:
        line = stream.readline()

        if line == 'END_CHARACTERISTICS\n':
            ended = True
        else:
            cha_list.append(int(line.split()[1]))

    cha_array = numpy.array(cha_list)
    kfl_coh = False
    if max(cha_array) == 7:
        kfl_coh = True
        
    return kfl_coh
