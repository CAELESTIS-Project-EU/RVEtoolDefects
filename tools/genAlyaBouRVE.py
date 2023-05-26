
import sys
import numpy

from opeAlyaRVE import loadAlyaGeoDat
from opeAlyaRVE import getRVEdimensionsAndCentering
from opeAlyaRVE import getRVEnodesBoundaries

"""
This script generates the list of external boundaries in Alya format from a brick-shaped RVE.
We assume that it's corners are at (0,0,0) and (lx,ly,lz). The dimensions are determined from the nodal coordinates.
"""

def getRVEelementBoundaries(ne):
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
    
def writeAlyaBouDat(blist):
    """
    Write Alya boundar file
    """
    fo = open(source+".bou.dat","w")
    fo.write("BOUNDARIES, ELEMENTS\n")
    iboun = 0
    for i in range(len(blist)):
        b = blist[i]
        for i in range(len(b)):
            iboun += 1
            ib = b[i]
            if len(ib) == 4:
                # TRI03
                fo.write("{0} {1} {2} {3} {4}\n".format(iboun,ib[0],ib[1],ib[2],ib[3]))
            elif len(ib) == 5:
                # QUA04
                fo.write("{0} {1} {2} {3} {4} {5}\n".format(iboun,ib[0],ib[1],ib[2],ib[3],ib[4]))
    fo.write("END_BOUNDARIES\n")
    fo.close()

def writeAlyaFixDat(blist):
    """
    Write Alya fixity file
    """
    fo = open(source+".fix.dat","w")
    fo.write("ON_BOUNDARIES\n")
    iboun = 0
    icode = 0
    for i in range(len(blist)):
        b = blist[i]
        icode += 1
        for i in range(len(b)):
            iboun += 1
            fo.write("{0} {1}\n".format(iboun,icode))
    fo.write("END_ON_BOUNDARIES\n")
    fo.close()

if __name__ == '__main__':

    # processing command line arguments, get the
    # jobname
    if len(sys.argv)>1:
        print( "Using file:",sys.argv[1])
        source = sys.argv[1]
    else:
        print( "Specify mesh file")
        quit()

    # Mapping tolerance
    tol = 1.0e-6
    
    # Load Alya geometry file   
    ne, na = loadAlyaGeoDat(source)
        
    # Get dimensions of the RVE and center to 0,0,0 when necessary
    na, n, x, y, z, lx, ly, lz = getRVEdimensionsAndCentering(na)

    # Get node list from each boundary (RVE face)
    x0, y0, z0, xl, yl, zl = getRVEnodesBoundaries(tol, n, x, y, z, lx, ly, lz)

    # Get element list from each boundary (RVE face)
    e1list, e2list, e3list, e4list, e5list, e6list = getRVEelementBoundaries(ne)
    blist = [[e1list,x0], [e2list,xl], [e3list,y0], [e4list,yl], [e5list,z0], [e6list,zl]]

    # Built RVE element boundaries for each boundary
    b_list, nboun = getRVEboundaries(ne,blist)

    # Write new files
    print('Writting Alya jobName.bou.dat ...')
    writeAlyaBouDat(b_list)
    print('Writting Alya jobName.fix.dat ...')
    writeAlyaFixDat(b_list)

    # Print total bounaries
    print('Total boundaries created:',nboun)
    
