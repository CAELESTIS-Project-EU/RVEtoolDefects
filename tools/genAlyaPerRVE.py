
import sys
import numpy

from opeAlyaRVE import loadAlyaGeoDat
from opeAlyaRVE import getRVEdimensionsAndCentering
from opeAlyaRVE import getRVEnodesBoundaries
from opeAlyaRVE import getRVEnodesFromVertices
from opeAlyaRVE import getRVEnodesFromEdges
from opeAlyaRVE import addNodesFromVertices
from opeAlyaRVE import addNodesFromEdges
from opeAlyaRVE import addNodesFromFaces
from opeAlyaRVE import addNodesFromFacesMeso

"""
This script generates the list of master-slave nodes in Alya format from a brick-shaped RVE.
We assume that it's corners are at (0,0,0) and (lx,ly,lz). The dimensions are determined from the nodal coordinates.
"""

def writeAlyaPerDat(source,lmast):
    """
    Write Alya jobName.per.dat
    """
    fo = open(source+".per.dat","w")
    fo.write("LMAST\n")
    for i in range(len(lmast)):
        fo.write("{0} {1}\n".format(lmast[i][0],lmast[i][1]))
    fo.write("END_LMAST\n")
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
    
    # Mapping accuracy
    tol = 1.0e-6

    # RVE type
    typeRVE = 'micro' # micro or meso
    flowDirection = 'x'
    
    # Load Alya geometry file   
    ne, na = loadAlyaGeoDat(source)

    # Get dimensions of the RVE and center to 0,0,0 when necessary
    na, n, x, y, z, lx, ly, lz = getRVEdimensionsAndCentering(na) 

    # Get node list from each boundary (RVE face)
    x0, y0, z0, xl, yl, zl = getRVEnodesBoundaries(tol, n, x, y, z, lx, ly, lz)

    # Get nodes from vertices
    n1, n2, n3, n4, n5, n6, n7, n8 = getRVEnodesFromVertices(lx,ly,lz,na,n)

    # Get nodes from edges
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12 = getRVEnodesFromEdges(lx,ly,lz,n,na,n1,n2,n3,n4,n5,n6,n7,n8)

    bound_xl = e1  + e2  + e5  + e6  + [n1] + [n2] + [n3] + [n4]
    bound_yl = e2  + e3  + e10 + e11 + [n2] + [n3] + [n6] + [n7]
    bound_zl = e6  + e7  + e11 + e12 + [n3] + [n4] + [n7] + [n8]

    # Slave - master approach
    lmast = []
    print('Adding nodes from vertices ...')
    lmast = addNodesFromVertices(n1,n2,n3,n4,n5,n6,n7,n8,lmast)

    print('Adding nodes from edges ...')
    lmast = addNodesFromEdges(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,x,y,z,tol,lmast)

    print('Adding nodes from faces ...')
    if typeRVE == 'micro':
        lmast = addNodesFromFaces(x,y,z,x0,y0,z0,xl,yl,zl,bound_xl,bound_yl,bound_zl,tol,lmast)
    else:
        lmast = addNodesFromFacesMeso(flowDirection,x,y,z,x0,y0,z0,xl,yl,zl,bound_xl,bound_yl,bound_zl,tol,lmast)
        
    print('Faces added!')
    print('No. nodes:',len(lmast))
    print('No. periodic nodes:',len(lmast))
    print('Sorting lmast ...')
    lmast.sort(key=lambda k: k[0])
    print( "{0} nodes constrained".format(len(lmast)))
    print('Writting Alya jobName.per.dat ...')
    writeAlyaPerDat(source,lmast)

    


