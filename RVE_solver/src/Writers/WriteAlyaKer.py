import math

def writeAlyaKer(file, lx, ly, iload, params_mesher, params_solver):
    """ Alya caseName.ker.dat file
    """
    # Get inputs
    dim   = str(params_mesher['domain'])
    debug = bool(params_solver['debug'])
    tf    = float(params_solver['tf'])
    eps   = float(params_solver['eps'])
    try:
        BCtype = str(params_solver['BCtype'])
    except:
        BCtype = 'Periodic'
    ux    = lx*eps
    uy    = ly*eps 
    uz    = float(params_mesher['c'])*eps
    
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
    stream.write('    SAVE_ELEMENT_DATA_BASE: ON\n')
    stream.write('  END_MESH\n')
    stream.write('  DISCRETE_FUNCTIONS\n')
    if BCtype == 'Periodic' or BCtype == 'Linear':
        if dim == '2D':
            if iload == '11' or iload == 'XX':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 4\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f}  {eps:1.5e} 0.0 0.0 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '22' or iload == 'YY':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 4\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f}  0.0 0.0 0.0 {eps:1.5e}\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '12' or iload == 'XY':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 4\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f}  0.0 {eps:1.5e} {eps:1.5e} 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            else:
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 4\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0 0.0\n')
                stream.write('        INCLUDE ./random_path.txt\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
                print('NOT PROGRAMMED!')
                exit()
        elif dim == '3D':
            if iload == '11' or iload == 'ZZ':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f} 0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 {eps:1.5e}\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '22' or iload == 'XX':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f} {eps:1.5e} 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '33' or iload == 'YY':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f} 0.0 0.0 0.0  0.0 {eps:1.5e} 0.0  0.0 0.0 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '23' or iload == 'XY':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f} 0.0 {eps:1.5e} 0.0  0.0 {eps:1.5e} 0.0  0.0 0.0 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '13' or iload == 'YZ':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f} 0.0 0.0 0.0  0.0 0.0 {eps:1.5e}  0.0 {eps:1.5e} 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            elif iload == '12' or iload == 'XZ':
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n')
                stream.write(f'        {tf:1.2f}  0.0 0.0 {eps:1.5e}  0.0 0.0 0.0  {eps:1.5e} 0.0 0.0\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
            else:
                stream.write('    TOTAL_NUMBER= 1\n')
                stream.write('    FUNCTIONS=  DGRAD, DIMENSIONS= 9\n')
                stream.write('      TIME_SHAPE: LINEAR\n')
                stream.write('      SHAPE_DEFINITION\n')
                stream.write('        2\n')
                stream.write('        0.0  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n')
                stream.write('        INCLUDE ./random_path.txt\n')
                stream.write('      END_SHAPE_DEFINITION\n')
                stream.write('    END_FUNCTIONS\n')
                print('NOT PROGRAMMED!')
                exit()
    elif BCtype == 'Standard':
        if dim == '2D':
            stream.write('    TOTAL_NUMBER= 3\n')
            stream.write('    FUNCTIONS=  F_UXX, DIMENSIONS= 2\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  {ux:1.5e} 0.0\n') # Transverse tension 11
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UYY, DIMENSIONS= 2\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  0.0 {uy:1.5e}\n') # Transverse tension 22
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UXY, DIMENSIONS= 2\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  {math.sin(math.pi/4.)*ux:1.5e} {math.sin(math.pi/4.)*ux:1.5e}\n') # Shear
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
        else:
            stream.write('    TOTAL_NUMBER= 6\n')
            stream.write('    FUNCTIONS=  F_UXX, DIMENSIONS= 3\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  {ux:1.5e} 0.0 0.0\n') # 
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UYY, DIMENSIONS= 3\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  0.0 {uy:1.5e} 0.0\n') 
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UZZ, DIMENSIONS= 3\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  0.0 0.0 {uz:1.5e}\n') 
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UXZ, DIMENSIONS= 3\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  {ux:1.5e} 0.0 {uz:1.5e}\n') 
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UYZ, DIMENSIONS= 3\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  0.0 {uy:1.5e} {uz:1.5e}\n') 
            stream.write('      END_SHAPE_DEFINITION\n')
            stream.write('    END_FUNCTIONS\n')
            stream.write('    FUNCTIONS=  F_UXY, DIMENSIONS= 3\n')
            stream.write('      TIME_SHAPE: LINEAR\n')
            stream.write('      SHAPE_DEFINITION\n')
            stream.write('        2\n')
            stream.write('        0.0  0.0 0.0 0.0\n')
            stream.write(f'        {tf:1.2f}  {ux:1.5e} {uy:1.5e} 0.0\n') 
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
