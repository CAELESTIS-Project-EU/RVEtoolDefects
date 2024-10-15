from RVE_mesher.src.Mesher2D.Mesher2D import mesher2D
from RVE_mesher.src.Mesher3D.Mesher3D import mesher3D

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass

def RVE_msh_start(caseName, mesh_output, gen_output, params):

    gmshBinFile = params['gmshBinFile_path']
    gmsh2alya   = params['gmsh2alya_path']
    h           = params['h']
    c           = params['c']
    nOfLevels   = params['nOfLevels']

    if params['domain']=='2D':
        mesher2D(caseName, mesh_output, gen_output, gmshBinFile, gmsh2alya, h)
    elif params['domain']=='3D':
        mesher3D(caseName, mesh_output, gen_output, gmshBinFile, gmsh2alya, h,
                 c, nOfLevels)
    

    
