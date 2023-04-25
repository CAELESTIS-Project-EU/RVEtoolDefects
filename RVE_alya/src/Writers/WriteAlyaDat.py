def writeAlyaDat(file,filename ):
    """ Alya caseName.dat file
    """
    
    stream = open(file, 'w')
    
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('RUN_DATA\n')
    stream.write(f'  ALYA:                   {filename:s}\n')
    stream.write('  CODE=                   1\n')
    stream.write('  LIVE_INFO:              SCREEN\n')
    stream.write('  LOG_FILE:               ON\n')
    stream.write('END_RUN_DATA\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PROBLEM_DATA\n')
    stream.write('  TIME_COUPLING:          GLOBAL, PRESCRIBED\n')
    stream.write(f'  TIME_INTERVAL:          {0.0:1.5f} {1.0:1.5f}\n')
    stream.write(f'  TIME_STEP_SIZE=         {0.1:1.5f}\n')
    stream.write('  NUMBER_OF_STEPS=        0\n')
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

    
