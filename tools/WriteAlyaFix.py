
def writeAlyaFix(path, fileName, blist):
    """
    Write Alya fixity file
    """
    fo = open(path+fileName+".fix.dat","w")
    fo.write("ON_BOUNDARIES\n")
    iboun = 0
    icode = 0
    for i in range(len(blist)):
        b = blist[i]
        icode += 1
        for i in range(len(b)):
            iboun += 1
            fo.write("{0} {1}\n".format(iboun,icode))
    fo.write("END_ON_BOUNDARIES\n")
    fo.close()
