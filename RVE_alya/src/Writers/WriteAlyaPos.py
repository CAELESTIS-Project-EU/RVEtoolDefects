def writeAlyaPos(file, ):
    """ Alya caseName.post.alyadat file
    """
    
    stream = open(file, 'w')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('DATA\n')
    stream.write('  FORMAT:                   ENSIGHT\n')
    stream.write('  MARK_ELEMENTS:            TYPE\n')
    stream.write('  ELIMINATE_BOUNDARY_NODES: YES\n')
    stream.write('  MULTIPLE_FILE:            OFF\n')
    stream.write('  BOUNDARY:                 ON\n')
    stream.write('  SUBDOMAINS, ALL\n')
    stream.write('  END_SUBDOMAINS\n')
    stream.write('$  SUBDOMAINS\n')
    stream.write('$     1\n')
    stream.write('$  END_SUBDOMAINS\n')
    stream.write('$  ONLY_STEP\n')
    stream.write('$      1\n')
    stream.write('$  END_ONLY_STEP\n')
    stream.write('END_DATA\n')
    stream.write('$-------------------------------------------------------------------\n')

    stream.close()

    
