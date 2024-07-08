import yaml
import os
from RVE_gen.rve_generator import RVEgen
from RVE_mesher.src import RVEmsh
from RVE_solver.src import RVEsol
import numpy as num
#num.random.seed(1) #0, 42, pilist breaks 

def runRVEtool(parameters_file):
    # Load configuration file
    with open(parameters_file, 'r') as f:
        params = yaml.safe_load(f)

    # Case Name
    JobName = params['General']['JobName']

    # Output folder to store gen, msh and solve of given case
    outputPath = params['General']['output_path']

    # Subforlders of gen, msh and solve
    gen_output   = os.path.join(outputPath, JobName, 'gen')
    mesh_output  = os.path.join(outputPath, JobName, 'msh')
    solve_output = os.path.join(outputPath, JobName)

    # Check if directory exists. If not create.
    for dir in [gen_output, mesh_output, solve_output]:
        if not os.path.isdir(dir):
            os.makedirs(dir, exist_ok=True)

    # RVE geometry generator
    #-------------------------------------------------------------------
    RVEgen.RVE_gen_start(JobName, gen_output, params['RVE_gen'])

    # RVE geometry mesher
    #-------------------------------------------------------------------
    RVEmsh.RVE_msh_start(JobName, mesh_output, gen_output, params['RVE_mesher'])

    # RVE solver
    #-------------------------------------------------------------------
    # Create load case scenarios
    for iload in params['RVE_solver']['listloads']:
        outputPath = os.path.join(solve_output, JobName+'-'+iload)
        if params['RVE_mesher']['domain'] == '2D' and iload in ['11','22','12']:
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            # Run Alya writer
            RVEsol.RVE_sol_start(JobName, mesh_output, outputPath, iload,
                                 params['RVE_gen'], params['RVE_mesher'],
                                 params['RVE_solver'], params['Material'])
        elif params['RVE_mesher']['domain'] == '3D':
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            # Run Alya writer
            RVEsol.RVE_sol_start(JobName, mesh_output, outputPath, iload,
                                 params['RVE_gen'], params['RVE_mesher'],
                                 params['RVE_solver'], params['Material'])
        else:
            continue
        
if __name__=='__main__':
    
    #parameters_file = 'Vallmajo2023_5x5.yaml'          # Vallmajo without voids small size
    #parameters_file = 'Vallmajo2023_15x15.yaml'         # Vallmajo without voids
    #parameters_file = 'Vallmajo2023_15x15_svoids.yaml' # Vallmajo with small voids 7%
    #parameters_file = 'Vallmajo2023_15x15_lvoids.yaml' # Vallmajo with small voids 7%
    #parameters_file = 'Liu2019_5x5.yaml'               # Liu
    parameters_file = 'CAELESTIS_15x15.yaml'           # CAELESTIS without voids

    parameters_file = os.path.join("examples", parameters_file)
        
    # Run program
    runRVEtool(parameters_file)    
