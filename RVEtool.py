import os
import yaml
import argparse
try:
    from RVE_gen.rve_generator import RVEgen
except:
    print('Reading from existing files ...')
    pass
from RVE_mesher.src import RVEmsh
from RVE_solver.src import RVEsol
import numpy as num

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
    try:
        RVEgen.RVE_gen_start(JobName, gen_output, params['RVE_gen'])
    except:
        pass
        
    # RVE mesher
    #-------------------------------------------------------------------
    RVEmsh.RVE_msh_start(JobName, mesh_output, gen_output, params['RVE_mesher'])

    # RVE solver
    #-------------------------------------------------------------------
    # Create load case scenarios
    for iload in params['RVE_solver']['listloads']:
        outputPath = os.path.join(solve_output, JobName+'-'+iload)
        if params['RVE_mesher']['domain'] == '2D' and iload in ['11','22','12','XX','YY','XY']:
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            # Run Alya writer
            RVEsol.RVE_sol_start(JobName, mesh_output, outputPath, iload,
                                 params['RVE_gen'], params['RVE_mesher'],
                                 params['RVE_solver'], params['Material'], params['General'])
        elif params['RVE_mesher']['domain'] == '3D':
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            # Run Alya writer
            RVEsol.RVE_sol_start(JobName, mesh_output, outputPath, iload,
                                 params['RVE_gen'], params['RVE_mesher'],
                                 params['RVE_solver'], params['Material'], params['General'])
        else:
            continue
        
if __name__=='__main__':

    RVEtool_parser = argparse.ArgumentParser(description="Run RVEtool from configuration file")
    RVEtool_parser.add_argument('-e', '--exp-file', type=str, required=True, help="Specify the configuration file path")
    args = RVEtool_parser.parse_args()
    exp_file = args.exp_file
    if os.path.exists(exp_file):
        print(f"The provided experiment file path is: {exp_file}")
    else:
        print(f"Error: The experiment {exp_file} does not exist.")
        exit(1)

    # Run program
    runRVEtool(exp_file)    
