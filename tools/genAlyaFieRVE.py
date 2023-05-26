
import sys
import numpy

from opeAlyaRVE import loadAlyaGeoDat

"""
This script generates the field of material system in Alya format from a brick-shaped RVE.
The elemental field of vectors is constant.
"""

def writeAlyaFieDat(source,ne,vecto):
    """
    Write Alya Field file
    """
    # Write Alya set file with only bulk elements
    fo = open(source+".fie.dat","w")
    fo.write("FIELD= 1\n")
    for i in range(len(ne)):
        fo.write(f'{ne[i][0]} ' + vecto +'\n')
    fo.write("END_FIELD\n")
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

    # Material vectors

    vecto = '0.0 0.0 1.0  1.0 0.0 0.0  0.0 1.0 0.0'
    
    # Write new files
    print('Writting Alya jobName.fie.dat ...')
    writeAlyaFieDat(source,ne,vecto)
