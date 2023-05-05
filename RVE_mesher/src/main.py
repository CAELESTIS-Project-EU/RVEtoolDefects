import pathlib
path = pathlib.Path(__file__).parent.resolve()

import sys
sys.path.append(path)

import shutil

from GmshMesher.GmshMesher import gmshMesher

from Readers.GmshReader import readMesh
from Readers.BoundaryConditionReader import readBoundaryCondition

from Writers.GmshWriter import writeMesh
from Writers.Gmsh3dWriter import gmsh3DWriter
from Writers.WriteAlyaElementType import writeElementType
from Writers.WriteAlyaElementLocalDirections import writeElementLocalDirections
from Writers.WriteAlyaBoundaryCondition import writeBoundaryCondition
from Writers.WriteAlyaPeriodicConditions import writePeriodicConditions
from Writers.WriteAlyaDom import writeAlyaDom
from Writers.WriteAlyaSet import writeAlyaSet

from MeshOperations import \
    RemoveOuterElements,\
    DetectMaterials,\
    DetectInterfaces, \
    GlobalMeshFaces, \
    AddCohesiveElements, \
    PeriodicBoundaryConditions, \
    ObtainBoundaryFaces

from Extrusion import \
    ExtrudeMesh, \
    ExtrudeBoundaries, \
    ExtrudePeriodicBoundaryCondition

import numpy
import os

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass

def runMesher(file, dataPath, outputPath, h, c, nOfLevels, generateCohesiveElements):

    RVE = numpy.load(f'{dataPath}/{file}.npz')

    scriptFile = f'{outputPath}/{file}.geo'
    mshFile = f'{outputPath}/{file}.msh'

    verbosityPrint('Creating gmsh script...')
    gmshMesher(RVE, h, scriptFile, mshFile)

    verbosityPrint('Running gmsh...')
    os.system(f'gmsh {scriptFile} -v 0 -')

    verbosityPrint('Reading mesh file...')
    x_id, T_ei, T_fi = readMesh(mshFile)

    a = RVE['a']
    b = RVE['b']

    verbosityPrint('Removing outer elements...')
    x_id, T_ei, T_fi = RemoveOuterElements.removeOuterElements(x_id, T_ei, T_fi, a, b)
    writeMesh(f'{outputPath}/{case}_repaired.msh', x_id, T_ei, T_fi)

    verbosityPrint('Detecting materials...')
    T_ei = DetectMaterials.detectMaterials(RVE['Fibre_pos'], x_id, T_ei)

    verbosityPrint('Obtaining global faces...')
    faces_ef, e_fe, markedFaces_f, interfaces_f = GlobalMeshFaces.globalMeshFaces(T_ei, T_fi)

    if generateCohesiveElements:
        verbosityPrint('Adding cohesive elements...')
        x_id, T_ei, type_e = AddCohesiveElements.addCohesiveElements(x_id, T_ei, T_fi, faces_ef, e_fe, markedFaces_f, interfaces_f)

        verbosityPrint('Obtaining new boundary faces...')
        T_fi = ObtainBoundaryFaces.obtainBoundaryFaces(T_ei)

    verbosityPrint('Classifying boundary faces...')
    b1_f, b2_f, b3_f, b4_f = DetectInterfaces.detectInterfaces(x_id, T_fi, a, b)

    verbosityPrint('Obtaining periodic boundary conditions...')
    f1_i, e42_i, e31_i, v41_i, v42_i, v43_i = \
        PeriodicBoundaryConditions.periodicBoundaryConditions(x_id, a, b)

    verbosityPrint('Extruding mesh...')
    x3d_id, T3d_ei = ExtrudeMesh.extrudeMesh(x_id, T_ei, c, nOfLevels)

    verbosityPrint('Extruding boundaries')
    nOfNodes2d = x_id.shape[0]
    T3d_fi = ExtrudeBoundaries.extrudeBoundaries(T_ei, b1_f, b2_f, b3_f, b4_f, T_fi, nOfLevels, nOfNodes2d)

    verbosityPrint('Extruding periodic conditions')
    pbcs_i = ExtrudePeriodicBoundaryCondition.extrudeBoundaryConditions(f1_i, e42_i, e31_i, v41_i, v42_i, v43_i, nOfNodes2d, nOfLevels)

    verbosityPrint('Writing 2d mesh (gmsh)...')
    writeMesh(f'{outputPath}/{file}_2d.msh', x_id, T_ei, T_fi)

    verbosityPrint('Writing 3d mesh (gmsh)...')
    gmsh3DWriter(f'{outputPath}/{file}_3d.msh', x3d_id, T3d_ei, T3d_fi)

    # oneFibre_3d --bulk "1,2,3,4" --bcs=boundaries

    verbosityPrint('Converting mesh to Alya format...')
    os.system(f'gmsh2alya.pl {outputPath}/{file}_3d --bulkcodes --bcs=boundaries --out {outputPath}{file}')

    nOf3dNodes = x3d_id.shape[0]
    nOf3dElements = T3d_ei.shape[0]
    dim = 3
    nOfMaterials = 4

    verbosityPrint('Writing Alya files...')
    if generateCohesiveElements:
        writeElementType(f'{outputPath}{file}.cha.dat', type_e, nOfLevels)

    writeElementLocalDirections(f'{outputPath}{file}.fie.dat', nOf3dElements)

    bcs_f = readBoundaryCondition(f'{outputPath}{file}.fix.bou')
    writeBoundaryCondition(f'{outputPath}{file}.fix.bou', bcs_f)

    writePeriodicConditions(f'{outputPath}{file}.per.dat', pbcs_i)

    writeAlyaDom(f'{outputPath}{file}.dom.dat', case, dim, nOfMaterials, generateCohesiveElements)
    writeAlyaSet(f'{outputPath}{file}.set.dat', nOf3dElements)

    verbosityPrint('Done!')



if __name__ == '__main__':

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
    
    basePath = f'{path}/../..'
    dataPath = f'{basePath}/RVE_gen/data'
    outputPath = f'{basePath}/output/'+case+'/'
    if os.path.exists(outputPath):
        shutil.rmtree(f'{basePath}/output/'+case+'/')
    os.makedirs(outputPath)
    runMesher(case, dataPath, outputPath, h, c, nOfLevels, generateCohesiveElements)
