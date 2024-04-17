""" 
-------------------------------------------------------------------------------
This Python file "Rand_uSTRU_f_Thi_Heur.py" contains a function
used by file "Rand_uSTRU_Main_vx.x.py".

The function in this file removes some fibres according to their position on
the edges.

Information regarding to each function in this file can be found at the
beginning of each function.

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
Jose Manuel Guerrero Garcia
josemanuel.guerrero@udg.edu 
AMADE research group, University of Girona (UdG), Girona, Catalonia, Spain
-------------------------------------------------------------------------------

"""

#Import libraries:
import numpy as num
from numba import jit
#import time
#time.process_time()
#import sys

@jit(cache=True, nopython=True)
def Rand_Per_uSTRU_ThirdHeur(N_fibre,Fibre_pos,a,b,Vol_fibre,Vol_fibre_1,Vol_fibre_2,A_total,A_1_fibre,A_2_fibre,Vec_mem,N_fibre_real,S_base):
    """
    -------------------------------------------------------------------------------
    This Python function named 'Rand_Per_uSTRU_ThirdHeur' removes the fibres at
    edges whose coordinate is above a certain limit.
    
    Author
    -------------------------------------------------------------------------------
    Jose Manuel Guerrero Garcia
    josemanuel.guerrero@udg.edu 
    AMADE research group, University of Girona (UdG), Girona, Catalonia, Spain
    
    Input parameters
    -------------------------------------------------------------------------------  
    N_fibre : integer, total number of fibres
    Fibre_pos : float32 numpy array of shape (N_fibre,6), corresponds to the
                matrix of coordinates
    a : float, total RVE width
    b : float, total RVE height
    Vol_fibre : float, overall fibre volume fraction
    Vol_fibre_1 : float, fibre 1 volume fraction
    Vol_fibre_2 : float, fibre 2 volume fraction
    A_total : float, total area of the RVE
    A_1_fibre : float, area of a fibre type 1
    A_2_fibre : float, area of a fibre type 2
    Vec_mem : float32 numpy array of shape (N_fibre, 3), used in 1st heuristic
    N_fibre_real : integer, total number of complete fibres
    S_base : float, average of element size for third heuristic.
    
    Returns
    -------------------------------------------------------------------------------
    Vol_fibre,Vol_fibre_1,Vol_fibre_2,Fibre_pos,Vec_mem,N_fibre,N_fibre_real
    
    Program called by
    -------------------------------------------------------------------------------
    This function is called by file "Rand_uSTRU_f_HardCoreModel.py".
    
    Program calls
    -------------------------------------------------------------------------------
    This function does not call any other function.
    
    Change log
    -------------------------------------------------------------------------------
    2016/05/xx - First version
    2018/01-xx/ - Added generation of interlayer and intralayer hybrids
    2018/11/21 - added the variable fibre radius
    -------------------------------------------------------------------------------
    """
    GO = 0 #Flag for stopping the heuristic
    Lim = 0.90 #Limit value multiplier for the heuristic
    while GO==0:
        GO = 1
        for i in range(1,N_fibre+1): #Loop on fibres
            if i>=N_fibre:
                break
            
            if Fibre_pos[i-1,4-1] == 2: #If fibre at an edge
                X_TMP = Fibre_pos[i-1,2-1] #Get its coordinates
                Y_TMP = Fibre_pos[i-1,3-1]
                
                #Now check if the coordinates are larger or smaller than a certain limit pondered by Lim. If so, delete the fibre and its pair
                if X_TMP < -Lim*Fibre_pos[i-1,6-1] or (X_TMP > Lim*Fibre_pos[i-1,6-1] and X_TMP < Fibre_pos[i-1,6-1]) or \
                        Y_TMP < -Lim*Fibre_pos[i-1,6-1] or (Y_TMP > Lim*Fibre_pos[i-1,6-1] and Y_TMP < Fibre_pos[i-1,6-1]) or \
                        X_TMP > a+Lim*Fibre_pos[i-1,6-1] or (X_TMP > a-Fibre_pos[i-1,6-1] and X_TMP < a-Lim*Fibre_pos[i-1,6-1]) or \
                        Y_TMP > b+Lim*Fibre_pos[i-1,6-1] or (Y_TMP > b-Fibre_pos[i-1,6-1] and Y_TMP < b-Lim*Fibre_pos[i-1,6-1]):
                    if Fibre_pos[i-1,5-1]==0:
                        Vol_fibre -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                        Vol_fibre_1 -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                    else:
                        Vol_fibre -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                        Vol_fibre_2 -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                    
                    IndexFibre=num.concatenate((num.arange(0,(i-1)),num.arange(i+1,Fibre_pos.shape[0])))
                    indexMem=num.concatenate((num.arange(0,(i-1)),num.arange(i+1,Vec_mem.shape[0])))
                    Fibre_pos=Fibre_pos[IndexFibre,:]
                    Vec_mem=Vec_mem[indexMem,:]
                    N_fibre -= 2
                    N_fibre_real -= 1
                    GO = 0 #re-set the variable to continue the while loop
                    break #And break the for loop (it is re-started again)

            elif Fibre_pos[i-1,4-1] == 4: #If fibre is located in a vertex
                X_TMP = Fibre_pos[i-1,2-1] #Get all coordinates again
                Y_TMP = Fibre_pos[i-1,3-1]
                #However, if none of the specified conditions meet, then we check this another similar criteria:
                dist_tmp1 = num.sqrt(X_TMP**2+Y_TMP**2)
                dist_tmp2 = num.sqrt((a-X_TMP)**2+Y_TMP**2)
                dist_tmp3 = num.sqrt((a-X_TMP)**2+(b-Y_TMP)**2)
                dist_tmp4 = num.sqrt(X_TMP**2+(b-Y_TMP)**2)
                
                #Check the coordiantes again according to the specified limits. If true, delete the fibre and associated pairs
                if (X_TMP>Lim*Fibre_pos[i-1,6-1] and X_TMP<Fibre_pos[i-1,6-1] and Y_TMP<Fibre_pos[i-1,6-1]) or \
                        (Y_TMP>Lim*Fibre_pos[i-1,6-1] and Y_TMP<Fibre_pos[i-1,6-1] and X_TMP<Fibre_pos[i-1,6-1]) or \
                        (X_TMP>a-Fibre_pos[i-1,6-1] and X_TMP<a-Lim*Fibre_pos[i-1,6-1] and Y_TMP<Fibre_pos[i-1,6-1]) or \
                        (Y_TMP<Fibre_pos[i-1,6-1] and Y_TMP>Lim*Fibre_pos[i-1,6-1] and X_TMP>a-Fibre_pos[i-1,6-1]) or \
                        (X_TMP>a-Fibre_pos[i-1,6-1] and X_TMP<a-Lim*Fibre_pos[i-1,6-1] and Y_TMP>b-Fibre_pos[i-1,6-1]) or \
                        (Y_TMP>b-Fibre_pos[i-1,6-1] and Y_TMP<b-Lim*Fibre_pos[i-1,6-1] and X_TMP>a-Fibre_pos[i-1,6-1]) or \
                        (X_TMP>Lim*Fibre_pos[i-1,6-1] and X_TMP<Fibre_pos[i-1,6-1] and Y_TMP>b-Fibre_pos[i-1,6-1]) or \
                        (Y_TMP>b-Fibre_pos[i-1,6-1] and Y_TMP<b-Lim*Fibre_pos[i-1,6-1] and X_TMP<Fibre_pos[i-1,6-1]) or \
                        (dist_tmp1 > Fibre_pos[i-1,6-1]-S_base/2 and dist_tmp1 < Fibre_pos[i-1,6-1]+S_base/2) or \
                        (dist_tmp2 > Fibre_pos[i-1,6-1]-S_base/2 and dist_tmp2 < Fibre_pos[i-1,6-1]+S_base/2) or \
                        (dist_tmp3 > Fibre_pos[i-1,6-1]-S_base/2 and dist_tmp3 < Fibre_pos[i-1,6-1]+S_base/2) or \
                        (dist_tmp4 > Fibre_pos[i-1,6-1]-S_base/2 and dist_tmp4 < Fibre_pos[i-1,6-1]+S_base/2):
                
                    if Fibre_pos[i-1,5-1]==0:
                        Vol_fibre -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                        Vol_fibre_1 -=(num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                    else:
                        Vol_fibre -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total
                        Vol_fibre_2 -= (num.pi*Fibre_pos[i-1,6-1]**2)/A_total

                    IndexFibre=num.concatenate((num.arange(0,(i-1)),num.arange(i+3,Fibre_pos.shape[0])))
                    indexMem=num.concatenate((num.arange(0,(i-1)),num.arange(i+3,Vec_mem.shape[0])))
                    Fibre_pos=Fibre_pos[IndexFibre,:]
                    Vec_mem=Vec_mem[indexMem,:]
                    N_fibre -= 4
                    N_fibre_real -= 1
                    GO = 0 #Again break and re-start
                    break

    return(Vol_fibre,Vol_fibre_1,Vol_fibre_2,Fibre_pos,Vec_mem,N_fibre,N_fibre_real)