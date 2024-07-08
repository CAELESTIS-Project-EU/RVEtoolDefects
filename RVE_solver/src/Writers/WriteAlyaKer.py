import math

def writeAlyaKer(file, params_gen, params_mesher, params_solver):
    """ Alya caseName.ker.dat file
    """
    # Get inputs
    dim   = params_mesher['domain']
    debug = params_solver['debug']
    tf    = params_solver['tf']
    eps   = params_solver['eps']
    u     = params_gen['R_fibre']*params_gen['delta_width']*eps
    uc    = params_mesher['c']*eps
    
    stream = open(file, 'w')
    
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  MESH\n')
    stream.write('    MULTIPLICATION\n')
    stream.write('      LEVEL= 0\n')
    stream.write('      ELEMENT_NORMAL_MULTIPLICATION: OFF\n')
    stream.write('      PARALLELIZATION:               GLOBAL\n')
    stream.write('    END_MULTIPLICATION\n')
    stream.write('  END_MESH\n')
    stream.write('  DISCRETE_FUNCTIONS\n')
    if dim == '2D':
        stream.write('    TOTAL_NUMBER= 3\n')
        stream.write('    FUNCTIONS=  F_UXX, DIMENSIONS= 2\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  {u:1.5e} 0.0\n') # Transverse tension 11
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
        stream.write('    FUNCTIONS=  F_UYY, DIMENSIONS= 2\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  0.0 {u:1.5e}\n') # Transverse tension 22
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
        stream.write('    FUNCTIONS=  F_UXY, DIMENSIONS= 2\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  {math.sin(math.pi/4.)*u:1.5e} {math.sin(math.pi/4.)*u:1.5e}\n') # Shear
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
    else:
        stream.write('    TOTAL_NUMBER= 5\n')
        stream.write('    FUNCTIONS=  F_UXX, DIMENSIONS= 3\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  {u:1.5e} 0.0 0.0\n') # Transverse tension 11
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
        stream.write('    FUNCTIONS=  F_UYY, DIMENSIONS= 3\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  0.0 {u:1.5e} 0.0\n') # Transverse tension 22
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
        stream.write('    FUNCTIONS=  F_UZZ, DIMENSIONS= 3\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  0.0 0.0 {uc:1.5e}\n') # Longitudinal tension 33
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
        stream.write('    FUNCTIONS=  F_UXY, DIMENSIONS= 3\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  {math.sin(math.pi/4.)*u:1.5e} {math.sin(math.pi/4.)*u:1.5e} 0.0\n') # Shear 12
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
        stream.write('    FUNCTIONS=  F_UYZ, DIMENSIONS= 3\n')
        stream.write('      TIME_SHAPE: LINEAR\n')
        stream.write('      SHAPE_DEFINITION\n')
        stream.write('        2\n')
        stream.write('        0.0  0.0 0.0 0.0\n')
        stream.write(f'        {tf:1.2f}  0.0 {math.sin(math.pi/4.)*uc:1.5e} {math.sin(math.pi/4.)*uc:1.5e}\n') # Shear 12
        stream.write('      END_SHAPE_DEFINITION\n')
        stream.write('    END_FUNCTIONS\n')
    stream.write('  END_DISCRETE_FUNCTIONS\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    if debug:
        stream.write('  ON_LAST_MESH\n')
        stream.write('  STEPS= 1e+6\n')
    else:
        stream.write('  NO_MESH\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')

    stream.close()

    
