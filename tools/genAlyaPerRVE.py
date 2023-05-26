
import sys
import numpy

from opeAlyaRVE import loadAlyaGeoDat
from opeAlyaRVE import getRVEdimensionsAndCentering
from opeAlyaRVE import getRVEnodesBoundaries

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

def getNodesRVEfromVertices(lx,ly,lz,na,n):
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

def getNodesRVEfromEdges(lx,ly,lz,n,na):
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
    # Edge 1-4
    for i in e1:
        for j in e4:
            if( abs(z[i-1]-z[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 2-4
    for i in e2:
        for j in e4:
            if( abs(z[i-1]-z[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 3-4
    for i in e3:
        for j in e4:
            if( abs(z[i-1]-z[j-1]) <= tol):
                lmast.append([i,j])              
    # Edge 5-8
    for i in e5:
        for j in e8:                
            if( abs(y[i-1]-y[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 6-8
    for i in e6:
        for j in e8:                
            if( abs(y[i-1]-y[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 7-8
    for i in e7:
        for j in e8:                
            if( abs(y[i-1]-y[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 10-9
    for i in e10:
        for j in e9:
            if( abs(x[i-1]-x[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 11-9
    for i in e11:
        for j in e9:
            if( abs(x[i-1]-x[j-1]) <= tol):
                lmast.append([i,j])
    # Edge 12-9
    for i in e12:
        for j in e9:
            if( abs(x[i-1]-x[j-1]) <= tol):
                lmast.append([i,j])
    return lmast

def addNodesFromFaces(x,y,z,x0,y0,z0,bound_xl,bound_yl,bound_zl,tol,lmast):
    """
    Add nodes from faces
    """
    # Append faces
    # Faces 1-3
    for i in xl:
        if i not in bound_xl:
            for j in x0:
                ydif = abs(y[i-1]-y[j-1])
                zdif = abs(z[i-1]-z[j-1])
                if( (ydif <= tol) and (zdif <= tol) ):
                    lmast.append([i,j])
    # Faces 2-4
    for i in yl:
        if i not in bound_yl:
            for j in y0:
                xdif = abs(x[i-1]-x[j-1])
                zdif = abs(z[i-1]-z[j-1])
                if( (xdif <= tol) and (zdif <= tol) ):
                    lmast.append([i,j])
    # Face 6-5
    for i in zl:
        if i not in bound_zl:
            for j in z0:
                ydif = abs(y[i-1]-y[j-1])
                xdif = abs(x[i-1]-x[j-1])
                if( (ydif <= tol) and (xdif <= tol) ):
                    lmast.append([i,j])
    return lmast
                
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
    
    # Load Alya geometry file   
    ne, na = loadAlyaGeoDat(source)

    # Get dimensions of the RVE and center to 0,0,0 when necessary
    na, n, x, y, z, lx, ly, lz = getRVEdimensionsAndCentering(na) 

    # Get node list from each boundary (RVE face)
    x0, y0, z0, xl, yl, zl = getRVEnodesBoundaries(tol, n, x, y, z, lx, ly, lz)

    # Get nodes from vertices
    n1, n2, n3, n4, n5, n6, n7, n8 = getNodesRVEfromVertices(lx,ly,lz,na,n)

    # Get nodes from edges
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12 = getNodesRVEfromEdges(lx,ly,lz,n,na)

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
    lmast = addNodesFromFaces(x,y,z,x0,y0,z0,bound_xl,bound_yl,bound_zl,tol,lmast)

    print('Faces added!')
    print('No. nodes:',len(lmast))
    print('No. periodic nodes:',len(lmast))
    print('Sorting lmast ...')
    lmast.sort(key=lambda k: k[0])
    print( "{0} nodes constrained".format(len(lmast)))
    print('Writting Alya jobName.per.dat ...')
    writeAlyaPerDat(source,lmast)

    


