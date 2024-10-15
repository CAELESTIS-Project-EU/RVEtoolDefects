def writeAlyaDom(file, filename, ndime, nmate):
    """ Alya caseName.dom.dat file
    """
    
    stream = open(file, 'w')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('DIMENSIONS\n')
    #stream.write('  NODAL_POINTS      = %d\n' % npoin)
    #stream.write('  ELEMENTS          = %d\n' % nelem)
    #stream.write('  BOUNDARIES        = %d\n' % nboun)
    stream.write('  INCLUDE ../msh/%s.dims.dat\n' % filename)
    stream.write('  SPACE_DIMENSIONS  = %d\n' % ndime)
    if ndime == 2:
        stream.write('  TYPES_OF_ELEMENTS = QUA04\n')
    elif ndime == 3:
        stream.write('  TYPES_OF_ELEMENTS = HEX08\n')
    stream.write('  MATERIALS         = %d\n' % nmate)
    stream.write('  FIELDS            = 1\n')
    stream.write('    FIELD= 1, DIMENSIONS= %d, ELEMENTS\n' % (ndime*ndime))
    stream.write('  END_FIELDS\n')
    stream.write('END_DIMENSIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('STRATEGY\n')
    stream.write('  INTEGRATION_RULE:                OPEN\n')
    stream.write('  DOMAIN_INTEGRATION_POINTS=       0\n')
    stream.write('  SCALE:                           XSCAL= 1.0 YSCAL= 1.0 ZSCAL= 1.0\n')
    stream.write('  TRANSLATION:                     XTRAN= 0.0 YTRAN= 0.0 ZTRAN= 0.0\n')
    stream.write('  EXTRAPOLATE_BOUNDARY_CONDITIONS: ON\n')
    stream.write('  BOUNDARY_ELEMENT:                OFF\n')
    stream.write('END_STRATEGY\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('GEOMETRY\n')
    stream.write('  INCLUDE ../msh/%s.geo.dat\n' % filename)
    stream.write('  INCLUDE ../msh/%s.mat.dat\n' % filename)
    stream.write('  INCLUDE ../msh/%s.per.dat\n' % filename)
    stream.write('END_GEOMETRY\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('SETS\n')
    stream.write('  INCLUDE ../msh/%s.set.dat\n' % filename)
    stream.write('END_SETS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('BOUNDARY_CONDITIONS\n')
    stream.write('  INCLUDE ../msh/%s.fix.bou\n' % filename)
    stream.write('END_BOUNDARY_CONDITIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('FIELDS\n')
    stream.write('  INCLUDE ../msh/%s.fie.dat\n' % filename)
    stream.write('END_FIELDS\n')
    stream.write('$-------------------------------------------------------------------\n')
    
    stream.close()

    
