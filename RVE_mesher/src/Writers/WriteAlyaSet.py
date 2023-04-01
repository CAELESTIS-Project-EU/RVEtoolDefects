def writeAlyaSet(file, nOfElements):

    stream = open(file, 'w')

    stream.write('ELEMENTS\n')

    for e in range(1,nOfElements+1):
        
        stream.write(f'{e} 1 \n')
        
    stream.write('END_ELEMENTS\n')

    stream.close()
