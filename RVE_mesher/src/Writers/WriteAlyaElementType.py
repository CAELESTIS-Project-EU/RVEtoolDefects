def writeElementType(file, type_e, nOfLevels):

    stream = open(file, 'w')

    stream.write('CHARACTERISTICS, ELEMENTS\n')

    iHex = 1
    for iLevel in range(nOfLevels):
        for type in type_e:
            stream.write(f'{iHex} {type}\n')
            iHex += 1

    stream.write('END_CHARACTERISTICS\n')

    stream.close()