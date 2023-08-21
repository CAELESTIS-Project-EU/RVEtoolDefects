import shutil

import time

from GmshMesher.GmshMesher import gmshMesher

from Readers.GmshReader import readMesh
from Readers.BoundaryConditionReader import readBoundaryCondition

from Writers.GmshWriter import writeMesh
from Writers.Gmsh3dWriter import gmsh3DWriter
from Writers.WriteAlyaElementType import writeElementType
from Writers.WriteAlyaElementLocalDirections import writeElementLocalDirections
from Writers.WriteAlyaBoundaryCondition import writeBoundaryCondition
from Writers.WriteAlyaPeriodicConditions import writePeriodicConditions
from Writers.WriteAlyaSet import writeAlyaSet

from MeshOperations import \
    RemoveOuterElements, \
    DetectMaterials, \
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

def mesher3D(file, gmshBinFile, gmsh2alya, dataPath, outputPath, h, c, nOfLevels, generateCohesiveElements):
    # Get the start time
    t1 = time.time()

    RVE = numpy.load(f'{dataPath}/{file}.npz')

    scriptFile = f'{outputPath}/{file}.geo'
    mshFile = f'{outputPath}/{file}.msh'

    verbosityPrint('Creating gmsh script...')
    gmshMesher(RVE, h, scriptFile, mshFile)

    verbosityPrint('Running gmsh...')
    os.system(f'{gmshBinFile} {scriptFile} -v 0 -')

    verbosityPrint('Reading mesh file...')
    x_id, T_ei, T_fi = readMesh(mshFile)

    a = RVE['a']
    b = RVE['b']

    verbosityPrint('Removing outer elements...')
    x_id, T_ei, T_fi = RemoveOuterElements.removeOuterElements(x_id, T_ei, T_fi, a, b)
    # writeMesh(f'{outputPath}/{file}_repaired.msh', x_id, T_ei, T_fi)

    verbosityPrint('Detecting materials...')
    T_ei = DetectMaterials.detectMaterials(RVE['Fibre_pos'], x_id, T_ei)

    verbosityPrint('Obtaining global faces...')
    faces_ef, e_fe, markedFaces_f, interfaces_f = GlobalMeshFaces.globalMeshFaces(T_ei, T_fi)

    if generateCohesiveElements:
        verbosityPrint('Adding cohesive elements...')
        x_id, T_ei, type_e = AddCohesiveElements.addCohesiveElements(x_id, T_ei, T_fi, faces_ef, e_fe,
                                                                     markedFaces_f, interfaces_f)
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
    pbcs_i = ExtrudePeriodicBoundaryCondition.extrudeBoundaryConditions(f1_i, e42_i, e31_i, v41_i, v42_i, v43_i,
                                                                        nOfNodes2d, nOfLevels)

    verbosityPrint('Writing 2d mesh (gmsh)...')
    writeMesh(f'{outputPath}/{file}_2d.msh', x_id, T_ei, T_fi)

    verbosityPrint('Writing 3d mesh (gmsh)...')
    gmsh3DWriter(f'{outputPath}/{file}_3d.msh', x3d_id, T3d_ei, T3d_fi)

    # oneFibre_3d --bulk "1,2,3,4" --bcs=boundaries

    t2 = time.time()

    verbosityPrint('Converting mesh to Alya format...')
    os.system(f'{gmsh2alya} {outputPath}/{file}_3d --bulkcodes --bcs=boundaries --out {outputPath}{file}')

    nOf3dElements = T3d_ei.shape[0]

    verbosityPrint('Writing extra Alya mesh files...')
    if generateCohesiveElements:
        writeElementType(f'{outputPath}{file}.cha.dat', type_e, nOfLevels)

    writeElementLocalDirections(f'{outputPath}{file}.fie.dat', nOf3dElements)

    bcs_f = readBoundaryCondition(f'{outputPath}{file}.fix.bou')
    writeBoundaryCondition(f'{outputPath}{file}.fix.bou', bcs_f)

    writePeriodicConditions(f'{outputPath}{file}.per.dat', pbcs_i)

    writeAlyaSet(f'{outputPath}{file}.set.dat', nOf3dElements)

    verbosityPrint('Done!')

    t3 = time.time()

    if VERBOSITY == 1:
        print('Mesh generation time:', round(t2 - t1, 2), 'seconds')
        print('Mesh conversion time:', round(t3 - t2, 2), 'seconds')
        print('Total execution time:', round(t3 - t1, 2), 'seconds')

    return
