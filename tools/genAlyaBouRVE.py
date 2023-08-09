
import sys
import numpy

from opeAlyaRVE import loadAlyaGeoDat
from opeAlyaRVE import getRVEdimensionsAndCentering
from opeAlyaRVE import getRVEnodesBoundaries
from opeAlyaRVE import getRVEelementBoundaries
from opeAlyaRVE import getRVEnodesBoundaries

from WriteAlyaBou import writeAlyaBou
from WriteAlyaFix import writeAlyaFix

"""
This script generates the list of external boundaries in Alya format from a brick-shaped RVE.
We assume that it's corners are at (0,0,0) and (lx,ly,lz). The dimensions are determined from the nodal coordinates.
"""

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
    e1list, e2list, e3list, e4list, e5list, e6list = getRVEelementBoundaries(ne, x0, x1, y0, y1, z0, z1)
    blist = [[e1list,x0], [e2list,xl], [e3list,y0], [e4list,yl], [e5list,z0], [e6list,zl]]

    # Built RVE element boundaries for each boundary
    b_list, nboun = getRVEboundaries(ne,blist)

    # Write new files
    path = './'
    fileName = source
    print('Writting Alya jobName.bou.dat ...')
    writeAlyaBou(path, fileName, b_list)
    print('Writting Alya jobName.fix.dat ...')
    writeAlyaFix(path, fileName, b_list)

    # Print total bounaries
    print('Total boundaries created:',nboun)
    
