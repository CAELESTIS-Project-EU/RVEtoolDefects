import pathlib
path = pathlib.Path(__file__).parent.resolve()

import sys
sys.path.append(path)

from Writers.WriteAlyaDat import writeAlyaDat
from Writers.WriteAlyaKer import writeAlyaKer
from Writers.WriteAlyaSld import writeAlyaSld
from Writers.WriteAlyaPos import writeAlyaPos

import numpy
import os

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass

def run(file, generateCohesiveElements):

    verbosityPrint('Writing Alya files...')
    writeAlyaDat(f'{outputPath}{file}.dat',file)
    writeAlyaKer(f'{outputPath}{file}.ker.dat')
    writeAlyaSld(f'{outputPath}{file}.sld.dat',file,0)
    writeAlyaPos(f'{outputPath}{file}.post.alyadat')
    
if __name__ == '__main__':

#    case = 'oneFibre'
#generateCohesiveElements = False
    case = 'RVE_Test_1'
    generateCohesiveElements = False

    basePath = f'{path}/../data'
    dataPath = f'{basePath}/data'
    outputPath = f'{path}/../../output/'+case+'/'
    print(outputPath)
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        
    run(case,generateCohesiveElements)
