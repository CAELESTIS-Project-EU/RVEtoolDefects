#Import libraries
import numpy as num
from numba import jit
#Import local libraries
from .Rand_uSTRU_f_overlap import f_overlap, f_overlap_min
from .Rand_uSTRU_f_overlap import f_boundary, f_close_to_boundary

@jit(cache=True, nopython=True)
def Rand_Per_uSTRU_SecHeur(IDlayerVect,Hybrid_type,Xmax,Xmin,Ymax,Ymin,Square_size,Square_inc,a,b,R,N_fibre,Fibre_pos,DISTMIN, cluster_fibres, Vec_mem,NbundlesRa,BundZoneFtEnd,Sec_heur_inter_intra,Vol_fibre_1,Vol_fibre_2,Fibre_type_1,Vol_fibre):
    '''
    Python function to perform the second Heuristic approach proposed by Melro et al.
    With this function, the fibres on the outskirts are moved and compacted for
    generating matrix rich regions

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    IDlayerVect : float32 numpy array of shape (N_fibre, )
            Gives the layer at which each fibre belongs to in interlayer hybrids
    Hybrid_type : integer
            Determines the hybrid type to generate (intrayarn, interlayer or
            intralayer)
    Xmax : float32 numpy array of shape(n, ), where n is the number of regions
           in the RVE: layers, bundles or a single region for an intrayarn
           hybrid or a non-hybrid composite
           Contains the maximum X coordinate
    Xmin : float32 numpy array of shape(n, ), where n is the number of regions
           in the RVE: layers, bundles or a single region for an intrayarn
           hybrid or a non-hybrid composite
           Contains the minimum X coordinate
    Ymax : float32 numpy array of shape(n, ), where n is the number of regions
           in the RVE: layers, bundles or a single region for an intrayarn
           hybrid or a non-hybrid composite
           Contains the maximum Y coordinate
    Ymin : float32 numpy array of shape(n, ), where n is the number of regions
           in the RVE: layers, bundles or a single region for an intrayarn
           hybrid or a non-hybrid composite
           Contains the minimum Y coordinate
    Square_size : float
            Initial size of the square for 2nd heuristic
    Square_inc : float
            Square size increment for 2nd heuristic
    a : float
            Width of the generated RVE
    b : float
            Height of the generated RVE
    R : float
            Fibre radius
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    DISTMIN : array [0,3]
            Minimum distance multiplier between: [fibres, fibre-void, vois]
    cluster_fibres : numba dict
            Dictionary with the position where there must be a fiber cluster and the minimum position between them
    Vec_mem : float32 numpy array of shape (N_fibre,3)
            Used for the 1st heuristic
    NbundlesRa : integer
            Defines the number of bundles in an intralayer hybrid
    BundZoneFtEnd : numpy array of shape (NbundlesRa,NbundlesRa)
            Defines the fibre population that occupies each bundle in the RVE
    Sec_heur_inter_intra : integer
            Determines whether the 2nd heuristic is applied when the volum
            fraction is already reached.
    Vol_fibre_1 : float
            Type 1 fibre volume fraction
    Vol_fibre_2 : float
            Type 2 fibre volume fraction
    Fibre_type_1 : float
            Amount of type 1 fibres in respect to the overal
            fibre volume fraction.
    Vol_fibre : float
            Overall fibre volume fraction

    Kwargs
    -----
        none

    Return
    --------
    Square_size : float
            Size of the square for the next iteration of the 2nd heuristic
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    Vec_mem : float32 numpy array of shape (N_fibre,N_change)
            Determines the neighbour not to use for moving the fibres in the first
            heuristic

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
        File "Rand_uSTRU_f_HardCoreModel.py"

    Program calls
    -----
        File "Rand_uSTRU_f_overlap.py": f_overlap(...) and f_overlap_min(...) functions
    '''

    print('2n Heuristic')
    
    fibre_jump = 0 #Threshold to jump in the loop, if a quarter of fibre was previously treated
    if Sec_heur_inter_intra==1: #If this option is used, then check if the required volume of a fibre population was reached
        if Vol_fibre_1>Fibre_type_1*(Vol_fibre): #Then fibres of type 1 are already well placed, do not move them using this heuristic to avoid generating large and unrealistic matrix rich regions
            Jump_fibres_1=1
        elif Vol_fibre_2>(1-Fibre_type_1)*(Vol_fibre): #Then fibres of type 1 are already well placed, do not move them using this heuristic to avoid generating large and unrealistic matrix rich regions
            Jump_fibres_2=1
    else:
        Jump_fibres_1=0
        Jump_fibres_2=0
        
    for i in range(1,N_fibre+1): #Loop on fibres. Original did it by two to two. Changed this.
        if i>N_fibre:
            break
        
        if fibre_jump != 0: #For fibres in the vertex only one is moved, the other ones are jumped by the loop.
            fibre_jump -= 1
            continue
        
        #Get data of fibre i:
        XC_i=Fibre_pos[i-1,1] #X coordinate
        YC_i=Fibre_pos[i-1,2] #Y coordinate
        Rf_i=Fibre_pos[i-1,6-1] #Fibre radius
        Ft_i=Fibre_pos[i-1,4] #Fibre type
        
        if Sec_heur_inter_intra==1:
            if Ft_i==0 and Jump_fibres_1==1: #Since the volume of fibres 1 is already reached, do not apply this heuristic to them
                continue
            elif Ft_i==1 and Jump_fibres_2==1: #Same in the case it occurs with fibres of type 2
                continue

        if Hybrid_type==2 and (NbundlesRa % 2) == 0: #If an intralayer hybrid with even number of bundles is generated then
            if Fibre_pos[i-1,4-1] == 2 or Fibre_pos[i-1,4-1] == 4: #If the fibre i is in an edge or vertex:
                continue #Just leave it where it is and do not move it. This is done to aviod fibres entering in bundles where they should not be. 
                #This should be improved in the future so that the fibre is only not moved when it does only move towards a wrong bundle
        
        #Now, the region where the fibre i is placed in the RVE is checked. The region will affect how the fibre is moved.
        if Hybrid_type==0: #Intrayarn hybrid
            a_fib=Xmax[1-1]-Xmin[1-1] #The a_fib variable defines the total width of the region where the fibre is placed. Thus, this corresponds to the RVE width in intrayarn hybrids.
            Xoff=Xmin[1-1] #The Xoff variable it is then used to obtain the corresponding outskirt area where the fibre belongs to.
            b_fib=Ymax[1-1]-Ymin[1-1] #The b_fib variable defines the total height of the region where the fibre is placed. Thus, this corresponds to the RVE height in intrayarn hybrids.
            Yoff=Ymin[1-1] #The Yoff variable it is then used to obtain the corresponding outskirt area where the fibre belongs to.
        elif Hybrid_type==1: #Interlayer hybrid
            #First of all, check at which region (ply) of the RVE the fibre is located:
            for Ind in range(1, Xmax.shape[0]+1):
                if (XC_i<=Xmax[Ind-1]) and (XC_i>Xmin[Ind-1]):
                    Position=Ind
                    a_fib=Xmax[Position-1]-Xmin[Position-1] #X longitude of the layer where the fibre is placed
                    Xoff=Xmin[Position-1] #Corresponding offset used to calculate the outskirts where the fibre is placed
                    break #NOTE: In fact this pace of code should be simplified, a_fib and Xoff shoudl always be the same wince all plies have the same width.
                        
            for Ind in range(1, Ymax.shape[0]+1):
                if (YC_i<=Ymax[Ind-1]) and (YC_i>Ymin[Ind-1]):
                    Position=Ind
                    if IDlayerVect[Ind-1]!=Ft_i: #Fibre belongs to a different ply than the one it should be. May be the next ply or the previous one. Let's check.
                        if YC_i<(Ymin[Ind-1]+(Ymax[Ind-1]-Ymin[Ind-1])/2): #Belongs to previous
                            Position=Ind-1
                        elif YC_i>(Ymin[Ind-1]+(Ymax[Ind-1]-Ymin[Ind-1])/2): #Belongs to next
                            Position=Ind+1
                            
                    b_fib=Ymax[Position-1]-Ymin[Position-1] #Thickness of the ply where the fibre is/should be placed
                    Yoff=Ymin[Position-1] #Offset used later to determine the square region, taking into account the ply
                    break
        elif Hybrid_type==2: #Intralayer hybri
            #First of all, check at which region of the RVE the fibre is located:
            for Ind in range(1, Xmax.shape[0]+1):
                for Ind2 in range(1, Ymax.shape[0]+1):
                    if (XC_i<=Xmax[Ind-1]) and (XC_i>Xmin[Ind-1]) and (YC_i<=Ymax[Ind2-1]) and (YC_i>Ymin[Ind2-1]):
                        PositionX=Ind
                        PositionY=Ind2
                        if BundZoneFtEnd[PositionX-1,PositionY-1]!=Ft_i: #Finbre belongs to a different bundle. May be the next bundle or the previous. Let's check.
                            if XC_i<(Xmin[Ind-1]+(Xmax[Ind-1]-Xmin[Ind-1])/2): #Belongs to previous
                                PositionX=Ind-1
                            elif XC_i>(Xmin[Ind-1]+(Xmax[Ind-1]-Xmin[Ind-1])/2): #Belongs to next
                                PositionX=Ind+1
                            if YC_i<(Ymin[Ind2-1]+(Ymax[Ind2-1]-Ymin[Ind2-1])/2): #Belongs to previous
                                PositionY=Ind2-1
                            elif YC_i>(Ymin[Ind2-1]+(Ymax[Ind2-1]-Ymin[Ind2-1])/2): #Belongs to next
                                PositionY=Ind2+1
                            
                        a_fib=Xmax[PositionX-1]-Xmin[PositionX-1] #X longitude of the bundle where the fibre is placed
                        Xoff=Xmin[PositionX-1] #Offset used later to determine the square region
                        b_fib=Ymax[PositionY-1]-Ymin[PositionY-1] #Y longitude of the bundle where the fibre is placed
                        Yoff=Ymin[PositionY-1] #Offset used later to determine the square region
                        break
                
        #Determine the size of the square that affects fibre i
        Square_sizeX=Square_size
        Square_sizeY=Square_size
        if (Square_sizeX > a_fib/2-R):
            Square_sizeX=a_fib/2-R
        if (Square_sizeY > b_fib/2-R):
            Square_sizeY=b_fib/2-R
        
        #Check where the fibre is in relation with the square. According to the position, the fibre is stirred a different angle, always towards the square and away of the edges of the region.
        SqRegion=0
        if XC_i-Xoff < Square_sizeX and YC_i-Yoff > Square_sizeY and YC_i-Yoff < b_fib-Square_sizeY: #If left of square
            PiList=num.arange(-num.pi/2,(num.pi/2)+(num.pi/90),num.pi/90)
            SqRegion=1
        elif XC_i-Xoff > a_fib-Square_sizeX and YC_i-Yoff > Square_sizeY and YC_i-Yoff < b_fib-Square_sizeY: #Right
            PiList=num.arange(num.pi/2,(1.5*num.pi)+(num.pi/90),num.pi/90)
            SqRegion=2
        elif YC_i-Yoff < Square_sizeY and XC_i-Xoff > Square_sizeX and XC_i-Xoff < a_fib-Square_sizeX: #Bottom 
            PiList=num.arange(0,(num.pi)+(num.pi/90),num.pi/90)
            SqRegion=3
        elif YC_i-Yoff > b_fib-Square_sizeY and XC_i-Xoff > Square_sizeX and XC_i-Xoff < a_fib-Square_sizeX: #Top
            PiList=num.arange(-num.pi,0.0+(num.pi/90),num.pi/90)
            PiList[-1]=0.0
            SqRegion=4
        elif XC_i-Xoff < Square_sizeX and YC_i-Yoff < Square_sizeY: #Left bottom
            PiList=num.arange(0,(num.pi/2)+(num.pi/90),num.pi/90)
            SqRegion=5
        elif XC_i-Xoff > a_fib-Square_sizeX and YC_i-Yoff < Square_sizeY: #Right bottom
            PiList=num.arange(num.pi/2,(num.pi)+(num.pi/90),num.pi/90)
            SqRegion=6
        elif XC_i-Xoff > a_fib-Square_sizeX and YC_i-Yoff > b_fib-Square_sizeY: #Right top
            PiList=num.arange(-num.pi,(-num.pi/2)+(num.pi/90),num.pi/90)
            SqRegion=7
        elif XC_i-Xoff < Square_sizeX and YC_i-Yoff > b_fib-Square_sizeY: #Left top
            PiList=num.arange(-num.pi/2,(0.0)+(num.pi/90),num.pi/90)
            PiList[-1]= 0
            SqRegion=8
        
        MIN = a*2 #Initiate a minimum distance
        THETA_MIN = 100 #Angle to stir the fibre
        RAD = 0.75*Rf_i #Possible length to stir the fibre
        GO = 0 #Flag
        
        #Now find the angle in PiList that most reduces the gap between fibre i and any other neighbour.
        #Note: the angles are chosen previously so that the fibres are moved away of the edges and vertices
        while RAD != 0 and GO == 0:
            for j in PiList:
                X_TMP = XC_i + RAD*num.cos(j) #New possible position, according to the stir length Rad and the angle j
                Y_TMP = YC_i + RAD*num.sin(j)
                check,dist = f_overlap_min(X_TMP,Y_TMP,i,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN,a,cluster_fibres)
                check_boundary = f_close_to_boundary(X_TMP, Y_TMP, Rf_i, a,
                                            b)  # Check if the fibre is very close to a boundary
                if check == 0 and check_boundary == 0 and dist < MIN:
                    GO = 1 #If it does not overlap, then stop, and save the distance, and the angle we found as THETA_MIN
                    MIN = dist
                    THETA_MIN = j

            if GO == 0: #If however, there was no angle found with no overlap, then we change RAD to a smaller value and try again, until RAD is zero
                RAD = RAD - 0.25*Rf_i
        
        if THETA_MIN != 100 and SqRegion!=0: #If the while loop found an angle to "move/stir" the fibre with no overlap and the fibre was outside the square then
            X_TMP = XC_i + RAD*num.cos(THETA_MIN) #New possible coordinates according to the angle found and the stirring length
            Y_TMP = YC_i + RAD*num.sin(THETA_MIN)
            if i != N_fibre:
                if (((num.abs(XC_i - Fibre_pos[i+1-1,2-1])) <= (1e-08 + 1e-05 * num.abs(Fibre_pos[i+1-1,2-1]))) == 1) or (((num.abs(YC_i - Fibre_pos[i+1-1,3-1])) <= (1e-08 + 1e-05 * num.abs(Fibre_pos[i+1-1,3-1]))) == 1): #Check wether the pair of fibre i is the next or previous fibre, if fibre i has a pair of course
                    ics = 1 #Then the pair is next fibre
                else:
                    ics = -1 #Then the pair is previous fibre

            else: 
                ics = -1
                    
            if (X_TMP >= Rf_i and X_TMP <= a-Rf_i and Y_TMP >= Rf_i and Y_TMP <= b-Rf_i): #Fibre moves to domain 
                Fibre_pos[i-1,2-1] = X_TMP  #Update coordinates
                Fibre_pos[i-1,3-1] = Y_TMP
                         
                if Fibre_pos [i-1,4-1] == 2: #If the fibre was half we delete the pair (because now it becomes a full fibre)
                    Fibre_pos[i-1,4-1] = 0 
                    N_fibre -= 1
                    #IndexFibre=num.concatenate((num.arange(0,i+ics-1),num.arange(i+ics,Fibre_pos.shape[0])))
                    IndexFibre=num.concatenate((num.arange(0,i+ics),num.arange(i+ics,Fibre_pos.shape[0])))
                    #indexMem=num.concatenate((num.arange(0,i+ics-1),num.arange(i+ics,Vec_mem.shape[0])))
                    Fibre_pos=Fibre_pos[IndexFibre,:]
                    print('--Jorge1',len(Fibre_pos))
                    #Vec_mem=Vec_mem[indexMem,:]
                    Vec_mem=Vec_mem[IndexFibre,:]
                elif Fibre_pos [i-1,4-1] == 4: #If the fibre was a quarter, then delete the remaining three parts
                    Fibre_pos[i-1,4-1] = 0
                    N_fibre -= 3
                    
                    for QuarID in range(1,4):
                        Del=(num.where(Fibre_pos[:,3] == 4)[0]) #Succesive 3 pairs to delete
                        #Index=num.concatenate((num.arange(0,Del[0]),num.arange(Del[0]+1,Fibre_pos.shape[0])))
                        Index=num.concatenate((num.arange(0,Del[0]),num.arange(Del[0],Fibre_pos.shape[0])))
                        #indexMem=num.concatenate((num.arange(0,Del[0]),num.arange(Del[0]+1,Vec_mem.shape[0])))
                        Fibre_pos=Fibre_pos[Index,:]
                        print('--Jorge2',len(Fibre_pos))
                        #Vec_mem=Vec_mem[indexMem,:]
                        Vec_mem=Vec_mem[Index,:]
                    
                continue #Go to next fibre
        
            elif (X_TMP >= Rf_i and X_TMP <= a-Rf_i and (Y_TMP < Rf_i or Y_TMP > b-Rf_i)) or (Y_TMP >= Rf_i and Y_TMP <= b-Rf_i and (X_TMP < Rf_i or X_TMP > a-Rf_i)): #If fibre is moved to an edge
                if Fibre_pos [i-1,4-1] == 0:
                    continue #Note that in this condition, a full fibre can't be considered since we are moving the fibres away from edges!
                
                #Check where is the pair of fibre i
                if Y_TMP < Rf_i: #Fibre is at bottom edge
                    marginY=b #Pair is at top
                    marginX=0
                elif Y_TMP > b-Rf_i: #Fibre is at top edge
                    marginY=-b #Pair is at bottom
                    marginX=0
                if X_TMP < Rf_i: #Fibre is at left edge
                    marginX=a #Pair is at right
                    marginY=0
                elif X_TMP > a-Rf_i: #Fibre is at right edge
                    marginX=-a #Pair is at left
                    marginY=0
                    
                check = f_overlap(X_TMP+marginX,Y_TMP+marginY,i+ics,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN,cluster_fibres)
                check_boundary = f_boundary(X_TMP+marginX,Y_TMP+marginY, Rf_i, a,
                                            b)  # Check if the fibre is in a boundary very small
                if check == 0 and check_boundary == 0: #If the pair may be moved, update all
                    Fibre_pos[i-1,2-1] = X_TMP 
                    Fibre_pos[i-1,3-1] = Y_TMP
                    Fibre_pos[i+ics-1,2-1] = X_TMP+marginX 
                    Fibre_pos[i+ics-1,3-1] = Y_TMP+marginY
                    Fibre_pos[i+ics-1,5-1]=Ft_i #ft of pair
                    Fibre_pos[i+ics-1,6-1]=Rf_i #Radius of pair
                    
                    #Note that the fibre "i" could not be "full" since a full fibre is not stirred here to an edge.
                    if Fibre_pos [i-1,4-1] == 2: #If the fibre i was a half, put the pair as a half too
                        Fibre_pos[i+ics-1,4-1] = 2
                    elif Fibre_pos [i-1,4-1] == 4: #If fibre i was a quarter, put the pair as a half and delete the other two parts
                        Fibre_pos[i-1,4-1] = 2
                        Fibre_pos[i+ics-1,4-1] = 2 
                        N_fibre -= 2
                        
                        for QuarID in range(1,3):
                            Del=(num.where(Fibre_pos[:,3] == 4)[0]) #Succesive 3 pairs to delete
                            FibDel=Del[0]
                            Index=num.concatenate((num.arange(0,FibDel),num.arange(FibDel+1,Fibre_pos.shape[0])))
                            #indexMem=num.concatenate((num.arange(0,FibDel),num.arange(FibDel+1,Vec_mem.shape[0])))
                            
                            Fibre_pos=Fibre_pos[Index,:]
                            print('--Jorge3',len(Fibre_pos))
                            #Vec_mem=Vec_mem[indexMem,:]
                            Vec_mem=Vec_mem[Index,:]
                        
                    continue
            elif ((X_TMP < Rf_i or X_TMP > a-Rf_i) and Y_TMP < Rf_i) or ((X_TMP > a-Rf_i or X_TMP < Rf_i) and Y_TMP > b-Rf_i): #Fibre is at a vertex
                if Fibre_pos[i-1,4-1] == 4: #Only accept this case for a quarter fibre (we won't convert a half or a full fibre into a quarter)
                    if X_TMP < Rf_i and Y_TMP < Rf_i: #Fibre at bottom-left vertex
                        marginX=a 
                        marginY=b
                        MaxDist=num.sqrt((X_TMP)**2+(Y_TMP)**2) #Max distance allowed for fibre centre to have 4 quartes
                    elif X_TMP > a-Rf_i and Y_TMP < Rf_i: #Fibre is at bottom-right vertex
                        marginX=-a
                        marginY=b
                        MaxDist=num.sqrt((X_TMP-a)**2+(Y_TMP)**2) #bottom right
                    elif X_TMP > a-Rf_i and Y_TMP > b-Rf_i: #Fibre is at top-right vertex
                        marginX=-a
                        marginY=-b
                        MaxDist=num.sqrt((X_TMP-a)**2+(Y_TMP-b)**2) #top right
                    elif X_TMP < Rf_i and Y_TMP > b-Rf_i: #Fibre is at top left
                        marginX=a
                        marginY=-b
                        MaxDist=num.sqrt((X_TMP)**2+(Y_TMP-b)**2)
                    
                    if MaxDist<Rf_i: #Security distance to make sure there are really 4 neighbours
                        check = f_overlap(X_TMP,Y_TMP+marginY,i+1,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres)
                        check_boundary = f_boundary(X_TMP, Y_TMP + marginY, Rf_i, a,
                                                    b)  # Check if the fibre is in a boundary very small
                        if check == 0 and check_boundary == 0:
                            check = f_overlap(X_TMP+marginX,Y_TMP,i+2,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres)
                            check_boundary = f_boundary(X_TMP+marginX, Y_TMP, Rf_i, a,
                                                        b)  # Check if the fibre is in a boundary very small
                            if check == 0 and check_boundary == 0:
                                check = f_overlap(X_TMP+marginX,Y_TMP+marginY,i+3,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres)
                                check_boundary = f_boundary(X_TMP+marginX, Y_TMP+marginY, Rf_i, a,
                                                            b)  # Check if the fibre is in a boundary very small
                                if check == 0 and check_boundary == 0: #If all three parts may be moved then update all
                                    Fibre_pos[i-1,2-1] = X_TMP 
                                    Fibre_pos[i-1,3-1] = Y_TMP
                                    Fibre_pos[i-1,4-1] = 4
                                    Fibre_pos[i+1-1,2-1] = X_TMP 
                                    Fibre_pos[i+1-1,3-1] = Y_TMP+marginY
                                    Fibre_pos[i+1-1,4-1] = 4
                                    Fibre_pos[i+1-1,5-1]=Ft_i
                                    Fibre_pos[i+1-1,6-1]=Rf_i 
                                    Fibre_pos[i+2-1,2-1] = X_TMP+marginX 
                                    Fibre_pos[i+2-1,3-1] = Y_TMP
                                    Fibre_pos[i+2-1,4-1] = 4
                                    Fibre_pos[i+2-1,5-1]=Ft_i
                                    Fibre_pos[i+2-1,6-1]=Rf_i 
                                    Fibre_pos[i+3-1,2-1] = X_TMP+marginX 
                                    Fibre_pos[i+3-1,3-1] = Y_TMP+marginY
                                    Fibre_pos[i+3-1,4-1] = 4
                                    Fibre_pos[i+3-1,5-1]=Ft_i 
                                    Fibre_pos[i+3-1,6-1]=Rf_i 
    
                    fibre_jump = 3 #Now jump the three next fibres
                    continue
                        
    Square_size += Square_inc #Increase square size
        
    return(Square_size,N_fibre,Fibre_pos,Vec_mem)
