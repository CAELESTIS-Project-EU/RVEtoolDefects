import pathlib
path = pathlib.Path(__file__).parent.resolve()

import sys
sys.path.append(path)

from Readers.ReadAlyaMat import readAlyaMat
from Readers.ReadAlyaCha import readAlyaCha

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

def run(file):

    verbosityPrint('Writing Alya files...')
    writeAlyaDat(f'{outputPath}{file}.dat',file)
    writeAlyaKer(f'{outputPath}{file}.ker.dat')
    writeAlyaPos(f'{outputPath}{file}.post.alyadat')
    
    nOfMaterials = readAlyaMat(f'{outputPath}{file}.mat.dat')

    kfl_coh = False
    if os.path.exists(f'{outputPath}{file}.cha.dat'):
        kfl_coh = readAlyaCha(f'{outputPath}{file}.cha.dat')

    writeAlyaSld(f'{outputPath}{file}.sld.dat',file,'STATIC',kfl_coh,nOfMaterials)
    
if __name__ == '__main__':

    #case = 'oneFibre'
    case = 'RVE_Test_1'
    #case = 'RVE_1x1_with_voids_1'

    basePath = f'{path}/../..'
    dataPath = f'{basePath}/RVE_gen/data'
    outputPath = f'{path}/../../output/'+case+'/'
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        
    run(case)
