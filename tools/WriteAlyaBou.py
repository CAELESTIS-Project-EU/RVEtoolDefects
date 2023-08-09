
def writeAlyaBou(path, fileName, blist):
    """
    Write Alya boundary file
    """
    fo = open(path+fileName+".bou.dat","w")
    fo.write("BOUNDARIES, ELEMENTS\n")
    iboun = 0
    for i in range(len(blist)):
        b = blist[i]
        for i in range(len(b)):
            iboun += 1
            ib = b[i]
            if len(ib) == 4:
                # TRI03
                fo.write("{0} {1} {2} {3} {4}\n".format(iboun,ib[0],ib[1],ib[2],ib[3]))
            elif len(ib) == 5:
                # QUA04
                fo.write("{0} {1} {2} {3} {4} {5}\n".format(iboun,ib[0],ib[1],ib[2],ib[3],ib[4]))
    fo.write("END_BOUNDARIES\n")
    fo.close()
