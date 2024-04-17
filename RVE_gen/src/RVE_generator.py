''' 
-------------------------------------------------------------------------------
This is a Python routine for generating a distribution of fibres.

This program is based on the original generator created in Matlab by:
Antonio Rui Melro - antonio.melro@fe.up.pt
June 2010
Published with ref: A.R. Melro, P.P. Camanho, S.T. Pinho, Generation of random 
distribution of fibres in long-fibre reinforced composites, Composites Science 
and Technology 68 (2008) 2092–2102. doi:10.1016/j.compscitech.2008.03.013.

And extended to hybrid composites by:
Rodrigo Paiva Tavares - em10140@fe.up.pt

Author
-------------------------------------------------------------------------------
Oriol Vallmajó Martín
oriol.vallmajo@udg.edu
AMADE research group, University of Girona (UdG), Girona, Catalonia, Spain
April, 2020

Program called by
-------------------------------------------------------------------------------
This file is not called by any other function.

Program calls
-------------------------------------------------------------------------------
This Python file calls:
    - Rand_uSTRU_f_Loop.py
'''

#Import libraries
import numpy as num
import time
from joblib import Parallel, delayed
import os
#Import local libraries
from Scripts.RVE_generator.Rand_uSTRU_f_Loop import RandGen
from Scripts.Misc import move_files
from Scripts.Misc import remove_files


###############################################################################
# Input Parameters defined by the user
###############################################################################
exec(open(os.path.join(os.path.dirname(__file__), 'Inputs_RVE_generator.py')).read())

Error_V_fibres  = Error_V_fibres_perc / 100.            #Maximum error allowed for the fibres volume content (relative error)
Error_V_voids   = Error_V_voids_perc / 100.             #Maximum error allowed for the voids volume content (relative error)

Summary_file = str(OutputCaseName + '_summary.txt')
with open(Summary_file, 'w') as f:
    f.write('DESCRIPTION OF THE INPUTS \n')
    f.write('Properties regarding the fibres \n')
    f.write('R_fibre [mm]:                  %s\n'       % R_fibre)
    f.write('R_fibre_STDEV [mm]:            %s\n'       % R_fibre_STDEV)
    f.write('Vol_fibre [-]:                 %s\n'       % Vol_fibre)
    f.write('##### \n')
    f.write('Properties regarding the voids \n')
    f.write('R_void [mm]:                   %s\n'       % R_void)
    f.write('R_void_STDEV [mm]:             %s\n'       % R_void_STDEV)
    f.write('Vol_voids [-]:                 %s\n'       % Vol_voids)
    f.write('##### \n')
    f.write('Distances between fibres and voids \n')
    f.write('Dist_fibres [*R_fibre]:        %s\n'       % DISTMIN[0])
    f.write('Dist_fibre_voids [*R_mean]:    %s\n'       % DISTMIN[1])
    f.write('Dist_voids [*R_void]:          %s\n'       % DISTMIN[2])
    f.write('##### \n')
    f.write('Errors allowed for the volume fractions achieved \n')
    f.write('Error_V_fibres [%%]:            %s\n'       % Error_V_fibres_perc)
    f.write('Error_V_voids [%%]:             %s\n'       % Error_V_voids_perc)
    f.write('##### \n')
    f.write('Dimensions of the RVE \n')
    f.write('delta_width [*2*R_fibre]:        %s\n'       % delta_width)
    f.write('Width [mm]:                    %s\n'       % str(delta_width*2*R_fibre))
    f.write('delta_height [*2*R_fibre]:       %s\n'       % delta_height)
    f.write('Height [mm]:                   %s\n'       % str(delta_height*2*R_fibre))
    f.write('###########################################\n')

###############################################################################
#General options
###############################################################################
StartingSim             = 1                             #Starting number for the fibre distribution
num_cores               = 1                             #Number of cpu 'threads' to be used for the parallelization. Each thread will create a different distribution, all working in parallel
Hybrid_type             = 0                             #Type of hybrid to make: 0=fiber-by-fiber (intrayarn), 1=layer-by-layer (interlayer), 2=Bundle-by-bundle (intralayer)
R                       = R_fibre                       #fibre1 average radius
R1                      = R_void                        #fibre2 average radius
R_STDEV                 = R_fibre_STDEV                 #Standard deviation for fibre type 1, used if VariableFibreRadius=1. Must be in the same units of fibre radius in mm
R1_STDEV                = R_void_STDEV                  #Standard deviation for fibre type 2, used if VariableFibreRadius=1. Must be in the same units of fibre radius in mm
if R_STDEV == 0.00000000000000 and R1_STDEV == 0.00000000000000:
    VariableFibreRadius = 0                             #Variable for the algorithm to know if the fibre and void radius are variable in a normal distribution. 0=No, 1=Yes
else:
    VariableFibreRadius = 1                             #Variable for the algorithm to know if the fibre and void radius are variable in a normal distribution. 0=No, 1=Yes
Vol_fibre_req           = Vol_fibre + Vol_voids         #Overall fibre volume we wish to obtain
Fibre_type_1            = Vol_fibre/Vol_fibre_req       #Fibre volume fraction of population 1 over the total fibre volume fraction:
                                                            # (i.e. 0.5 --> half of the overall volume fraction are type 1 fibres, the other half are type 2 fibres)

###############################################################################
#Options for the algorithm to create the RVE
###############################################################################
N_guesses_max           = (50E3)*num.ceil(num.maximum(delta_width/2.,delta_height/2.)/50.0)   #Number of guesses in the random generation of fibre position. Recommended 50E3 for delta_height=50.
                                                                                            # For bigger RVEs, the number of guesses is proportionally increased.
