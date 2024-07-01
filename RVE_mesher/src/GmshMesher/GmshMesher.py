import sys
import os
sys.path.append('..')

import numpy

def createRectangle(gmshScript, a, b):
    gmshScript.write(f'Rectangle(1) ={{0, 0, 0, {a}, {b}}};\n\n')

def createCircle(gmshScript, i, x, y, r):
    gmshScript.write(f'Disk({i}) = {{{x}, {y}, 0, {r} }};\n\n')

def createGeometry(gmshScript, nOfFibres, a, b):

    gmshScript.write(f'v() = BooleanFragments{{ Surface{{1}}; Delete; }}{{ Surface{{2:{1+nOfFibres}}}; Delete; }};\n\n')
    # gmshScript.write(f'Rectangle(0) ={{0, 0, 0, {a}, {b}}};\n\n')
    # gmshScript.write(f'v() = BooleanIntersection{{ Surface{{0}}; Delete; }}{{ Surface{{:}}; Delete; }};\n\n')

def setMesher(gmshScript, h):
    gmshScript.write(f'MeshSize{{ PointsOf{{ Surface{{:}}; }} }} = {h};\n\n')

    # TODO
    #gmshScript.write(f'Mesh.Algorithm=8;\n')
    #gmshScript.write(f'Mesh 2;\n')
    #gmshScript.write(f'Mesh.RecombinationAlgorithm=0;\n')
    #gmshScript.write(f'RecombineMesh;\n')
    #gmshScript.write(f'Mesh.SubdivisionAlgorithm=1;\n')
    #gmshScript.write(f'RefineMesh;\n')
    #gmshScript.write(f'OptimizeMesh "Laplace2D";\n\n')

    gmshScript.write(f'Recombine Surface "*";\n')
    gmshScript.write(f'Mesh.Algorithm=8;               // Frontal-Delaunay for quads\n')
    gmshScript.write(f'Mesh.RecombinationAlgorithm=3;  // Simple (2) Blossom full quad (3)\n')
    gmshScript.write(f'OptimizeMesh "Laplace2D";\n\n')
    
def setoutputFile(gmshScript, mshFile):
    gmshScript.write('Mesh.MshFileVersion = 2.2;\n')

    gmshScript.write(f'Save "{os.path.split(mshFile)[-1]}";\n')

def gmshMesher(RVE, h, scriptFile, mshFile):

    gmshScript = open(scriptFile, 'w')

    gmshScript.write('SetFactory("OpenCASCADE");\n')

    a = RVE['a']
    b = RVE['b']

    # print(a, b)

    createRectangle(gmshScript, a, b)

    fibres = RVE['Fibre_pos']

    nOfFibres = fibres.shape[0]

    for iFibre in range(nOfFibres):
        x = fibres[iFibre, 1]
        y = fibres[iFibre, 2]
        r = fibres[iFibre, -1]

        createCircle(gmshScript, iFibre+2, x, y, r)

    createGeometry(gmshScript, nOfFibres, a, b)

    setMesher(gmshScript, h)

    setoutputFile(gmshScript, mshFile)

    gmshScript.close()
