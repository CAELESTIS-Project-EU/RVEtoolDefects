import os

basePathList = (
    "/home/ruiz/Data/Dropbox/src/RVE_mesher/data",
)

basePath = None

for currentBasePath in basePathList:

    if os.path.exists(currentBasePath):
        basePath = currentBasePath

if basePath is None:
    for currentBasePath in basePathList:
        print(currentBasePath)
    exit(1)

dataPath=basePath+"/data/"
outputPath=basePath+"/output/"

gmshBin = '/home/ruiz/software/gmsh/gmsh-4.11.0-Linux64/bin/gmsh'
gmsh2alya = '/home/ruiz/Data/Dropbox/msh/gmsh2alya.pl'