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
    PeriodicBoundaryConditions, \
    ObtainBoundaryFaces, \
    Set2DBoundaries

import numpy
import os

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass

def joinPeriodicBoundaryConditions(e42_i, e31_i, v41_i, v42_i, v43_i):
    unsortedPbc_i = numpy.concatenate(
        [
            e42_i,
            e31_i,
            v41_i,
            v42_i,
            v43_i
        ]
    )

    permutation = numpy.argsort(unsortedPbc_i[:, 1])

    pbc_i = numpy.zeros(unsortedPbc_i.shape, dtype='int')
    pbc_i[:, 0] = unsortedPbc_i[permutation, 1]
    pbc_i[:, 1] = unsortedPbc_i[permutation, 0]

    return pbc_i

def mesher2D(caseName, mesh_output, gen_output, gmshBinFile, gmsh2alya, h):
    """
    Boundary conditions:

     D            C               4
      o----------o          o----------o
      |          |          |          |
      |          |          |          |
      |          |        1 |          | 2
      |          |          |          |
      |          |          |          |
      o----------o          o----------o
     A            B               3

       ^ y
       |
       |      x
       o----->
    
       CODE 1: LEFT,  X= 0
       CODE 2: RIGHT, X= lx
       CODE 3: BOT,   Y= 0
       CODE 4: TOP,   Y= ly
    
          Edges         Vertices
       ------------------------------------------------
       Slave Master    Slave Master
        DC    AB         B     A
        BC    AD         C     A
                         D     A
    
     Materials:
        CODE 1: MATRIX
        CODE 2: FIBER
        CODE 3: DAMAGED FIBER (OPTIONAL)
    """
    
    # Get the start time
    t1 = time.time()

    RVE = numpy.load(os.path.join(gen_output, caseName+'.npz')) 

    scriptFile = os.path.join(mesh_output, caseName+'.geo')
    mshFile = os.path.join(mesh_output, caseName+'.msh')

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
    
    verbosityPrint('Classifying boundary faces...')
    b1_f, b2_f, b3_f, b4_f = DetectInterfaces.detectInterfaces(x_id, T_fi, a, b)
    Tb_fi = Set2DBoundaries.set2DBoundaries(b1_f, b2_f, b3_f, b4_f, T_fi)

    verbosityPrint('Obtaining periodic boundary conditions...')
    f1_i, e42_i, e31_i, v41_i, v42_i, v43_i = \
        PeriodicBoundaryConditions.periodicBoundaryConditions(x_id, a, b)

    pbcs_i = joinPeriodicBoundaryConditions(e42_i, e31_i, v41_i, v42_i, v43_i)

    verbosityPrint('Writing 2d mesh (gmsh)...')
    writeMesh(f'{os.path.join(mesh_output, caseName)}_2d.msh', x_id, T_ei, Tb_fi)

    t2 = time.time()

    verbosityPrint('Converting mesh to Alya format...')
    os.system(f'{gmsh2alya} {os.path.join(mesh_output, caseName)}_2d --bulkcodes --bcs=boundaries --out {os.path.join(mesh_output, caseName)}')

    nOfElements = T_ei.shape[0]

    verbosityPrint('Writing extra Alya mesh files...')

    writeElementLocalDirections(os.path.join(mesh_output, caseName+'.fie.dat'), nOfElements)

    bcs_f = readBoundaryCondition(os.path.join(mesh_output, caseName+'.fix.bou'))
    writeBoundaryCondition(os.path.join(mesh_output, caseName+'.fix.bou'), bcs_f)

    writePeriodicConditions(os.path.join(mesh_output, caseName+'.per.dat'), pbcs_i)

    writeAlyaSet(os.path.join(mesh_output, caseName+'.set.dat'), nOfElements)

    verbosityPrint('Done!')

    t3 = time.time()

    if VERBOSITY == 1:
        print('Mesh generation time:', round(t2 - t1, 2), 'seconds')
        print('Mesh conversion time:', round(t3 - t2, 2), 'seconds')
        print('Total execution time:', round(t3 - t1, 2), 'seconds')

    return


