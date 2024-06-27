import shutil

import time

from RVE_mesher.src.GmshMesher.GmshMesher import gmshMesher

from RVE_mesher.src.Readers.GmshReader import readMesh
from RVE_mesher.src.Readers.BoundaryConditionReader import readBoundaryCondition

from RVE_mesher.src.Writers.GmshWriter import writeMesh
from RVE_mesher.src.Writers.Gmsh3dWriter import gmsh3DWriter
from RVE_mesher.src.Writers.WriteAlyaElementType import writeElementType
from RVE_mesher.src.Writers.WriteAlyaElementLocalDirections import writeElementLocalDirections
from RVE_mesher.src.Writers.WriteAlyaBoundaryCondition import writeBoundaryCondition
from RVE_mesher.src.Writers.WriteAlyaPeriodicConditions import writePeriodicConditions
from RVE_mesher.src.Writers.WriteAlyaSet import writeAlyaSet

from RVE_mesher.src.MeshOperations import \
    RemoveOuterElements, \
    DetectMaterials, \
    DetectInterfaces, \
    GlobalMeshFaces, \
    AddCohesiveElements, \
    PeriodicBoundaryConditions, \
    ObtainBoundaryFaces

from RVE_mesher.src.Extrusion import \
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

def mesher3D(caseName, mesh_output, gen_output, gmshBinFile, gmsh2alya, h, c, nOfLevels, generateCohesiveElements):
    
    # Get the start time
    t1 = time.time()

    RVE = numpy.load(os.path.join(gen_output, caseName+'.npz')) 

    scriptFile = os.path.join(mesh_output, caseName+'.geo')
    mshFile = os.path.join(mesh_output, caseName+'.msh')

    verbosityPrint('Creating gmsh script...')
    gmshMesher(RVE, h, scriptFile, mshFile)

    verbosityPrint('Running gmsh...')
    os.system(f'{gmshBinFile} {scriptFile} -o {mshFile} -v 0 -2')

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
    writeMesh(f'{os.path.join(mesh_output, caseName)}_2d.msh', x_id, T_ei, T_fi)

    verbosityPrint('Writing 3d mesh (gmsh)...')
    gmsh3DWriter(f'{os.path.join(mesh_output, caseName)}_3d.msh', x3d_id, T3d_ei, T3d_fi)

    t2 = time.time()

    verbosityPrint('Converting mesh to Alya format...')
    os.system(f'{gmsh2alya} {os.path.join(mesh_output, caseName)}_3d --bulkcodes --bcs=boundaries --out {os.path.join(mesh_output, caseName)}')

    nOf3dElements = T3d_ei.shape[0]

    verbosityPrint('Writing extra Alya mesh files...')
    if generateCohesiveElements:
        writeElementType(f'{os.path.join(mesh_output, caseName)}.cha.dat', type_e, nOfLevels)

    writeElementLocalDirections(f'{os.path.join(mesh_output, caseName)}.fie.dat', nOf3dElements)

    bcs_f = readBoundaryCondition(f'{os.path.join(mesh_output, caseName)}.fix.bou')
    writeBoundaryCondition(f'{os.path.join(mesh_output, caseName)}.fix.bou', bcs_f)

    writePeriodicConditions(f'{os.path.join(mesh_output, caseName)}.per.dat', pbcs_i)

    writeAlyaSet(f'{os.path.join(mesh_output, caseName)}.set.dat', nOf3dElements)

    verbosityPrint('Done!')

    t3 = time.time()

    if VERBOSITY == 1:
        print('Mesh generation time:', round(t2 - t1, 2), 'seconds')
        print('Mesh conversion time:', round(t3 - t2, 2), 'seconds')
        print('Total execution time:', round(t3 - t1, 2), 'seconds')

    return
