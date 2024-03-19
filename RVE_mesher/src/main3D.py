import pathlib

path = pathlib.Path(__file__).parent.resolve()

import sys
sys.path.append(path)

from Mesher3D.Mesher3D import mesher3D

import shutil

import os

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass


if __name__ == '__main__':
    
    #-------------------------------------------------------------------
    # User inputs
    #-------------------------------------------------------------------

    #case = 'RVE_10_10_1'
    #h = 0.001
    #c = 0.01
    #nOfLevels = 10
    #generateCohesiveElements = False

    #case = 'RVE_Test_1'
    #h = 0.001
    #c = 0.01
    #nOfLevels = 10
    #generateCohesiveElements = False

    # case = 'twoFibres'
    # h = 0.25
    # c = 1
    # nOfLevels = 2
    # generateCohesiveElements = True

    #case = 'oneFibre'
    #h = 0.25
    #c = 1
    #nOfLevels = 2
    #generateCohesiveElements = False

    case = 'RVE_1x1_with_voids_1'
    h = 0.0005   # in-plane size
    c = 0.028   # out-plane thickness
    nOfLevels = 10
    generateCohesiveElements = True

    #-------------------------------------------------------------------
    
    # Set paths for directories  
    basePath = f'{path}/../..'
    dataPath = f'{basePath}/RVE_gen/data'
    outputPath = f'{basePath}/output/'+case+'/msh/'
    if os.path.exists(outputPath):
        shutil.rmtree(f'{basePath}/output/'+case+'/msh/')
    os.makedirs(outputPath)

    # Set paths for binaries
    gmshBinFile = 'gmsh'
    #gmshBinFile = '/gpfs/projects/bsce81/gmsh/gmsh-4.11.1-Linux64/bin/gmsh'
    gmsh2alya = 'gmsh2alya.pl'
    #gmsh2alya = '/gpfs/projects/bsce81/alya/builds/gmsh2alya.pl'
    
    # Run mesher
    mesher3D(case, gmshBinFile, gmsh2alya, dataPath, outputPath, h, c, nOfLevels, generateCohesiveElements)


