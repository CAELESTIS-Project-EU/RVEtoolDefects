#Import libraries
import numpy as num
import matplotlib
import matplotlib.pyplot as plt
import time
#Import local libraries
from .Rand_uSTRU_f_ExtendDom import ExtendDomain, AdjustArea
from .Rand_uSTRU_f_HardCoreModel import Rand_PER_uSTRU_GEN_3D_LayerBundle
from .Rand_uSTRU_f_overlap import f_area_voids_overlap
from .Rand_uSTRU_f_Plot_Fibres import circles
from .Rand_uSTRU_f_CheckVfAlongRVE import CheckVfAlongRVE,PlotVfAlongRVE


def RandGen(SimNumb, Hybrid_type,Max_fibres,R,Vol_fibre_req, Error_V_fibres, Error_V_voids, DISTMIN, cluster_fibres, N_guesses_max,N_cycles_max,
                N_change, Square_size, Square_inc, inter_option, a, b, S_base, Fibre_type_1, R1,
                CreateLargerRatio, MultipleSizeWidth, MultipleSizeheight, NbundlesRa,
                MatRichRegionX,MatRichRegionY,WidthMatRich,HeightMatRich,
                Check_Vf,NSquaresY,NSquaresX,OutputCaseName,FirstFibreTypeRa,VariableFibreRadius,R_STDEV,R1_STDEV,
                Stacking_sequence,Stacking_sequence_thickness,Sec_heur_inter_intra,kfl_plot):

    '''
    The Python function generates a RVE with a random distribution of fibres as many
    times as requested by the user.

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    SimNumb : float
            Current distribution number
    Hybrid_type : integer
            Determines the hybrid type to generate (intrayarn, interlayer or intralayer)
    Max_fibres : integer
            Determines the maximum number of possible fibres in the RVE
    R : float
            Average radius of fibre type 1
    Vol_fibre_req : float
            Overall fibre volume fraction requested
    Error_V_fibres : float
            Maximum error allowed for the fibre volume content
    Error_V_voids : float
            Maximum error allowed for the voids volume content
    DISTMIN : array [0,3]
            Minimum distance multiplier between: [fibres, fibre-void, vois]
    cluster_fibres : numba dict
            Dictionary with the position where there must be a fiber cluster and the minimum position between them
    N_guesses_max : float
            Maximum number of guesses in the hard-core model
    N_cycles_max : integer
            Maximum number of cycles run by the program for reaching the requested fibre
            volume fraction
    N_change : integer
            Number of cycles before changing criteria on 1st heuristic
    Square_size : float
            Initial size of the square for 2nd heuristic
    Square_inc : float
            Square size increment for 2nd heuristic
    inter_option : integer
            Determines if the interlaminar area is modelled
    a : float
            Width of the generated RVE
    b : float
            Height of the generated RVE
    S_base : float
            Average of element size for third heuristic.
    Fibre_type_1 : float
            Amount of type 1 fibres in respect to the overal fibre volume fraction
    R1 : float
            Average radius of fibre type 2
    CreateLargerRatio : integer
            Option to multiply an RVE and make it bigger by repeating a smaller generated RVE
    MultipleSizeWidth : integer
            The RVE is copied "MultipleSize" times in X direction to have a larger RVE
    MultipleSizeheight : integer
            The RVE is copied "MultipleSize" times in Y direction to have a larger RVE
    NbundlesRa : integer
            Number of bundles for an intralayer hybrid
    MatRichRegionX : float,
            Defines a region where there are no fibres in X direction close to the edges of the RVE
    MatRichRegionY : float
            Defines a region where there are no fibres in Y direction close to the edges of the RVE
    WidthMatRich : integer
            Whether to use the MatRichRegionX region
    HeightMatRich : integer
            Whether to use the MatRichRegionY region
    Check_Vf : integer
            Option to plot the variance of the fibre volume fraction along the RVE
    NSquaresY : integer
            Points at which to create an area to check volume fraction in Y direction
    NSquaresX : integer
            Points at which to create an area to check volume fraction in X direction
    OutputCaseName : string
            Name of output file
    FirstFibreTypeRa : integer
            Determines the fibre type of the first bundle or layer in an interlayer
            or intralayer hybrid
    VariableFibreRadius : integer
            Allows to model the statistical variation of the fibre radius using a
            normal distribution
    R_STDEV : float
            Standard deviation of the fibre radius of type 1 if VariableFibreRadius
            is used
    R1_STDEV : float
            Standard deviation of the fibre radius of type 2 if VariableFibreRadius
            is used
    Stacking_sequence : numpy array of shape (,x) where x is the number of plies
            It contains the stacking sequence of an interlayer hybrid composite
            to generate
    Stacking_sequence_thickness: numpy array of shape (,x)
            It contains the thickness of each ply in interlayer hybrids
    Sec_heur_inter_intra : integer
            Determines whether the 2nd heuristic is applied when the volum
            fraction is already reached

    Kwargs
    -----
        none

    Return
    --------
        fig : pdf
            Save a pdf file with a graph to check the RVE created
        matrix : npz
            numpy compressed file (.npz) with the fibres coordinates

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
        File "Rand_uSTRU_Main_XXXXX.py"

    Program calls
    -----
        File "Rand_uSTRU_f_ExtendDom.py", "Rand_uSTRU_f_HardCoreModel.py", "Rand_uSTRU_f_Plot_Fibres.py",
        "Rand_uSTRU_f_CheckVfAlongRVE.py"
    '''

    time.process_time() #Start timing

    #
    ###########################################################################
    # Determination of Auxiliary Parameters                                   #
    ###########################################################################
    #
    Stacking_sequence=num.array(Stacking_sequence, dtype=num.int64) #Convert to array
    Stacking_sequence_thickness=num.array(Stacking_sequence_thickness, dtype=num.float32) #Convert to array

    if VariableFibreRadius==0: #Enforce no standard deviation if this option is not used
        R_STDEV=0.0
        R1_STDEV=0.0

    if Stacking_sequence[0]==0:
        IDlayerVectFt0=Stacking_sequence #Vector used for 2nd heuristic when an interlayer hybrid is generated. This stores the layer at which each fibre of type 1 belongs to.
        IDlayerVectFt1=num.zeros(IDlayerVectFt0.shape[0], dtype=num.int64)
        Layers_type1=num.where(Stacking_sequence[:]==0)[0]
        Layers_type2=num.where(Stacking_sequence[:]==1)[0]
        IDlayerVectFt1[Layers_type1]=1
        IDlayerVectFt1[Layers_type2]=0
    else:
        IDlayerVectFt1=Stacking_sequence #Vector used for 2nd heuristic when an interlayer hybrid is generated. This stores the layer at which each fibre of type 1 belongs to.
        IDlayerVectFt0=num.zeros(IDlayerVectFt1.shape[0], dtype=num.int64)
        Layers_type1=num.where(Stacking_sequence[:]==0)[0]
        Layers_type2=num.where(Stacking_sequence[:]==1)[0]
        IDlayerVectFt0[Layers_type1]=1
        IDlayerVectFt0[Layers_type2]=0

    #These are vectors for intralayer hybrids, which are used to determine what fibre type goes in each bundle
    First_row_types_ft0=num.tile([0,1],NbundlesRa**2)
    Next_row_types_ft0=num.tile([1,0],NbundlesRa**2)
    First_row_types_ft1=num.tile([1,0],NbundlesRa**2)
    Next_row_types_ft1=num.tile([0,1],NbundlesRa**2)

    #
    ###########################################################################
    # Call RVE generator                                                      #
    ###########################################################################
    #    
    N_fibre =0 # Current number of fibres
    status = 0 # Flag to stop, 0=continues the generation, 1=stops
    while status == 0: # If status=1, the RVE complies with the volumes requested, and hence, here it stops. Otherwise, a new distribution starts all over again.
        Fibre_pos=num.zeros((Max_fibres,6), dtype=num.float32) #Fibre position matrix. This is a Matrix of coordinates:
        
        print('BSC: Abans de Rand_PER_uSTRU',len(Fibre_pos))
        
        # 1st Column = fibre ID
        # 2nd Column = X-coordinate of centre
        # 3rd Column = Y-coordinate of centre
        # 4th Column = Splitted fibre: 0=No split, 2=half, 4=corners 
        # 5th Column = Fibre Type     
        # 6th Column = Fibre radius
        # Row = data of fibre with identity ID

        # Call function for generating the fibres:
        status,N_fibre,Fibre_pos,A_total,a,b = Rand_PER_uSTRU_GEN_3D_LayerBundle(IDlayerVectFt1,IDlayerVectFt0,MatRichRegionX,MatRichRegionY,WidthMatRich,HeightMatRich,CreateLargerRatio, Vol_fibre_req,Fibre_type_1, Error_V_fibres, Error_V_voids,
                                                                                 NbundlesRa, Hybrid_type,Fibre_pos, R, DISTMIN, cluster_fibres, Max_fibres, N_guesses_max, N_cycles_max, N_change, Square_size, Square_inc, inter_option, a, b, S_base, R1, FirstFibreTypeRa,VariableFibreRadius,
                                                                                 R_STDEV,R1_STDEV,Stacking_sequence,Stacking_sequence_thickness, First_row_types_ft0,Next_row_types_ft0,First_row_types_ft1,Next_row_types_ft1,Sec_heur_inter_intra)
        print('BSC: Despres de RAnd_Per_uSTRU',len(Fibre_pos))


    ###########################################################################
    # Output all data and finish                                              #
    ###########################################################################
    
    # Update RVE information:
    delta_width=a/R
    delta_height=b/R
    #Vec_del=num.arange(N_fibre,Max_fibres, dtype=num.int32)      # Fibres to delete (since were not generated)
    Vec_del=num.arange(N_fibre,len(Fibre_pos), dtype=num.int32)   # Fibres to delete (since were not generated)
    Fibre_pos=num.delete(Fibre_pos,Vec_del,axis=0)                # Delete them
    Fibre_pos[:,0]=num.arange(1,N_fibre+1)                        # Correclty input the fibre indices

    if kfl_plot:
      # Update default matplotlib options with custom ones
      plt.ioff()
      plt.rcParams['xtick.labelsize'] = 40 #Set x tick size
      plt.rcParams['ytick.labelsize'] = 40 #Set y tick size
      plt.rcParams['font.size'] = 40 #Set font size for labels
      plt.rcParams['figure.figsize'] = [10, 10] #Set figure size
      #    plt.rcParams.update({'lines.markersize': 10.0})
      plt.rcParams.update({'lines.linewidth': 2.5})
      #    plt.rcParams.update({'lines.marker': 'None'})
      #    plt.rcParams.update({'axes.titlepad': 50.0})
      plt.rcParams['xtick.major.pad'] = 10 #Space between label numbers and figure
      plt.rcParams['xtick.minor.pad'] = 10
      plt.rcParams['ytick.major.pad'] = 10
      plt.rcParams['ytick.minor.pad'] = 10
      plt.rcParams['xtick.major.width'] = 3 #Width of x tick (the line from the label numbers to the plot)
      plt.rcParams['xtick.minor.width'] = 3
      plt.rcParams['ytick.major.width'] = 3
      plt.rcParams['ytick.minor.width'] = 3
      plt.rcParams['xtick.minor.size'] = 15 #And the length of those lines
      plt.rcParams['xtick.major.size'] = 15
      plt.rcParams['ytick.minor.size'] = 15
      plt.rcParams['ytick.major.size'] = 15
      plt.rcParams['lines.markeredgewidth'] = 5.0
      # matplotlib.font_manager._rebuild()
      plt.rcParams['font.family']='Times New Roman'

    if CreateLargerRatio==1: #Then the domain is multiplied as given by MultipleSize:
        Ind1=(num.where(Fibre_pos[:,4]==0)[0])+1 #Indices of fibre type 1
        Ind2=(num.where(Fibre_pos[:,4]==1)[0])+1 #Indices of fibre type 2
        if kfl_plot:
            fig=plt.figure(num=1) #Generate a figure
            ax=fig.add_subplot(1,1,1) #Generate axes
            ax.set_aspect(1) #Forces the x and y axes as to be of the same scale

            #plot the fibres
            circles(Fibre_pos[Ind1-1,1], Fibre_pos[Ind1-1,2], Fibre_pos[Ind1-1,5], c='b', edgecolor='none', lw=0)#, rasterized=True)
            if Ind2.shape[0]>0:
                circles(Fibre_pos[Ind2-1,1], Fibre_pos[Ind2-1,2], Fibre_pos[Ind2-1,5], c='g', edgecolor='none', lw=0)#, rasterized=True)

            plt.ylim(0, b) #Cut the domain to represent the matrix
            plt.xlim(0, a)
            plt.xlabel('RVE width [mm]')
            plt.ylabel('RVE height [mm]')
            plt.savefig(OutputCaseName+'_FibrePlotBefore_'+str(SimNumb)+'.pdf', bbox_inches='tight')
            plt.close(fig)

        #Now multiply the domain:
        Fibre_posNew = ExtendDomain(R, N_fibre, delta_width, MultipleSizeWidth,MultipleSizeheight, delta_height, Fibre_pos) #This simply repeats the fibres shifting them
        Fibre_pos2=num.zeros((Fibre_posNew.shape[0],6), dtype=num.float32) #Change its name.
        Fibre_pos2[:,1:]=Fibre_posNew[:,1:]
        Fibre_pos2[:,0]=num.arange(1,Fibre_pos2.shape[0]+1)

        #Some fibres are now repeated since they have been merged. Proceed to remove them and adjust their area:
        IndexDel = AdjustArea(Fibre_pos2)
        IndexDel=num.unique(IndexDel)
        Fibre_pos2=num.delete(Fibre_pos2,IndexDel[1:]-1,0)
        delta_width *=MultipleSizeWidth #Final ratio width
        delta_height *=MultipleSizeheight #Final ratio height
        a=delta_width*R #Final RVE width
        b=delta_height*R #Final RVE height
        A_total=a*b #Total cross-sectional area
        Fibre_pos=Fibre_pos2 #Re-name (CONSIDER CREATING DIRECLTY FIBRE_POS)
        N_fibre=Fibre_pos.shape[0] #Final amount of fibres
        Fibre_pos[:,0]=num.arange(1,N_fibre+1) #Re-adjust fibre identities

    #Show final data in screen (volume fractions and fibre numbers)
    # print('Final total number of fibres:',N_fibre)
    Ind1=(num.where(Fibre_pos[:,4]==0)[0])+1 #Fibre 1 indices
    Ind2=(num.where(Fibre_pos[:,4]==1)[0])+1 #Fibre 2 indices
    N_fibre_1=Ind1.shape[0] #Number of fibres 1
    N_fibre_2=Ind2.shape[0] #Number of fibres 2
    print('Final total number of fibres:', N_fibre_1)
    print('Final total number of voids:', N_fibre_2)

    # Update final fibre volume fractions
    Vol_fibreReal=0
    Vol_fibreReal1=0
    Vol_fibreReal2=0
    Area_Dic={0: 1.0, 2: 0.5, 4: 0.25} #0=Full Fibre --> area complete (1 area), 2=half fibre (0.5 of a complete area), 4=quarter area
    for zz in range(1, N_fibre+1):
        Vol_fibreReal +=((num.pi*Fibre_pos[zz-1,6-1]**2)/A_total)*Area_Dic[Fibre_pos[zz-1,4-1]]
        if Fibre_pos[zz-1,5-1]==0: # Fiber 1
            Vol_fibreReal1 +=((num.pi*Fibre_pos[zz-1,6-1]**2)/A_total)*Area_Dic[Fibre_pos[zz-1,4-1]]
        elif Fibre_pos[zz-1,5-1]==1: # Fiber 2
            Vol_fibreReal2 +=((num.pi*Fibre_pos[zz-1,6-1]**2)/A_total)*Area_Dic[Fibre_pos[zz-1,4-1]]
    #
    if DISTMIN[1] < 0.:  # if voids can overlap with fibers, recalculate the void volume fraction
        Fibres2Ind = (num.where(Fibre_pos[:, 4] == 1)[0])  # Fibre 2 indices
        A_fibre_2 = num.sum((num.pi * Fibre_pos[Fibres2Ind[:], 5] ** 2))
        for i in Fibres2Ind:
            x = Fibre_pos[i, 1]
            y = Fibre_pos[i, 2]
            r = Fibre_pos[i, 5]
            A_overlap = f_area_voids_overlap(x, y, r, N_fibre, Fibre_pos)
            A_fibre_2 = A_fibre_2 - A_overlap
        Vol_fibreReal2 = A_fibre_2 / A_total

    # print('Final achieved Fibre Volume: ', Vol_fibreReal)
    print('\n RVE GENERAL INFORMATION')
    print('----------------------------------')
    print('Final achieved Fibre Volume: ',      round(Vol_fibreReal1,3))
    print('Error Fibre Volume achieved [%]: ',  round((abs(Vol_fibreReal1-Vol_fibre_req*Fibre_type_1)/(Vol_fibre_req*Fibre_type_1) * 100),3))
    print('Final achieved Void Volume: ',       round(Vol_fibreReal2,3))
    if (Vol_fibre_req-Vol_fibre_req*Fibre_type_1) != 0:
        print('Error Void Volume achieved [%]: ',   round((abs(Vol_fibreReal2-(Vol_fibre_req-Vol_fibre_req*Fibre_type_1))/(Vol_fibre_req-Vol_fibre_req*Fibre_type_1) * 100),3))
    else:
        print('Error Void Volume achieved [%]: ',   round((abs(Vol_fibreReal2-(Vol_fibre_req-Vol_fibre_req*Fibre_type_1)) * 100),3))
    print('\n')

    if kfl_plot:
        # Generates a figure of the generated fibre distribution in pdf format. In blue color fibre 1 types, fibre 2 in green.
        fig=plt.figure(num=1)
        ax=fig.add_subplot(1,1,1)
        ax.set_aspect(1) #Forces the x and y axes as to be of the same scale

        #plot the fibres
        if Ind2.shape[0]>0:
            circles(Fibre_pos[Ind2-1,1], Fibre_pos[Ind2-1,2], Fibre_pos[Ind2-1,5], c='g', edgecolor='none', lw=0)#, rasterized=True) #Then plot the voids
        circles(Fibre_pos[Ind1-1,1], Fibre_pos[Ind1-1,2], Fibre_pos[Ind1-1,5], c='b', edgecolor='none', lw=0)#, rasterized=True) #First plot the fibres

        plt.ylim(0, b) #Cut the domain to represent the matrix
        plt.xlim(0, a)
        plt.xlabel('RVE width [mm]')
        plt.ylabel('RVE height [mm]')
        plt.savefig(OutputCaseName+ '_' + str(SimNumb) + '_FibrePlot.pdf', bbox_inches='tight')
        plt.show()
        plt.close(fig)

    # Volume fraction representation
    if Check_Vf == 1:
        Vol_f=num.zeros((NSquaresX, NSquaresY), dtype=num.float32)
        Xmean=num.zeros((NSquaresX, NSquaresY), dtype=num.float32)
        Ymean=num.zeros((NSquaresX, NSquaresY), dtype=num.float32)
        Vol_f = CheckVfAlongRVE(NSquaresY, NSquaresX, a, b, Fibre_pos, R, R1, Vol_f, Xmean, Ymean)
        PlotVfAlongRVE(Vol_f, NSquaresY, Xmean, Ymean, SimNumb)

    # Export a file with all data to be input in the Progressive Failure Model or other
    num.savez_compressed(OutputCaseName+'_'+str(SimNumb), Fibre_pos=Fibre_pos, R=R, R1=R1, DISTMIN=DISTMIN, SimNumb=SimNumb,
                         delta_width=delta_width,delta_height=delta_height,Fibre_type_1=Fibre_type_1,A_total=A_total,a=a,b=b,
                         Hybrid_type=Hybrid_type, R_STDEV=R_STDEV, R1_STDEV=R1_STDEV)

    print("--- %s minutes ---" % (time.process_time()/60))

    input = open(str(OutputCaseName + '_summary.txt'))
    data = input.read()
    Summary_file = str(OutputCaseName + '_' + str(SimNumb) + '_summary.txt')
    with open(Summary_file, 'a') as f:
        f.write(data)
        f.write('DESCRIPTION OF THE RVE ACHIEVED \n')
        f.write('Final achieved Fibre Volume [-]: %s\n'             % str((round(Vol_fibreReal1,3))))
        f.write('Error Fibre Volume achieved [percentage]: %s\n'    % str(round((abs(Vol_fibreReal1-Vol_fibre_req*Fibre_type_1)/(Vol_fibre_req*Fibre_type_1) * 100),3)))
        f.write('Final total number of fibres [fibres]: %s\n'       % N_fibre_1)
        #
        f.write('Final achieved Void Volume [-]: %s\n'              % str((round(Vol_fibreReal2,3))))
        if (Vol_fibre_req-Vol_fibre_req*Fibre_type_1) != 0.:
            f.write('Error Void Volume achieved [percentage]: %s\n' % str(round((abs(Vol_fibreReal2-(Vol_fibre_req-Vol_fibre_req*Fibre_type_1)) / (Vol_fibre_req - Vol_fibre_req * Fibre_type_1) * 100), 3)))
        else:
            f.write('Error Void Volume achieved [percentage]: %s\n'     % str(round((abs(Vol_fibreReal2-(Vol_fibre_req-Vol_fibre_req*Fibre_type_1)) * 100),3)))
        f.write('Final total number of voids [fibres]: %s\n'        % N_fibre_2)
        
        return
    
    return Fibre_pos


    
    
