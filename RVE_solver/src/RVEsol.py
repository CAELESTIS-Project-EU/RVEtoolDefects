import os
import time

from RVE_solver.src.Readers.ReadAlyaMat import readAlyaMat
from RVE_solver.src.Readers.ReadAlyaCha import readAlyaCha
from RVE_solver.src.Readers.ReadAlyaGeo import readAlyaGeo

from RVE_solver.src.Writers.WriteAlyaDat import writeAlyaDat
from RVE_solver.src.Writers.WriteAlyaKer import writeAlyaKer
from RVE_solver.src.Writers.WriteAlyaDom import writeAlyaDom
from RVE_solver.src.Writers.WriteAlyaSld import writeAlyaSld3D
from RVE_solver.src.Writers.WriteAlyaSld import writeAlyaSld2D
from RVE_solver.src.Writers.WriteAlyaPos import writeAlyaPos

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass

def RVE_sol_start(file, meshPath, outputPath, iload,
                  params_solver, params_material, params_mesher):
    """
    Alya writer files
    """
    
    # Get the start time
    st = time.time()
    
    verbosityPrint('Writing Alya configuration files...')
    
    dash_iload = '-'+iload    
    writeAlyaDat(os.path.join(outputPath,file+dash_iload+'.dat'), file, dash_iload, params_solver)
    writeAlyaKer(os.path.join(outputPath,file+dash_iload+'.ker.dat'), iload, params_solver)
    if params_solver['debug']:
        writeAlyaPos(os.path.join(outputPath,file+dash_iload+'.post.alyadat'))
    
    nOfMaterials = readAlyaMat(os.path.join(meshPath,file+'.mat.dat'))

    kfl_coh = False
    if os.path.exists(os.path.join(meshPath,file+'.cha.dat')):
        kfl_coh = readAlyaCha(os.path.join(meshPath,file+'.cha.dat'))

    dim, lx, ly, lz = readAlyaGeo(os.path.join(meshPath,file+'.geo.dat'))
    if dim == 2:
        lz = params_mesher['c']
        
    writeAlyaDom(os.path.join(outputPath,file+dash_iload+'.dom.dat'), file, dim, nOfMaterials, kfl_coh)

    if dim == 2:
        writeAlyaSld2D(os.path.join(outputPath,file+dash_iload+'.sld.dat'), file, dash_iload, 'STATIC', kfl_coh, nOfMaterials, iload, lx, ly, lz, params_solver['debug'], params_solver, params_material)

    else:
        writeAlyaSld3D(os.path.join(outputPath,file+dash_iload+'.sld.dat'), file, dash_iload, 'STATIC', kfl_coh, nOfMaterials, iload, lx, ly, lz, params_solver['debug'], params_solver, params_material)

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st
    
    if VERBOSITY == 1:
        print('Execution time:', round(elapsed_time,2), 'seconds')
