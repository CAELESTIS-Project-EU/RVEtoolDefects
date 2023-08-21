
import os
import numpy

"""
General furnctions for operate a RVE mesh in Alya
"""

def loadAlyaGeoDat(source):
    """
    Load coordinates and element connectivity files 
    Skip first and last rows
    """
    # Alya coordinates list
    possible_extensions = ['.nod.dat', '.coo.dat', '.coor.dat']
    fileName = None
    for extension in possible_extensions:
        file_path = f"{source}{extension}"
        if os.path.isfile(file_path):
            fileName = file_path
            break
    if fileName:
        try:
            na = numpy.loadtxt(open(fileName).readlines()[:-1], skiprows=1, dtype=None)
        except FileNotFoundError:
            print('FileNotFoundError')
    else:
        print("No valid file found.")
            
    # Alya element connectivity list
    possible_extensions = ['.ele.dat', '.con.dat']
    fileName = None
    for extension in possible_extensions:
        file_path = f"{source}{extension}"
        if os.path.isfile(file_path):
            fileName = file_path
            break
    if fileName:
        try:
            ne = []
            with open(fileName,'r') as fcon:
                for line in fcon:
                    if line.split()[0] == 'ELEMENTS':
                        continue
                    elif line.split()[0] == 'END_ELEMENTS':
                        continue
                    else:
                        iline = numpy.array([int(i) for i in line.split()])
                        ne.append(iline)
        except FileNotFoundError:
            print('FileNotFoundError')
    else:
        print("No valid file found.")
        
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

def getRVEnodesFromVertices(lx,ly,lz,na,n):
    """
    Get nodes RVE from vertices
    """
    n1 = numpy.extract([pt==[lx,0.,0.] for pt in na[:,1:].tolist()],n)[0]
    n2 = numpy.extract([pt==[lx,ly,0.] for pt in na[:,1:].tolist()],n)[0]
    n3 = numpy.extract([pt==[lx,ly,lz] for pt in na[:,1:].tolist()],n)[0]
    n4 = numpy.extract([pt==[lx,0.,lz] for pt in na[:,1:].tolist()],n)[0]
    n5 = numpy.extract([pt==[0.,0.,0.] for pt in na[:,1:].tolist()],n)[0]
    n6 = numpy.extract([pt==[0.,ly,0.] for pt in na[:,1:].tolist()],n)[0]
    n7 = numpy.extract([pt==[0.,ly,lz] for pt in na[:,1:].tolist()],n)[0]
    n8 = numpy.extract([pt==[0.,0.,lz] for pt in na[:,1:].tolist()],n)[0]

    return n1,n2,n3,n4,n5,n6,n7,n8

def getRVEnodesFromEdges(lx,ly,lz,n,na,n1,n2,n3,n4,n5,n6,n7,n8):
    """
    Get nodes RVE from edges
    """
    # x-y
    e1 = numpy.extract([pt == [lx,0.] for pt in na[:,1:3].tolist()],n)
    e1 = e1.tolist()
    e2 = numpy.extract([pt == [lx,ly] for pt in na[:,1:3].tolist()],n)
    e2 = e2.tolist()
    e3 = numpy.extract([pt == [0.,ly] for pt in na[:,1:3].tolist()],n)
    e3 = e3.tolist()
    e4 = numpy.extract([pt == [0.,0.] for pt in na[:,1:3].tolist()],n)
    e4 = e4.tolist()
    # y-z
    e9  = numpy.extract([pt == [0.,0.] for pt in na[:,2:4].tolist()],n)
    e9  = e9.tolist()
    e10 = numpy.extract([pt == [ly,0.] for pt in na[:,2:4].tolist()],n)
    e10 = e10.tolist()
    e11 = numpy.extract([pt == [ly,lz] for pt in na[:,2:4].tolist()],n)
    e11 = e11.tolist()
    e12 = numpy.extract([pt == [0.,lz] for pt in na[:,2:4].tolist()],n)
    e12 = e12.tolist()
    # x-z
    nb = na
    nb[:,2] = nb[:,3]
    e5  = numpy.extract([pt == [lx,0.] for pt in nb[:,1:3].tolist()],n)
    e5  = e5.tolist()
    e6  = numpy.extract([pt == [lx,lz] for pt in nb[:,1:3].tolist()],n)
    e6  = e6.tolist()
    e7  = numpy.extract([pt == [0.,lz] for pt in nb[:,1:3].tolist()],n)
    e7  = e7.tolist()
    e8  = numpy.extract([pt == [0.,0.] for pt in nb[:,1:3].tolist()],n)
    e8  = e8.tolist()
    # remove from the list
    e1.remove(n1)
    e1.remove(n4)
    e2.remove(n2)
    e2.remove(n3)
    e3.remove(n6)
    e3.remove(n7)
    e4.remove(n5)
    e4.remove(n8)
    e5.remove(n1)
    e5.remove(n2)
    e6.remove(n3)
    e6.remove(n4)
    e7.remove(n7)
    e7.remove(n8)
    e8.remove(n5)
    e8.remove(n6)
    e9.remove(n1)
    e9.remove(n5)
    e10.remove(n2)
    e10.remove(n6)
    e11.remove(n3)
    e11.remove(n7)
    e12.remove(n4)
    e12.remove(n8)

    return e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12

