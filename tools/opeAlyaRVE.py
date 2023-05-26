
import numpy

"""
General furnctions for operate a RVE mesh in Alya
"""

def loadAlyaGeoDat(source):
    """
    Load coordinates and element connectivity files 
    Skip first and last rows
    """
    na = numpy.loadtxt(open(f'{source}'+'.nod.dat').readlines()[:-1], skiprows=1, dtype=None)
    ne = []
    with open(f'{source}'+'.ele.dat','r') as fcon:
        for line in fcon:
            if line.split()[0] == 'ELEMENTS':
                continue
            elif line.split()[0] == 'END_ELEMENTS':
                continue
            else:
                iline = numpy.array([int(i) for i in line.split()])
                ne.append(iline)
    return ne, na

def getRVEdimensionsAndCentering(na):
    """
    Get dimensions and center to 0,0,0
    """
    # Nodes in different lists
    n  = numpy.int_(na[:,0])
    x  = numpy.array(na[:,1]) 
    y  = numpy.array(na[:,2])
    z  = numpy.array(na[:,3])

    # Determine dimensions of the brick and center when necessary
    [xmax,ymax,zmax]=[x.max(),y.max(),z.max()]
    [xmin,ymin,zmin]=[x.min(),y.min(),z.min()]
    print("RVE dimensions:")
    lx = xmax-xmin
    ly = ymax-ymin
    lz = zmax-zmin
    print( "lx: {0}\nly: {1}\nlz: {2}".format(lx,ly,lz))
    x = x - xmin
    y = y - ymin
    z = z - zmin
    na[:,1] = x
    na[:,2] = y
    na[:,3] = z
    
    return na, n, x, y, z, lx, ly, lz

def getRVEnodesBoundaries(tol,n,x,y,z,lx,ly,lz):
    """
    Get RVE node list for each boundary (face)
    """
    # Determine list of nodes for each limit bound
    x0 = numpy.extract(x <= tol, n)
    y0 = numpy.extract(y <= tol, n)
    z0 = numpy.extract(z <= tol, n)
    xl = numpy.extract(abs(x-lx) <= tol, n)
    yl = numpy.extract(abs(y-ly) <= tol, n)
    zl = numpy.extract(abs(z-lz) <= tol, n)
    return x0, y0, z0, xl, yl, zl

def readAlyaChaDat(source):
    """
    Read Alya .cha.dat file
    """
    stream = open(source,'r')
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
    return kfl_coh, cha_array
