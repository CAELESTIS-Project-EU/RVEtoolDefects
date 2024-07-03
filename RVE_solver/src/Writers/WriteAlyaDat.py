def writeAlyaDat(file, filename, dash_iload, params_solver):
    """ Alya caseName.dat file
    """
    debug = params_solver['debug']
    tf    = params_solver['tf']
    tinc  = params_solver['tinc']
    
    stream = open(file, 'w')
    
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('RUN_DATA\n')
    stream.write(f'  ALYA:                   {filename+dash_iload:s}\n')
    stream.write('  CODE=                   1\n')
    if debug:
        stream.write('  LIVE_INFO:              FILE\n')
        stream.write('  LOG_FILE:               ON\n')
    else:
        stream.write('  LIVE_INFO:              FILE\n')
        stream.write('  LOG_FILE:               OFF\n')        
    stream.write('END_RUN_DATA\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PROBLEM_DATA\n')
    stream.write('  TIME_COUPLING:          GLOBAL, PRESCRIBED\n')
    stream.write(f'  TIME_INTERVAL:          {0.0:1.5f} {tf:1.5f}\n')
    stream.write(f'  TIME_STEP_SIZE=         {tinc:1.5f}\n')
    if debug:
        stream.write('  NUMBER_OF_STEPS=        0\n')
    else:
        stream.write('  NUMBER_OF_STEPS=        1e6\n')
    stream.write('  MAXIMUM_NUMBER_GLOBAL=  1\n')
    stream.write('  SOLIDZ_MODULE:          ON\n')
    stream.write('  END_SOLIDZ_MODULE\n')
    stream.write('  PARALL_SERVICE:         ON\n')
    stream.write('  OUTPUT_FILE:            OFF\n')
    stream.write('    POSTPROCESS:          MASTER\n')
    stream.write('    PARTITION_TYPE:       FACES\n')
    stream.write('    PARTITIONING:\n')
    stream.write('      METHOD:             METIS\n')
    stream.write('    END_PARTITIONING\n')
    stream.write('  END_PARALL_SERVICE\n')
    stream.write('END_PROBLEM_DATA\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('MPI_IO:                   OFF\n')
    stream.write('  GEOMETRY:               OFF\n')
    stream.write('  POSTPROCESS:            OFF\n')
    stream.write('  RESTART:                OFF\n')
    stream.write('  MERGE:                  OFF\n')
    stream.write('  SYNCHRONOUS:            OFF\n')
    stream.write('END_MPI_IO\n')
    stream.write('$-------------------------------------------------------------------\n')

    stream.close()

    
