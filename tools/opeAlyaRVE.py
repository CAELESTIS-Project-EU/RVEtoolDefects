
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

def getRVEelementBoundaries(ne, x0, xl, y0, yl, z0, zl):
    """
    Get RVE element list for each boundary (face)
    """
    # List of elements belonging to the boundary elemetns
    e1list = [] # X = 0
    e2list = [] # X = L
    e3list = [] # Y = 0
    e4list = [] # Y = L
    e5list = [] # Z = 0
    e6list = [] # Z = L
    for i in range(len(ne)):
        ielem = ne[i][0]
        elcon = ne[i][1:]
        for inode in elcon:
            if inode in x0:
                e1list.append(ielem)
            elif inode in xl:
                e2list.append(ielem)
            elif inode in y0:
                e3list.append(ielem)
            elif inode in yl:
                e4list.append(ielem)
            elif inode in z0:
                e5list.append(ielem)
            elif inode in zl:
                e6list.append(ielem)        

    # Remove repeated nodes for each list
    e1list = list(set(e1list))
    e2list = list(set(e2list))
    e3list = list(set(e3list))
    e4list = list(set(e4list))
    e5list = list(set(e5list))
    e6list = list(set(e6list))
    return e1list, e2list, e3list, e4list, e5list, e6list
    
def getRVEboundaries(ne,blist):
    """
    Get RVE boundaries for each ID.
    """
    #
    # Defining possible face connectivities
    #
    surfhex08 = {'s1' : [4, 3, 2, 1],
                 's2' : [5, 6, 7, 8],
                 's3' : [2, 3, 7, 6],
                 's4' : [1, 5, 8, 4],
                 's5' : [3, 4, 8, 7],
                 's6' : [1, 2, 6, 5]}
    surfpen06 = {'s1' : [3, 2, 1],
                 's2' : [5, 6, 4],
                 's3' : [2, 5, 4, 1],
                 's4' : [3, 6, 5, 2],
                 's5' : [1, 4, 6, 3]}
    b_list = []
    nboun = 0
    for iboun in range(len(blist)):
        elist       = blist[iboun][0]
        nodes_plane = blist[iboun][1]
        b = []
        for ielem in elist:
            # Line element connectivity: element_id node1, node2, node3
            e = ne[ielem-1]
            if len(e) == 7:
                surfelem = surfpen06
            elif len(e) == 9:
                surfelem = surfhex08
            else:
                print('Element type not found!')
                exit()
            for s, c in surfelem.items():
                bcon = list([i for i in e[c]])
                iBelongToBoundary = all(inode in nodes_plane for inode in bcon)
                if iBelongToBoundary:
                    nboun += 1
                    bcon = bcon + [ielem]
                    b.append(bcon)
        b_list.append(b)
        
    return b_list, nboun
