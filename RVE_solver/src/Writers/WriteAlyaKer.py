def writeAlyaKer(file, ):
    """ Alya caseName.ker.dat file
    """
    
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
    stream.write(f'        {1.0:1.1f}  0.0 0.0 {1.0e-5:1.5e}\n')
    stream.write('      END_SHAPE_DEFINITION\n')
    stream.write('    END_FUNCTIONS\n')
    stream.write('  END_DISCRETE_FUNCTIONS\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS \n')
    stream.write('  ON_LAST_MESH \n')
    stream.write('  STEPS= 1e+6 \n')
    stream.write('END_OUTPUT_&_POST_PROCESS \n')
    stream.write('$-------------------------------------------------------------------\n')

    stream.close()

    
