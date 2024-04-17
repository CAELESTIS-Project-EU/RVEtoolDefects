#Import libraries
import numpy as num
from numba import jit
import matplotlib.pyplot as plt
#Import local libraries

@jit(cache=True, nopython=True)
def CheckVfAlongRVE(NSquaresY, NSquaresX, a, b, Fibre_pos, R, R1, Vol_f, Xmean, Ymean):
    '''
    Python function to calculate the volume fraction in certain given windows along the RVE

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    NSquaresY : float
            Number of windows along Y direction.
    NSquaresX : float
            Number of windows along X direction.
    a : float
            RVE width.
    b : float
            RVE height.
    Fibre_pos : float32 numpy array of shape(n,6) where n is the number of fibres
            Matrix of coordinates of fibres
    R : float
            Fibre radius of type 1
    R1 : float
            Fibre radius of type 2
    Vol_f : float32 numpy array of shape (NSquaresX,NSquaresY)
            Gives the volume fraction of each window
    Xmean : float32 numpy array of shape (NSquaresX,NSquaresY)
            Gives the X coordinate of each window
    Ymean : float32 numpy array of shape (NSquaresX,NSquaresY)
            Gives the Y coordinate of each window

    Kwargs
    -----
        none

    Return
    --------
    Vol_f : float
        Volume fraction in certain given windows along the RVE

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

    
    YMin=-(b/NSquaresY)
    YMax=YMin+(b/NSquaresY)
    for SqY in range(1, NSquaresY+1):
        XMin=-(a/NSquaresX)
        XMax=XMin+(a/NSquaresX)
        YMin+=(b/NSquaresY)
        YMax+=(b/NSquaresY)
        for SqX in range(1, NSquaresX+1):
            XMin +=(a/NSquaresX)
            XMax +=(a/NSquaresX)
            At=(XMax-XMin)*(YMax-YMin) 
            
            FibInSq=(num.where((Fibre_pos[:,1]>=XMin-Fibre_pos[:,5]) & (Fibre_pos[:,1]<=XMax+Fibre_pos[:,5]) & (Fibre_pos[:,2]>=YMin-Fibre_pos[:,5]) & (Fibre_pos[:,2]<=YMax+Fibre_pos[:,5]))[0])+1
            N1_s=num.sum((Fibre_pos[FibInSq-1,4]==0) & (Fibre_pos[FibInSq-1,1]>XMin+Fibre_pos[FibInSq-1,5]) & (Fibre_pos[FibInSq-1,1]<XMax-Fibre_pos[FibInSq-1,5]) & (Fibre_pos[FibInSq-1,2]>YMin+Fibre_pos[FibInSq-1,5]) & (Fibre_pos[FibInSq-1,2]<YMax-Fibre_pos[FibInSq-1,5]))
            N2_s=num.sum((Fibre_pos[FibInSq-1,4]==1) & (Fibre_pos[FibInSq-1,1]>XMin+Fibre_pos[FibInSq-1,5]) & (Fibre_pos[FibInSq-1,1]<XMax-Fibre_pos[FibInSq-1,5]) & (Fibre_pos[FibInSq-1,2]>YMin+Fibre_pos[FibInSq-1,5]) & (Fibre_pos[FibInSq-1,2]<YMax-Fibre_pos[FibInSq-1,5]))
            N1_h=num.sum((Fibre_pos[FibInSq-1,4]==0) & ((Fibre_pos[FibInSq-1,1]<XMin+Fibre_pos[FibInSq-1,5]) | (Fibre_pos[FibInSq-1,1]>XMax-Fibre_pos[FibInSq-1,5]) | (Fibre_pos[FibInSq-1,2]<YMin+Fibre_pos[FibInSq-1,5]) | (Fibre_pos[FibInSq-1,2]>YMax-Fibre_pos[FibInSq-1,5])))
            N2_h=num.sum((Fibre_pos[FibInSq-1,4]==1) & ((Fibre_pos[FibInSq-1,1]<XMin+Fibre_pos[FibInSq-1,5]) | (Fibre_pos[FibInSq-1,1]>XMax-Fibre_pos[FibInSq-1,5]) | (Fibre_pos[FibInSq-1,2]<YMin+Fibre_pos[FibInSq-1,5]) | (Fibre_pos[FibInSq-1,2]>YMax-Fibre_pos[FibInSq-1,5])))
            Vol_f[SqX-1,SqY-1]=((N1_s*num.pi*R**2)+(N2_s*num.pi*R1**2)+(N1_h*0.5*num.pi*R**2)+(N2_h*0.5*num.pi*R1**2))/At
            Xmean[SqX-1,SqY-1]=XMin+((XMax-XMin)/2.0)
            Ymean[SqX-1,SqY-1]=YMin+((YMax-YMin)/2.0)
            
    return(Vol_f)
    
def PlotVfAlongRVE(Vol_f,NSquaresY, Xmean, Ymean,SimNumb):
    '''
    Python function to plot the volume fraction in certain given windows along the RVE
    
    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia
    
    Args
    -----
    Vol_f : float32 numpy array of shape (NSquaresX,NSquaresY)
            Gives the volume fraction of each window
    NSquaresY : float
            Number of windows along Y direction
    Xmean : float32 numpy array of shape (NSquaresX,NSquaresY)
            Gives the X coordinate of each window
    Ymean : float32 numpy array of shape (NSquaresX,NSquaresY)
            Gives the Y coordinate of each window
    SimNumb : integer
            Current fibre distribution number

    Kwargs
    -----
        none

    Return
    --------
    fig : pdf
        Save a pdf file with a graph to check the volume fraction

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

    plt.ioff()
    plt.rcParams['xtick.labelsize'] = 30
    plt.rcParams['ytick.labelsize'] = 30
    plt.rcParams['figure.figsize'] = [10, 10]
    
    plt.figure(num=1)
    for SqY in range(1, NSquaresY+1):
        plt.plot(Xmean[:,SqY-1], Vol_f[:,SqY-1], Color=(num.random.uniform(0,1), num.random.uniform(0,1), num.random.uniform(0,1)),label='Y position='+str(Ymean[0,SqY-1])+' [mm]')
   
    plt.xlabel('X dimension', fontsize=30)
    plt.ylabel('Volume fraction', fontsize=30)
    plt.legend(loc='best', numpoints=1, ncol=1, fontsize=10)
    plt.savefig('VolumeFractionVariation_'+str(SimNumb)+'.pdf', bbox_inches='tight')
    plt.close(1)   