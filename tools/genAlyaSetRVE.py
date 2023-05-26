
import sys
import numpy

from opeAlyaRVE import loadAlyaGeoDat
from opeAlyaRVE import readAlyaChaDat
"""
This script generates the element set in Alya format from a brick-shaped RVE.
The element set consists of all the elments for the RVE except the interface elements.
"""

def writeAlyaSetDat(source,ne):
    """
    Write Alya Set file
    """
    # Check the existance of interface elements
    try:
        kfl_coh, cha_array = readAlyaChaDat(source+'.cha.dat')
    except:
        kfl_coh = False
        cha_array = numpy.zeros(len(ne))
    # Write Alya set file with only bulk elements
    fo = open(source+".set.dat","w")
    fo.write("ELEMENTS\n")
    for i in range(len(ne)):
        if cha_array[i] == 0:
            fo.write("{0} {1}\n".format(ne[i][0],1))
    fo.write("END_ELEMENTS\n")
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

    # Load Alya geometry file   
    ne, na = loadAlyaGeoDat(source)
    
    # Write new files
    print('Writting Alya jobName.set.dat ...')
    writeAlyaSetDat(source,ne)
