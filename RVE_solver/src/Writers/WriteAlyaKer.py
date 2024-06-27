def writeAlyaKer(file, iload, params_solver):
    """ Alya caseName.ker.dat file
    """
    # Get inputs
    debug = params_solver['debug']
    tf    = params_solver['tf']
    u     = params_solver['u']
    
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
    stream.write('    TOTAL_NUMBER= 1\n')
    stream.write('    FUNCTIONS=  U_FUNC, DIMENSIONS= 3\n')
    stream.write('      TIME_SHAPE: LINEAR\n')
    stream.write('      SHAPE_DEFINITION\n')
    stream.write('        2\n')
    stream.write('        0.0  0.0 0.0 0.0\n')
    if iload == '11':
        # Longitudinal tension
        stream.write(f'        {tf:1.2f}  0.0 0.0 {u:1.5e}\n')
    elif iload == '22':
        # Transverse tension
        stream.write(f'        {tf:1.2f}  0.0 {u:1.5e} 0.0\n')
    elif iload == '12':
        # In-plane shear
        stream.write(f'        {tf:1.2f}  {u:1.5e} 0.0 0.0\n')
    elif iload == '23':
        # Transverse shear
        stream.write(f'        {tf:1.2f}  0.0 0.0 {u:1.5e}\n')
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

    
