# Import libraries
import numpy as num
from numba import jit
# Import local libraries
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_overlap import f_overlap
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_overlap import f_boundary
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_overlap import f_close_to_boundary
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_overlap import f_area_voids_overlap
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_FirstHeur import Rand_Per_uSTRU_FirstHeur
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_SecHeur import Rand_Per_uSTRU_SecHeur


@jit(cache=True, nopython=True)
def Rand_PER_uSTRU_GEN_3D_LayerBundle(IDlayerVectFt1, IDlayerVectFt0, MatRichRegionX, MatRichRegionY, WidthMatRich,
                                      HeightMatRich, CreateLargerRatio, Vol_fibre_req, Fibre_type_1,
                                      Error_V_fibres, Error_V_voids,
                                      NbundlesRa, Hybrid_type, Fibre_pos,
                                      R, DISTMIN, cluster_fibres, Max_fibres, N_guesses_max, N_cycles_max, N_change, Square_size,
                                      Square_inc, inter_option, a, b, S_base, R1, FirstFibreTypeRa, VariableFibreRadius,
                                      R_STDEV, R1_STDEV, Stacking_sequence, Stacking_sequence_thickness,
                                      First_row_types_ft0, Next_row_types_ft0, First_row_types_ft1, Next_row_types_ft1,
                                      Sec_heur_inter_intra):
    '''
    The Python function generates a RVE with a random distribution of fibres as many
    times as requested by the user by means of a hard-core-model and two heuristic
    criteria.

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    IDlayerVectFt1 : float32 numpy array of shape (n, ) where n is the number of fibres in thr RVE
            This is used in interlayer hybrids to know the layer at which each fibre of type 2
            belongs to.
    IDlayerVectFt0 : float32 numpy array of shape (n, ) where n is the number of fibres in thr RVE
            This is used in interlayer hybrids to know the layer at which each fibre of type 1
            belongs to.
    MatRichRegionX : float,
            Defines a region where there are no fibres in X direction close to the edges of the RVE
    MatRichRegionY : float
            Defines a region where there are no fibres in Y direction close to the edges of the RVE
    WidthMatRich : integer
            Whether to use the MatRichRegionX region
    HeightMatRich : integer
            Whether to use the MatRichRegionY region
    CreateLargerRatio : integer
            Option to multiply an RVE and make it bigger by repeating a smaller generated RVE
    Vol_fibre_req : float
            Overall fibre volume fraction requested.
    Fibre_type_1 : float
            Amount of type 1 fibres in respect to the overal fibre volume fraction
    Error_V_fibres : float
            Maximum error allowed for the fibre volume content
    Error_V_voids : float
            Maximum error allowed for the voids volume content
    NbundlesRa : integer,
            Number of bundles for an intralayer hybrid
    Hybrid_type : integer
            Determines the hybrid type to generate (intrayarn, interlayer or intralayer)
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    R : float
            Average radius of fibre type 1
    DISTMIN : array [0,3]
            Minimum distance multiplier between: [fibres, fibre-void, voids]
    cluster_fibres : numba dict
            Dictionary with the position where there must be a fiber cluster and the minimum position between them
    Max_fibres : integer
            Determines the maximum number of possible fibres in the RVE
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
    R1 : float
            Average radius of fibre type 2
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
    First_row_types_ft0 : numpy array of shape (,NbundlesRa)
            Used to establish the different bundles for an intralayer hybrid
    Next_row_types_ft0 : numpy array of shape (,NbundlesRa)
            Used to establish the different bundles for an intralayer hybrid
    First_row_types_ft1 : numpy array of shape (,NbundlesRa)
            Used to establish the different bundles for an intralayer hybrid
    Next_row_types_ft1 : numpy array of shape (,NbundlesRa)
            Used to establish the different bundles for an intralayer hybrid
    Sec_heur_inter_intra : integer
            Determines whether the 2nd heuristic is applied when the volum
            fraction is already reached

    Kwargs
    -----
        none

    Return
    --------
    status : integer
            Status of the simulation
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    A_total : float
            Total area of image
    a : float
            Width of the generated RVE
    b : float
            Height of the generated RVE


    Examples
    -----
        none

    Raises
    -----
        none

    Note
    -----
        Generation of random distribution of fibres in long-fibre reinforced composites
        Melro, A.R. et al.

    Program called by
    -----
        File "Rand_uSTRU_f_Loop.py"

    Program calls
    -----
        File "Rand_uSTRU_f_overlap.py", "Rand_uSTRU_f_FirstHeur", "Rand_uSTRU_f_SecHeur.py"
    '''

    ###########################################################################
    # Determination of Auxiliary Parameters                                   #
    ###########################################################################
    if inter_option == 1:
        A_total = a * (b - 2.0 * R)  # total area of image minus the interlaminar area
    else:
        A_total = a * b  # total area of image

    # WIP parameters:
    if MatRichRegionX == 0:  # No matrix rich region for x and y
        WidthMatRich = 0.0
    if MatRichRegionY == 0:
        HeightMatRich = 0.0

    # Generate some auxiliary arrays and variables
    r_fib = num.array([R, R1])  # Average fibre radius array
    r_STDEV = num.array([R_STDEV, R1_STDEV])  # Standard deviation of each fibre radius
    A_fib = num.array([num.pi * R ** 2, num.pi * R1 ** 2])  # Area of a single fibre type 1 and 2
    N_cycles = 1  # number of cycles of the algorithm
    # Re_start=0 #Variable when a pair is incorreclty deleted (possible bug)
    if Hybrid_type == 0:
        First_Heur_op = 0  # Intrayarn and non-hybrid composites use this option as default
        Sec_heur_inter_intra = 0  # Intrayarn and non-hybrid composites use this option as default
    else:
        First_Heur_op = 1
    #
    ###########################################################################
    # Generation of regions for the RVE where only a certain fibre tye is     #
    # allowed.                                                                #
    ###########################################################################
    #
    if FirstFibreTypeRa == 0:  # First fibre type for intralayer hybrid is given by Python
        if Fibre_type_1 <= 0.5:
            FirstBundleTypeRa = 1  # Then first fibre type is a fibre type 2
        else:
            FirstBundleTypeRa = 0  # Then first fibre type is a fibre type 1
    elif FirstFibreTypeRa == 1:  # Then first fibre type is fibre 1
        FirstBundleTypeRa = 0
    elif FirstFibreTypeRa == 2:  # Then first fibre type is fibre 2
        FirstBundleTypeRa = 1

    if Hybrid_type == 1:  # In interlayer hybrids the first fibre type is given by the user data
        if Stacking_sequence[0] == 0:
            FirstBundleTypeRa = 0  # Then first fibre type is fibre 1
        else:
            FirstBundleTypeRa = 1  # Then first fibre type is fibre 2
        Nlayers1 = int(num.sum(Stacking_sequence[:] == 0))  # Number of layers of population 1
        Nlayers2 = int(num.sum(Stacking_sequence[:] == 1))  # Number of layers of population 2
        Nlayers = int(Nlayers1 + Nlayers2)  # Total number of layers

        # Generate the coordinates of each ply
        Xmin = num.zeros(Nlayers)
        Xmax = num.zeros(Nlayers)
        Xmax[:] = a
        Ymin = num.zeros(Nlayers)
        Ymax = num.zeros(Nlayers)
        Ycurr = 0
        for lay in range(1, Nlayers + 1):  # For each ply
            LayerThick = Stacking_sequence_thickness[lay - 1]  # Ply thickness
            Ycurr += LayerThick
            Ymin[lay - 1] = Ycurr - LayerThick  # Y coordinate where the ply starts
            Ymax[lay - 1] = Ycurr  # Y coordinate where the ply ends

        # Now set the correct type of fibre that is allowed at each layer
        Ft1IndexRows = (num.where(Stacking_sequence[:] == 0)[
            0]) + 1  # These are x and y indices of the layers of fibre type 1. This indices may be used to enter into the vectors Xmin, Xmax, Ymin, Ymax to konw the coordinates of the layers
        Ft2IndexRows = (num.where(Stacking_sequence[:] == 1)[0]) + 1
        Ft1IndexCols = (num.where(Stacking_sequence[:] == 0)[
            0]) + 1  # These are x and y indices of the layers of fibre type 2. This indices may be used to enter into the vectors Xmin, Xmax, Ymin, Ymax to konw the coordinates of the layers
        Ft2IndexCols = (num.where(Stacking_sequence[:] == 1)[0]) + 1

    BundZoneFtEnd = num.zeros((NbundlesRa, NbundlesRa), dtype=num.int64)    # BSC

    if Hybrid_type == 2:  # Regions for an intralayer hybrid (bundle-by-bundle)
        if CreateLargerRatio == 0:
            # Create X and Y regions where each fibre type is allowed according to the bundles.
            # Note: each region is defined by four points, given by the Xmin, Xmax, Ymin and Ymax coordinates.
            # Each position in these vectors corresponds to a region. A different fibre type is then
            # assigned to each region, so that each fibre type is located in different bundles.
            X_thickness = a / NbundlesRa  # The x thickness (width) of the bundles
            Y_thickness = b / NbundlesRa  # The y thickness (height) of the bundles
            Xmin = num.zeros(NbundlesRa)
            Xmax = num.zeros(NbundlesRa)
            Ymin = num.zeros(NbundlesRa)
            Ymax = num.zeros(NbundlesRa)
            for bundle in range(1, NbundlesRa + 1):  # For each bundle
                if bundle == 1:
                    Xmin[bundle - 1] = 0.0
                    Xmax[bundle - 1] = X_thickness
                    Ymin[bundle - 1] = 0.0
                    Ymax[bundle - 1] = Y_thickness
                else:
                    Xmin[bundle - 1] = Xmin[bundle - 2] + X_thickness
                    Xmax[bundle - 1] = Xmin[bundle - 1] + X_thickness
                    Ymin[bundle - 1] = Ymin[bundle - 2] + Y_thickness
                    Ymax[bundle - 1] = Ymin[bundle - 1] + Y_thickness

        #            Xmin=num.arange(0,a,a/NbundlesRa)
        #            Xmax=num.arange(a/NbundlesRa,a+a/NbundlesRa,a/NbundlesRa)
        #            Ymin=num.arange(0,b,b/NbundlesRa)
        #            Ymax=num.arange(b/NbundlesRa,b+b/NbundlesRa,b/NbundlesRa)
        elif CreateLargerRatio == 1:  # First and last X, Y are half.
            # Create X and Y regions where each fibre type is allowed according to the bundles
            Xmin = num.zeros(NbundlesRa)
            Xmax = num.zeros(NbundlesRa)
            Ymin = num.zeros(NbundlesRa)
            Ymax = num.zeros(NbundlesRa)
            IncrX = a / (NbundlesRa - 1)
            IncrY = b / (NbundlesRa - 1)
            for bund in range(1, NbundlesRa + 1):
                if bund == 1:
                    Xmin[bund - 1] = 0.0
                    Xmax[bund - 1] = IncrX / 2
                    Ymin[bund - 1] = 0.0
                    Ymax[bund - 1] = IncrY / 2
                elif bund != 1 and bund != NbundlesRa:
                    if bund == 2:
                        Xmin[bund - 1] = Xmin[bund - 2] + IncrX / 2
                        Ymin[bund - 1] = Ymin[bund - 2] + IncrY / 2
                    else:
                        Xmin[bund - 1] = Xmin[bund - 2] + IncrX
                        Ymin[bund - 1] = Ymin[bund - 2] + IncrY
                    Xmax[bund - 1] = Xmax[bund - 2] + IncrX
                    Ymax[bund - 1] = Ymax[bund - 2] + IncrY
                elif bund == NbundlesRa:
                    Xmin[bund - 1] = Xmin[bund - 2] + IncrX
                    Xmax[bund - 1] = Xmax[bund - 2] + IncrX / 2
                    Ymin[bund - 1] = Ymin[bund - 2] + IncrY
                    Ymax[bund - 1] = Ymax[bund - 2] + IncrY / 2
            a = Xmax[-1]
            b = Ymax[-1]
            A_total = a * b

        # Now set the correct type of fibre that is allowed at each bundle.
        # In each region, only one fibre type is allowed.
        if FirstBundleTypeRa == 0:  # In this case, the first bundle contains fibres of type 1
            First_row_types = First_row_types_ft0
            Next_row_types = Next_row_types_ft0
        else:  # In this case, the first bundle contains fibres of type 2
            First_row_types = First_row_types_ft1
            Next_row_types = Next_row_types_ft1
        First_row_types = First_row_types[0:NbundlesRa]
        Next_row_types = Next_row_types[0:NbundlesRa]

        BundZoneFtEnd = num.zeros((NbundlesRa, NbundlesRa),
                                  dtype=num.int64)  # 2D array representing all the bundles in the RVE and the fibre type allowed in each one. Bundles with a 0 contain fibres of type 1, bundles with a 1 contain fibres of type 2.
        for bundle in range(1, NbundlesRa + 1):
            if (bundle % 2) == 0:  # Even bundle --> takes First_row_types
                BundZoneFtEnd[bundle - 1, :] = Next_row_types
            else:  # Odd bundle --> takes Next_row_types
                BundZoneFtEnd[bundle - 1, :] = First_row_types

        Ft1Index = num.where(BundZoneFtEnd == 0)  # Find all bundles of fibres type 1
        Ft1IndexRows = Ft1Index[
                           0] + 1  # These are x and y indices of the bundles of fibre type 1. This indices may be used to enter into the vectors Xmin, Xmax, Ymin, Ymax to konw the coordinates of the bundle
        Ft1IndexCols = Ft1Index[1] + 1
        Ft2Index = num.where(BundZoneFtEnd == 1)  # Find all bundles of fibres type 2
        Ft2IndexRows = Ft2Index[
                           0] + 1  # These are x and y indices of the bundles of fibre type 2. This indices may be used to enter into the vectors Xmin, Xmax, Ymin, Ymax to konw the coordinates of the bundle
        Ft2IndexCols = Ft2Index[1] + 1

    elif Hybrid_type == 0:  # Intrayarn hybrid or non-hybrid material
        # For this material configuration, all fibre types are allowed everywhere, and the RVE
        # is not divided into regions (i.e., there is only one region).
        Xmin = num.array([0.0])
        Xmax = num.array([a])
        Ymin = num.array([0.0])
        Ymax = num.array([b])
        Ft1IndexCols = num.array([1])
        Ft2IndexCols = num.array([1])
        Ft1IndexRows = num.array([1])
        Ft2IndexRows = num.array([1])

    #
    ###########################################################################
    # Definition of Output Variable                                           #
    ###########################################################################
    #
    # Fibre_pos            # Matrix of coordinates
    #                      # 1st Column = fibre ID
    #                      # 2nd Column = X-coordinate of centre
    #                      # 3rd Column = Y-coordinate of centre
    #                      # 4th Column = Splitted fibre: 
    #                      # 0=No, 2=half, 4=corners
    #                      # 5th Column = Fibre Type     
    #                      # 6th Column =  Fibre radius
    ###########################################################################
    # Initialization of Calculus                                              #
    ###########################################################################
    #
    # For interlayer hybrids pick up the correct stacking sequence that will be used later
    if FirstBundleTypeRa == 0:
        IDlayerVect = IDlayerVectFt0
    elif FirstBundleTypeRa == 1:
        IDlayerVect = IDlayerVectFt1

    Vec_mem = num.zeros((Max_fibres, N_change),
                        dtype=num.float32)  # Memory vector for First Heuristic. Orignal generator used a memory as num.zeros((Max_fibres,N_cycles_max+1), dtype=num.float32). But since only the current and previous cycle information are used, to save memory, I change it accordingly.
    Vol_fibre = 0  # Overall fibre volume fraction
    Vol_fibre_1 = 0  # Type 1 fibre volume fraction
    Vol_fibre_2 = 0  # Type 2 fibre volume fraction
    N_fibre_real = 1  # Number of "complete" fibres
    N_fibre = 1  # Total number of fibres. Start by one, as we now proceed to create the first fibre
    N_fibre_1 = 0  # Number of type 1 fibres (it is not really used here)
    N_fibre_2 = 0  # number of type 2 fibres (it is not really used here)
    #
    if Fibre_type_1 == 1:  # Non-hybrid, select fibre type 1, and region 1
        ft = 0
        Xend = Xmax[0]
        Xst = Xmin[0]
        Yend = Ymax[0]
        Yst = Ymin[0]
    elif Fibre_type_1 == 0:  # Non-hybrid, select fibre type 2, and region 1
        ft = 1
        Xend = Xmax[0]
        Xst = Xmin[0]
        Yend = Ymax[0]
        Yst = Ymin[0]
    else:
        if R > R1:  # Hybrid, select fibre type 1, and a random region
            ft = 0
            Ind = num.random.randint(1, Ft1IndexRows.shape[
                0] + 1)  # Select randomly one of the regions where fibre type 1 is allowed
            Xend = Xmax[Ft1IndexCols[Ind - 1] - 1]  # Get the coordinates of the selected region
            Xst = Xmin[Ft1IndexCols[Ind - 1] - 1]
            Yend = Ymax[Ft1IndexRows[Ind - 1] - 1]
            Yst = Ymin[Ft1IndexRows[Ind - 1] - 1]
        else:
            ft = 1  # Hybrid, select fibre type 2, and a random region
            Ind = num.random.randint(1, Ft2IndexRows.shape[
                0] + 1)  # Select randomly one of the regions where fibre type 2 is allowed
            Xend = Xmax[Ft2IndexCols[Ind - 1] - 1]  # Get the coordinates of the selected region
            Xst = Xmin[Ft2IndexCols[Ind - 1] - 1]
            Yend = Ymax[Ft2IndexRows[Ind - 1] - 1]
            Yst = Ymin[Ft2IndexRows[Ind - 1] - 1]

    Fibre_pos[1 - 1, 5 - 1] = ft  # Save fibre type
    if VariableFibreRadius == 0:
        Fibre_pos[1 - 1, 6 - 1] = r_fib[ft]  # Save fibre radius
        Vol_fibre += A_fib[ft] / A_total  # Update fibre volume fraction
        if ft == 0:
            Vol_fibre_1 += A_fib[ft] / A_total
        else:
            Vol_fibre_2 += A_fib[ft] / A_total
    elif VariableFibreRadius == 1:
        Fibre_pos[1 - 1, 6 - 1] = num.random.normal(loc=r_fib[ft], scale=r_STDEV[
            ft])  # Save fibre radius, accordingly to the standard deviation!
        Vol_fibre += (num.pi * Fibre_pos[1 - 1, 6 - 1] ** 2) / A_total  # Save fibre radius
        if ft == 0:
            Vol_fibre_1 += (num.pi * Fibre_pos[1 - 1, 6 - 1] ** 2) / A_total
        else:
            Vol_fibre_2 += (num.pi * Fibre_pos[1 - 1, 6 - 1] ** 2) / A_total
    Fibre_pos[1 - 1, 2 - 1] = num.random.uniform(Xst + Fibre_pos[1 - 1, 6 - 1] + WidthMatRich, Xend - Fibre_pos[
        1 - 1, 6 - 1] - WidthMatRich)  # Generate random X-position of first fibre in the chosen region
    Fibre_pos[1 - 1, 3 - 1] = num.random.uniform(Yst + Fibre_pos[1 - 1, 6 - 1] + HeightMatRich, Yend - Fibre_pos[
        1 - 1, 6 - 1] - HeightMatRich)  # Generate random Y-position of first fibre in the chosen region
    Fibre_pos[1 - 1, 4 - 1] = 0
    N_attempts = 0  # number of attempts on fibre collocation

    #
    ###########################################################################
    # Start generation of RVE with random position of fibres                  #
    ###########################################################################
    #
    Zone = 0  # Current region of the RVE to place a fibre
    Dif_V_fibre = 1. # The initial difference between the fibre volume content real and theoretical is 100%
    Dif_V_void = 1.  # The initial difference between the voids volume content real and theoretical is 100%

    while (Dif_V_fibre >= Error_V_fibres or Dif_V_void >= Error_V_voids) and N_cycles <= N_cycles_max:
        print(' ')
        print('Iteration number: ', N_cycles)
        while N_attempts < (N_cycles * N_guesses_max) and (Vol_fibre_req > Vol_fibre) and (
                N_fibre < Max_fibres):  # The hard-core model runs while these conditions hold
            #
            ###########################################################################
            # Randomly determine position of fibres and compatibility check:          #
            # Hard-core model                                                         #
            ###########################################################################
            #
            N_attempts += 1  # New attempt
            split = 0  #
            Zone += 1  # Move to next RVE region

            # Check which fibre type should be created
            if Fibre_type_1 == 1:
                ft = 0
                FtIndexCols = Ft1IndexCols
                FtIndexRows = Ft1IndexRows
            elif Fibre_type_1 == 0:
                ft = 1
                FtIndexCols = Ft2IndexCols
                FtIndexRows = Ft2IndexRows
            elif Vol_fibre_1 < Fibre_type_1 * (Vol_fibre):
                ft = 0
                FtIndexCols = Ft1IndexCols
                FtIndexRows = Ft1IndexRows
            elif Vol_fibre_2 < (1 - Fibre_type_1) * (Vol_fibre):
                ft = 1
                FtIndexCols = Ft2IndexCols
                FtIndexRows = Ft2IndexRows

            if Zone > FtIndexRows.shape[0]:
                Zone = 1

            # Obtain the coordinates of the current RVE region to fill fibres with the selected fibre type
            Ind = int(Zone)
            Xend = Xmax[FtIndexCols[Ind - 1] - 1]
            Xst = Xmin[FtIndexCols[Ind - 1] - 1]
            Yend = Ymax[FtIndexRows[Ind - 1] - 1]
            Yst = Ymin[FtIndexRows[Ind - 1] - 1]

            # Generate fibre radius and area accordingly to the standard deviation (if used or not)
            if VariableFibreRadius == 0:
                r = r_fib[ft]
                A_fibre = A_fib[ft]
            elif VariableFibreRadius == 1:
                r = num.random.normal(loc=r_fib[ft], scale=r_STDEV[ft])
                A_fibre = num.pi * r ** 2

            MaxDist = 0.0  # Security distance used later
            XC = num.random.uniform(-r + Xst + WidthMatRich,
                                    Xend + r - WidthMatRich)  # Generate X random coordinate of possible new fibre, in the selected region
            YC = num.random.uniform(-r + Yst + HeightMatRich,
                                    Yend + r - HeightMatRich)  # Generate Y random coordinate of possible new fibre, in the selected region

            if (XC >= r) and (XC <= a - r) and (YC >= r) and (
                    YC <= b - r):  # If fibre is anywhere on the domain except the edges or vertices
                check = f_overlap(XC, YC, N_fibre + 1, r, ft, N_fibre, Fibre_pos, DISTMIN, cluster_fibres)  # Check if the fibre overlaps with any other fibre in the RVE
                check_boundary = f_close_to_boundary(XC, YC, r, a, b)  # Check if the fibre is very close to a boundary
                if check == 0 and check_boundary == 0:  # If does not overlap with any other fibre
                    N_fibre += 1  # Accept the fibre and add it into the RVE
                    Fibre_pos[N_fibre - 1, 0] = N_fibre  # Fibre ID
                    Fibre_pos[N_fibre - 1, 2 - 1] = XC  # Fibre XC
                    Fibre_pos[N_fibre - 1, 3 - 1] = YC  # Fibre YC
                    Fibre_pos[N_fibre - 1, 4 - 1] = 0  # Indicator
                    Fibre_pos[N_fibre - 1, 5 - 1] = ft  # Type
                    Fibre_pos[N_fibre - 1, 6 - 1] = r  # radius

                    # Update volume fractions and number of fibres of each type
                    if ft == 0:
                        N_fibre_1 += 1
                        Vol_fibre_1 += A_fibre / A_total
                    elif ft == 1:
                        N_fibre_2 += 1
                        # if DISTMIN[1] < 0: #if the void can overlap
                        #     A_overlap = f_area_voids_overlap(XC, YC, r, Fibre_pos)
                        #     A_fibre = A_fibre - A_overlap
                        Vol_fibre_2 += A_fibre / A_total

                    Vol_fibre += A_fibre / A_total
                    N_fibre_real += 1

            elif (XC >= r) and (XC <= a - r) and (
                    YC < r):  # Z2: fibre at bottom outskirt --> we need to do a pair, as there will be a pair for that fibre on top (to allow geometry periodicity)
                XC1 = XC  # XC coordinate of the pair fibre located at top, it is the same
                YC1 = YC + b  # The Y coordinate is the same plus b
                split = 2  # Indicates the fibre is divided into 2 parts
            elif (XC >= r) and (XC <= a - r) and (YC > b - r):  # Z3: fibre at top --> pair at bottom
                XC1 = XC
                YC1 = YC - b
                split = 2
            elif (YC >= r) and (YC <= b - r) and (XC < r):  # Z4: fibre at left --> pair at right
                XC1 = XC + a
                YC1 = YC
                split = 2
            elif (YC >= r) and (YC <= b - r) and (XC > a - r):  # Z5: fibre at right --> pair at left
                XC1 = XC - a
                YC1 = YC
                split = 2
            elif (XC < r) and (YC < r):  # Z6: fibre at bottom-left vertex --> 3 more pairs at the other vertices
                XC1 = XC + a  # Pair coordinates move to the other vertices so add a and b
                YC1 = YC + b
                split = 4  # Indicates the fibre is splitted into 4 fibres
                MaxDist = num.sqrt((XC) ** 2 + (
                    YC) ** 2)  # This is a maximum distance to enforce there are really 4 fibres (and not 2 or 3)
            elif (XC > a - r) and (YC < r):  # Z7: fibre at bottom-right vertex
                XC1 = XC - a  # Similalry, substract a and add b, and so on with the missing cases
                YC1 = YC + b
                split = 4
                MaxDist = num.sqrt((XC1) ** 2 + (YC) ** 2)
            elif (XC > a - r) and (YC > b - r):  # Z8: fibre at top-right vertex
                XC1 = XC - a
                YC1 = YC - b
                split = 4
                MaxDist = num.sqrt((XC1) ** 2 + (YC1) ** 2)
            elif (XC < r) and (YC > b - r):  # Z9: and at top-left
                XC1 = XC + a
                YC1 = YC - b
                split = 4
                MaxDist = num.sqrt((XC) ** 2 + (YC1) ** 2)
            #
            if split == 2:  # If the fibre needs a pair
                check = f_overlap(XC, YC, N_fibre + 1, r, ft, N_fibre, Fibre_pos,
                                  DISTMIN, cluster_fibres)  # Check if the fibre overlaps with any other fibre in the RVE
                check_boundary = f_boundary(XC, YC, r, a, b)  # Check if the fibre is in a boundary very small
                if check == 0 and check_boundary == 0:  # Then, this fibre can be added, but now we need to check the pair with coordinates XC1, YC1
                    check = f_overlap(XC1, YC1, N_fibre + 1, r, ft, N_fibre, Fibre_pos,
                                      DISTMIN, cluster_fibres)  # Check if the fibre pair overlaps with any other fibre in the RVE
                    check_boundary = f_boundary(XC1, YC1, r, a, b)  # Check if the fibre is in a boundary very small
                    if check == 0 and check_boundary == 0:  # Then, both fibre can be added, (1 entire fibre divided into two):
                        N_fibre += 2  # Two more fibres
                        Fibre_pos[N_fibre - 2, 0] = N_fibre - 1  # Fibre ID
                        Fibre_pos[N_fibre - 2, 2 - 1] = XC  # Fibre XC
                        Fibre_pos[N_fibre - 2, 3 - 1] = YC  # YC
                        Fibre_pos[N_fibre - 2, 4 - 1] = 2  # Area type
                        Fibre_pos[N_fibre - 2, 5 - 1] = ft  # Fibre type
                        Fibre_pos[N_fibre - 2, 6 - 1] = r  # Fibre radius
                        # Same now with the pair
                        Fibre_pos[N_fibre - 1, 0] = N_fibre  # Fibre ID
                        Fibre_pos[N_fibre - 1, 2 - 1] = XC1
                        Fibre_pos[N_fibre - 1, 3 - 1] = YC1
                        Fibre_pos[N_fibre - 1, 4 - 1] = 2
                        Fibre_pos[N_fibre - 1, 5 - 1] = ft
                        Fibre_pos[N_fibre - 1, 6 - 1] = r
                        # And now update the volume fractions and number of fibres as well
                        if ft == 0:
                            N_fibre_1 += 1
                            Vol_fibre_1 += A_fibre / A_total
                        elif ft == 1:
                            N_fibre_2 += 1
                            # if DISTMIN[1] < 0:  # if the void can overlap
                            #     A_overlap_1 = f_area_voids_overlap(XC, YC, r, Fibre_pos)
                            #     A_overlap_2 = f_area_voids_overlap(XC1, YC1, r, Fibre_pos)
                            #     A_fibre = A_fibre - A_overlap_1 - A_overlap_2
                            Vol_fibre_2 += A_fibre / A_total

                        Vol_fibre += A_fibre / A_total
                        N_fibre_real += 1

            elif split == 4:  # Now, the same but with a fibre in a vertex
                # Compared with the original generator by Merlo et al., here we add a new condition.
                # In this condition (MaxDist), we make sure that there will be really 4 parts in the domain.
                # Else, it happenend that sometimes there were 3 parts and a fourth part out of the domain, which may cause glitches with the PFM. This should avoid it.
                if MaxDist < r:
                    check = f_overlap(XC, YC, N_fibre + 1, r, ft, N_fibre, Fibre_pos, DISTMIN, cluster_fibres)
                    check_boundary = f_boundary(XC, YC, r, a, b)  # Check if the fibre is in a boundary very small
                    if check == 0 and check_boundary == 0:  # If created fibre can be added, check the next
                        check = f_overlap(XC, YC1, N_fibre + 1, r, ft, N_fibre, Fibre_pos, DISTMIN, cluster_fibres)
                        check_boundary = f_boundary(XC, YC1, r, a, b)  # Check if the fibre is in a boundary very small
                        if check == 0 and check_boundary == 0:
                            check = f_overlap(XC1, YC, N_fibre + 1, r, ft, N_fibre, Fibre_pos, DISTMIN, cluster_fibres)
                            check_boundary = f_boundary(XC1, YC, r, a,
                                                        b)  # Check if the fibre is in a boundary very small
                            if check == 0 and check_boundary == 0:
                                check = f_overlap(XC1, YC1, N_fibre + 1, r, ft, N_fibre, Fibre_pos, DISTMIN, cluster_fibres)
                                check_boundary = f_boundary(XC1, YC1, r, a,
                                                            b)  # Check if the fibre is in a boundary very small
                                if check == 0 and check_boundary == 0:  # Ok, if all can be added, do it now
                                    N_fibre += 4  # Four more fibres
                                    # Add one quarter
                                    Fibre_pos[N_fibre - 4, 0] = N_fibre - 3
                                    Fibre_pos[N_fibre - 4, 2 - 1] = XC
                                    Fibre_pos[N_fibre - 4, 3 - 1] = YC
                                    Fibre_pos[N_fibre - 4, 4 - 1] = 4
                                    Fibre_pos[N_fibre - 4, 5 - 1] = ft
                                    Fibre_pos[N_fibre - 4, 6 - 1] = r
                                    # next quarter
                                    Fibre_pos[N_fibre - 3, 0] = N_fibre - 2
                                    Fibre_pos[N_fibre - 3, 2 - 1] = XC
                                    Fibre_pos[N_fibre - 3, 3 - 1] = YC1
                                    Fibre_pos[N_fibre - 3, 4 - 1] = 4
                                    Fibre_pos[N_fibre - 3, 5 - 1] = ft
                                    Fibre_pos[N_fibre - 3, 6 - 1] = r
                                    # Next
                                    Fibre_pos[N_fibre - 2, 0] = N_fibre - 1
                                    Fibre_pos[N_fibre - 2, 2 - 1] = XC1
                                    Fibre_pos[N_fibre - 2, 3 - 1] = YC
                                    Fibre_pos[N_fibre - 2, 4 - 1] = 4
                                    Fibre_pos[N_fibre - 2, 5 - 1] = ft
                                    Fibre_pos[N_fibre - 2, 6 - 1] = r
                                    # Next
                                    Fibre_pos[N_fibre - 1, 0] = N_fibre
                                    Fibre_pos[N_fibre - 1, 2 - 1] = XC1
                                    Fibre_pos[N_fibre - 1, 3 - 1] = YC1
                                    Fibre_pos[N_fibre - 1, 4 - 1] = 4
                                    Fibre_pos[N_fibre - 1, 5 - 1] = ft
                                    Fibre_pos[N_fibre - 1, 6 - 1] = r
                                    # Update volumes and number of fibres
                                    if ft == 0:
                                        N_fibre_1 += 1
                                        Vol_fibre_1 += A_fibre / A_total
                                    elif ft == 1:
                                        N_fibre_2 += 1
                                        # if DISTMIN[1] < 0:  # if the void can overlap
                                        #     A_overlap_1 = f_area_voids_overlap(XC, YC, r, Fibre_pos)
                                        #     A_overlap_2 = f_area_voids_overlap(XC, YC1, r, Fibre_pos)
                                        #     A_overlap_3 = f_area_voids_overlap(XC1, YC, r, Fibre_pos)
                                        #     A_overlap_4 = f_area_voids_overlap(XC1, YC1, r, Fibre_pos)
                                        #     A_fibre = A_fibre - A_overlap_1 - A_overlap_2 - A_overlap_3 - A_overlap_4
                                        Vol_fibre_2 += A_fibre / A_total
                                    Vol_fibre += A_fibre / A_total
                                    N_fibre_real += 1
        #
        ###########################################################################
        # Heuristic criterias: use them to open up emtpy areas in the RVE         #
        ###########################################################################
        
        # First Heuristic - Move Fibres Around to Gain More Empty Areas
        N_fibre, Fibre_pos, Vec_mem = Rand_Per_uSTRU_FirstHeur(N_fibre, Fibre_pos, a, b, DISTMIN, cluster_fibres, N_cycles, Vec_mem, N_change, First_Heur_op)
        
        # Second Heuristic - Compact the fibres on the outskirts of the RVE
        Square_size,N_fibre,Fibre_pos,Vec_mem = Rand_Per_uSTRU_SecHeur(IDlayerVect,Hybrid_type,Xmax,Xmin,Ymax,Ymin,Square_size,Square_inc,a,b,R,N_fibre,Fibre_pos,DISTMIN, cluster_fibres, Vec_mem,NbundlesRa,BundZoneFtEnd,Sec_heur_inter_intra,Vol_fibre_1,Vol_fibre_2,Fibre_type_1,Vol_fibre)
        
        # Third Heuristic - Works only for fibres at vertices and outskirts --> discarded, it may be interesting for FEM analyses
        # Vol_fibre,Vol_fibre_1,Vol_fibre_2,Fibre_pos,Vec_mem,N_fibre,N_fibre_real = Rand_Per_uSTRU_ThirdHeur(N_fibre,Fibre_pos,a,b,Vol_fibre,Vol_fibre_1,Vol_fibre_2,A_total,A_fib[0],A_fib[1],Vec_mem,N_fibre_real,S_base)
        # print('Fibre Volume achieved after step 3: ', Vol_fibre)

        # Bug Check:
        CountersQuart = int(num.sum(Fibre_pos[:, 3] == 4))  # Number of fibres splitted into 4 (there should be 0 or 4)
        CountersHalf  = int(num.sum(Fibre_pos[:, 3] == 2))  # Number of fibres splitted into 2 (this should be an even number)
        if ((CountersQuart != 4) and (CountersQuart != 0)) or (CountersHalf % 2 != 0):  
            # If there is an incorrect number of these splitted fibres, then a bug occurred
            print(' ')
            if (CountersQuart != 4) and (CountersQuart != 0):                   # BSC   
                print('Inconsistent number of total fibres splitted into 4 ')   # BSC
            elif CountersHalf % 2 != 0:                                         # BSC
                print('Inconsistent number of total fibres splitted into 2 ')   # BSC
                
            print('Bug occurred. Deletting boundary fibres to avoid the bug.')
            # A bug has occurred which has deleted a fibre incorrectly.
            # As a workaround, we delete the boundary fibres, and update all variables accordingly:
            FullFibres = (num.where(Fibre_pos[:, 3] == 0)[0]) + 1  # Fibres without splitting
            Fibre_pos = Fibre_pos[FullFibres[:] - 1, :]
            Vec_mem = Vec_mem[FullFibres[:] - 1, :]
            N_fibre -= (CountersQuart + CountersHalf)
            N_fibre_real = N_fibre
            Fibres1Ind = (num.where(Fibre_pos[:, 4] == 0)[0]) + 1  # Fibre 1 indices
            Fibres2Ind = (num.where(Fibre_pos[:, 4] == 1)[0]) + 1  # Fibre 2 indices
            Vol_fibre_1 = num.sum((num.pi * Fibre_pos[Fibres1Ind[:] - 1, 6 - 1] ** 2) / A_total)
            A_fibre_2 = num.sum((num.pi * Fibre_pos[Fibres2Ind[:] - 1, 6 - 1] ** 2))
            if DISTMIN[1] < 0.: #if voids can overlap with fibers, recalculate the void volume fraction
                for i in Fibres2Ind:
                    x = Fibre_pos[i - 1, 1]
                    y = Fibre_pos[i - 1, 2]
                    r = Fibre_pos[i -1, 5]
                    A_overlap = f_area_voids_overlap(x, y, r, N_fibre, Fibre_pos)
                    A_fibre_2 = A_fibre_2 - A_overlap
            Vol_fibre_2 = A_fibre_2 / A_total
            Vol_fibre = Vol_fibre_1 + Vol_fibre_2
            # N_fibre_1=0
            # N_fibre_2=0

            # Re_start=1
            # break #If there is a quarter or a halved fibre with incorrect pairs, re-start the model (possible bug)
        print('Current fibre 1 and 2 volume achieved: ', Vol_fibre_1, Vol_fibre_2)
        #Actualize the Void volume fraction in case some of them overlap:
        if DISTMIN[1] < 0.:  # if voids can overlap with fibers, recalculate the void volume fraction
            Fibres2Ind = (num.where(Fibre_pos[:, 4] == 1)[0])   # Fibre 2 indices
            A_fibre_2 = num.sum((num.pi * Fibre_pos[Fibres2Ind[:], 5] ** 2))
            for i in Fibres2Ind:
                x = Fibre_pos[i, 1]
                y = Fibre_pos[i, 2]
                r = Fibre_pos[i, 5]
                A_overlap = f_area_voids_overlap(x, y, r, N_fibre, Fibre_pos)
                print('A_overlap: ', A_overlap)
                A_fibre_2 = A_fibre_2 - A_overlap
            Vol_fibre_2 = A_fibre_2 / A_total
        #
        print('Current fibre volume achieved: ', Vol_fibre)
        print('Current fibre 1 and 2 volume achieved: ', Vol_fibre_1, Vol_fibre_2)
        #
        Vol_type_fibre_req =  Fibre_type_1*Vol_fibre_req
        Dif_V_fibre = abs(Vol_type_fibre_req - Vol_fibre_1) / Vol_type_fibre_req
        Vol_type_void_req =  Vol_fibre_req - Vol_type_fibre_req
        if Vol_type_void_req != 0.0:
            Dif_V_void  = abs(Vol_type_void_req - Vol_fibre_2) / Vol_type_void_req
        else:
            Dif_V_void = abs(Vol_type_void_req - Vol_fibre_2)
        #
        N_cycles += 1
    #
    ###########################################################################
    # Display Miscellaneous Information                                       #
    ###########################################################################

    if Dif_V_fibre >= Error_V_fibres or Dif_V_void >= Error_V_voids:
        print('##############################################################')
        print('Fibre Volume Fraction NOT REACHED')
        print('Error fibre volume fraction [%]: ', Dif_V_fibre * 100)
        print('Error voids volume fraction [%]: ', Dif_V_void * 100)
        status = 0  # Since the volume was not achieved, a new distribution wil be generated
    else:
        print('##############################################################')
        print('Random Distribution of Fibres COMPLETED')
        print('Number of Attempts: ', N_attempts)
        print('Number of fibres: ', N_fibre)
        print('Number of complete fibres: ', N_fibre_real)
        print('Achieved total Volume: ', Vol_fibre)
        print('Achieved Fibre Volume: ', Vol_fibre_1)
        print('Error in fibre Volume Fraction [%]: ', Dif_V_fibre * 100)
        print('Achieved Void Volume: ', Vol_fibre_2)
        print('Error in voids Volume Fraction [%]: ', Dif_V_void * 100)
        status = 1

    return (status, N_fibre, Fibre_pos, A_total, a, b)
