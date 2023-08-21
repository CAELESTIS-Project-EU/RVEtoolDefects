import numpy


def readAlyaGeo(alyaGeoFile):
    """
    Load coordinates
    """
    f = open(alyaGeoFile,'r')
    nList = []
    line = True
    inCOOR = False
    while line:
        line = f.readline()
        if line == '':
            line = False
        else:
            if 'COORDINATES' in line:
                if 'END_COORDINATES' in line:
                    
                    inCOOR = False
                    line = True
                else:
                    inCOOR = True
                    line = True
            else:
                if inCOOR:
                    stripline = line.strip().split()
                    nodeLine = []
                    for i in range(len(stripline)):
                        if i == 0:
                            ivalue = int(stripline[i])
                        else:
                            ivalue = float(stripline[i])
                        nodeLine.append(ivalue)
                    nList.append(nodeLine)
                    line = True
                else:
                    line = True
    f.close()

    dim = len(nList[0])-1
    x = numpy.array([i[1] for i in nList])
    y = numpy.array([i[2] for i in nList])

    if dim == 2:
        [xmax,ymax]=[x.max(),y.max()]
        [xmin,ymin]=[x.min(),y.min()]
        lx = xmax-xmin
        ly = ymax-ymin
        lz = 0.
    else:
        z = numpy.array([i[3] for i in nList])
        [xmax,ymax,zmax]=[x.max(),y.max(),z.max()]
        [xmin,ymin,zmin]=[x.min(),y.min(),z.min()]
        lx = xmax-xmin
        ly = ymax-ymin
        lz = zmax-zmin
        
    return dim, lx, ly, lz
