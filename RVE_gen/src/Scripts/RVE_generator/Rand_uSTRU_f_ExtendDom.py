# Import libraries
import numpy as num
from numba import jit
# Import local libraries


@jit(cache=True, nopython=True)
def ExtendDomain(R, N_fibre, delta_width,MultipleSizeWidth,MultipleSizeheight,delta_height, Fibre_pos):
    '''
    Python function to create a larger RVE by shifting a smaller one, i.e. a RVE
    is multiplied many times to obtain a new one.

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    R : float
            Fibre radius
    N_fibre : integer
            Total number of fibres
    delta_width : float
            Width of the RVE divided by the fibre radius
    MultipleSizeWidth : integer
            Number of times to shift the RVE in X direction
    MultipleSizeheight : integer
            Number of times to shift the RVE in Y direction
    delta_height : float
            Height of the RVE divided by the fibre radius
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibre coordinates

    Kwargs
    -----
        none

    Return
    --------
    Fibre_posNew : numpy array of shape (n,6) where n is the number of fibres in the RVE
            Equivalent Fibre_pos array but containing the coordinates
            of the final RVE
    Examples
    -----
        none

    Raises
    -----
        none

    Note
    -----
        none

    Program called by
    -----
        File "Rand_uSTRU_f_Loop.py"

    Program calls
    -----
        none
    '''

    print('Extending domain')
    IncrX=delta_width*R
    IncrY=delta_height*R
    Xoff=-IncrX
    Fibre_posNew=num.zeros((1,6),dtype=num.float32)
    Fibre_posTemp=num.zeros((N_fibre, 6),dtype=num.float32)
    for row in range(1, MultipleSizeWidth+1):
        Xoff +=IncrX
        Yoff =-IncrY
        for col in range(1, MultipleSizeheight+1):
            Yoff +=IncrY
            Fibre_posTemp[:,:]=Fibre_pos[:,:]
            Fibre_posTemp[:,1] +=Xoff
            Fibre_posTemp[:,2] +=Yoff
            Fibre_posNew=num.concatenate((Fibre_posNew, Fibre_posTemp),0)
    Fibre_posNew=Fibre_posNew[1:,:] #Delete first row
    return(Fibre_posNew)

@jit(cache=True, nopython=True)
def AdjustArea(Fibre_pos2):
    '''
    Python function to enforce the correct area for each fibre after shifting
    and multiplying the RVE

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    Fibre_pos2 : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibre coordinates

    Kwargs
    -----
        none

    Return
    --------
    IndexDel : numpy array of shape (n)
            Indices of fibres to delete since they are repeated

    Examples
    -----
        none

    Raises
    -----
        none

    Note
    -----
        none

    Program called by
    -----
        File "Rand_uSTRU_f_Loop.py"

    Program calls
    -----
        none
    '''

    print('Adjusting the area of each fibre and deleting repeated fibres')
    IndexDel=num.zeros((Fibre_pos2.shape[0]),dtype=num.float32)
    
    for fib in range(1,Fibre_pos2.shape[0]+1):
        Rep=(num.where(((num.abs(Fibre_pos2[:,1] - Fibre_pos2[fib-1,1]) <= (1e-08 + 1e-05 * num.abs(Fibre_pos2[fib-1,1]))) == 1) & ((num.abs(Fibre_pos2[:,2] - Fibre_pos2[fib-1,2]) <= (1e-08 + 1e-05 * num.abs(Fibre_pos2[fib-1,2]))) == 1))[0])+1
        if Rep.shape[0]==2: #Then we either have two halves united into one, or 2 quarters united into a half
            if (IndexDel[Rep[0]-1] != Rep[0]) and (IndexDel[Rep[1]-1] != Rep[1]):
                if Fibre_pos2[Rep[0]-1,3]==2.0: #Then two halfs are united into a single fibre
                    Fibre_pos2[Rep[0]-1,3]=0.0 #Set its indicator to the proper value
                    IndexDel[Rep[1]-1] = Rep[1]
                elif Fibre_pos2[Rep[0]-1,3]==4.0: 
                    Fibre_pos2[Rep[0]-1,3]=2.0 #Set its indicator to the proper value
                    IndexDel[Rep[1]-1] = Rep[1]
        elif Rep.shape[0]==4: #Then we have 4 quarters united into a single fibre
            if (IndexDel[Rep[0]-1] != Rep[0]) and (IndexDel[Rep[1]-1] != Rep[1]) and (IndexDel[Rep[2]-1] != Rep[2]) and (IndexDel[Rep[3]-1] != Rep[3]):
                Fibre_pos2[Rep[0]-1,3]=0.0 #Set indicator
                IndexDel[Rep[1]-1] = Rep[1]
                IndexDel[Rep[2]-1] = Rep[2]
                IndexDel[Rep[3]-1] = Rep[3]
   
    return(IndexDel)