Square_size             = 3*R                       #Initial size of square in Second Heuristic. Now all the dimensions are based only on R.
Square_inc              =(8.5-10*Vol_fibre_req)*R   #Increment to be given to the square size in Second Heuristic. Now all the dimensions are based only on R.
S_base                  = 1.5*2*num.pi/60*R         #Average of element size for third heuristic. NOTE: 3rd heuristic is not used.
inter_option            = 0                         #Model the interlaminar area 0-NO, 1-YES
Sec_heur_inter_intra    = 1                         #For interlayer and intralayer hybrids, it may be of interest not applying the 2nd heuristic to a fibre population that
                                                        # has already reached its desired volume fraction. This option controlls it. 0=Apply it anyways, 1=Do not apply it.

###############################################################################
# Specific options for interlayer hybrids (Hybrid_type=1)
# By default, intrayarn hybrid is selected
###############################################################################
Stacking_sequence=[1,0]                             #Stacking sequence of the interlayer hybrid composite (from bottom of the RVE to top). For each ply,
                                                        # 0=ply with only fibre type 1, 1=ply with only fibre type 2.
Stacking_sequence_thickness=[0.0125,0.025]          #Corresponding thickness of each ply (from bottom to top). Must be consistent with the RVE height.

###############################################################################
# Specific options for intralayer hybrids (Hybrid_type=2)
# By default, intrayarn hybrid is selected
###############################################################################
NbundlesRa=16               #If Hybrid_type=2: Number of bundles to divide the composite (in each direction) for a bundle-by-bundle (intralayer) hybrid.
                                # Total number of bundles is then NbundlesRa*NbundlesRa.
FirstFibreTypeRa=0          #Which is the first fibre type (starting from the top-left side of the RVE). 0=Decided automatically by python, 1=Fibre type 1, 2=Fibre type 2.
#The algorithm assumes that the bundles are all of the same thickness, and always alternated. Thus the width of a bundle is simply the RVE width divided by NbundlesRa, and the height of a bundle is the RVE height divided by NbundlesRa.


###############################################################################
#Options under development
###############################################################################
MatRichRegionX  =0          #UNDER DEVELOPMENT, USE 0. 0=No matrix rich region next to the boundary of the RVE in X direction, 1=Yes.
MatRichRegionY  =0          #UNDER DEVELOPMENT, USE 0. 0=No matrix rich region next to the boundary of the RVE in Y direction, 1=Yes.
WidthMatRich    =2*R1       #UNDER DEVELOPMENT. If MatRichRegionX=1, Thickness of the matrix rich region on X direction. Must be bigger than twice the fibre radius
HeightMatRich   =2*R1       #UNDER DEVELOPMENT. If MatRichRegionY=1, Thickness of the matrix rich region on Y direction. Must be bigger than twice the fibre radius


###########################################################################
# End of input data, script start                                         #
###########################################################################
#Create some variables and start timing
a = delta_width*2*R           #RVE width
b = delta_height*2*R          #RVE height (aka thickness direction)

#Parallelization of the code
inputs = num.arange(StartingSim,NumTimes+1) # This is a vector of 'processes' (with each process being a distribution to generate) to be run each one by a cpu thread

kfl_plot = True

if __name__ == '__main__': #Necessary for windows o.s.
    
    startTime = time.time() #Start program timing

    Fibre_pos = Parallel(n_jobs=num_cores)(delayed(RandGen)(i,Hybrid_type,Max_fibres,R,Vol_fibre_req,
        Error_V_fibres, Error_V_voids, DISTMIN, cluster_fibres, N_guesses_max,
        N_cycles_max, N_change, Square_size, Square_inc, inter_option, a, b, S_base, Fibre_type_1, R1,
        CreateLargerRatio, MultipleSizeWidth, MultipleSizeheight, NbundlesRa,
        MatRichRegionX,MatRichRegionY,WidthMatRich,HeightMatRich,
        Check_Vf,NSquaresY,NSquaresX,OutputCaseName,FirstFibreTypeRa,VariableFibreRadius,R_STDEV,R1_STDEV,
        Stacking_sequence,Stacking_sequence_thickness,Sec_heur_inter_intra,kfl_plot) for i in inputs)

    EndTime=time.time() #End timing and finish
    
    print('Total computational time (min)', ((EndTime-startTime)/60))

   # for j in range(NumTimes):
   #     #Move the files in the correct folder to run the simulation
   #     #Where to move it
   #     dir_path = os.getcwd()
   #     # Files to move to a new folder with the name of the Project
   #     npz_file = [OutputCaseName + '_' + str(j+1) + '.npz', 'cut']
   #     pdf_file = [OutputCaseName + '_' + str(j+1) + '_FibrePlot.pdf', 'cut']
   #     txt_file = [OutputCaseName + '_' + str(j+1) + '_summary.txt', 'cut']
   #     place_to_move = OutputCaseName + '/' + str(j+1) + '/RVE_description'
   #     list_of_files = [npz_file, pdf_file, txt_file]
   #     move_files(dir_path, dir_path, place_to_move, list_of_files)
   #
   # remove_files(dir_path, list_of_files=[str(OutputCaseName + '_summary.txt')])
   #
   # Move all the project to the PROJECT's directory
   # move_files(dir_path, dir_path, 'PROJECTS', [[OutputCaseName, 'cut']])