def addNodesFromVertices(n1,n2,n3,n4,n5,n6,n7,n8,lmast):
    """
    Add nodes from vertices
    """
    lmast = [[n1,n5],[n2,n5],[n3,n5],[n4,n5],[n6,n5],[n7,n5],[n8,n5]]
    return lmast

def addNodesFromEdges(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,x,y,z,tol,lmast):
    """
    Add nodes from edges
    """
    # Append edges
    # Edge 1-4 (BF-AE)
    for i in e1:
        for j in e4:
            if( abs(z[i-1]-z[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 2-4 (CG-AE)
    for i in e2:
        for j in e4:
            if( abs(z[i-1]-z[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 3-4 (DH-AE)
    for i in e3:
        for j in e4:
            if( abs(z[i-1]-z[j-1]) <= tol):
                lmast.append([i,j])              
    # Edge 5-8 (BC-AD)
    for i in e5:
        for j in e8:                
            if( abs(y[i-1]-y[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 6-8 (FG-AD)
    for i in e6:
        for j in e8:                
            if( abs(y[i-1]-y[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 7-8 (EH-AD)
    for i in e7:
        for j in e8:                
            if( abs(y[i-1]-y[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 10-9 (DC-AB)
    for i in e10:
        for j in e9:
            if( abs(x[i-1]-x[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 11-9 (HG-AB)
    for i in e11:
        for j in e9:
            if( abs(x[i-1]-x[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 12-9 (EF-AB)
    for i in e12:
        for j in e9:
            if( abs(x[i-1]-x[j-1]) <= tol):
                lmast.append([i,j])
    return lmast

def addNodesFromFaces(x,y,z,x0,y0,z0,xl,yl,zl,bound_xl,bound_yl,bound_zl,tol,lmast):
    """
    Add nodes from faces
    """
    # Faces BCGF (Slave) - ADHE (Master)
    for i in xl:
        if i not in bound_xl:
            for j in x0:
                ydif = abs(y[i-1]-y[j-1])
                zdif = abs(z[i-1]-z[j-1])
                if( (ydif <= tol) and (zdif <= tol) ):
                    lmast.append([i,j])
    # Faces DHGC (Slave) - AEFB (Master)
    for i in yl:
        if i not in bound_yl:
            for j in y0:
                xdif = abs(x[i-1]-x[j-1])
                zdif = abs(z[i-1]-z[j-1])
                if( (xdif <= tol) and (zdif <= tol) ):
                    lmast.append([i,j])
    # Faces EFGH (Slave) - ABCD (Master)
    for i in zl:
        if i not in bound_zl:
            for j in z0:
                ydif = abs(y[i-1]-y[j-1])
                xdif = abs(x[i-1]-x[j-1])
                if( (ydif <= tol) and (xdif <= tol) ):
                    lmast.append([i,j])
    return lmast

def addNodesFromFacesMeso(flowDirection,x,y,z,x0,y0,z0,xl,yl,zl,bound_xl,bound_yl,bound_zl,tol,lmast):
    """
    Add nodes from faces
    """
    # Faces BCGF (Slave) - ADHE (Master)
    for i in xl:
        if i not in bound_xl: # Slave
            for j in x0: # Master
                ydif = abs(y[i-1]-y[j-1])
                zdif = abs(z[i-1]-z[j-1])
                if( (ydif <= tol) and (zdif <= tol) ):
                    lmast.append([i,j])
                    
    # Faces DHGC (Slave) - AEFB (Master)
    for i in yl:
        if i not in bound_yl: # Slave
            for j in y0: # Master
                xdif = abs(x[i-1]-x[j-1])
                zdif = abs(z[i-1]-z[j-1])
                if( (xdif <= tol) and (zdif <= tol) ):
                    lmast.append([i,j])

    if flowDirection == 'z':
        # Faces EFGH (Slave) - ABCD (Master)
        for i in zl:
            if i not in bound_zl: # Slave
                for j in z0: # Master
                    ydif = abs(y[i-1]-y[j-1])
                    xdif = abs(x[i-1]-x[j-1])
                    if( (ydif <= tol) and (xdif <= tol) ):
                        lmast.append([i,j])

    return lmast
