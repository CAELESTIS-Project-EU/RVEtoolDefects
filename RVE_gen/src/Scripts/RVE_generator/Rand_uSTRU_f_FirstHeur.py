# Import libraries
import numpy as num
from numba import jit
# Import local libraries
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_overlap import f_overlap
from RVE_gen.src.Scripts.RVE_generator.Rand_uSTRU_f_overlap import f_boundary, f_close_to_boundary

#With this criteria we want to move the fibres closer between them to gain more empty areas to fill them with more fibres
@jit(cache=True, nopython=True)
def Rand_Per_uSTRU_FirstHeur(N_fibre, Fibre_pos, a, b, DISTMIN, cluster_fibres, N_cycles, Vec_mem, N_change, First_Heur_op):
    '''
    Python function to perform the first Heuristic approach proposed by Melro et al.
    With this function, the fibres are moved closer between them to gain more empty
    areas to fill, afterwards, with more fibres.

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    a : float
            Width of the generated RVE
    b : float
            Height of the generated RVE
    DISTMIN : array [0,3]
            Minimum distance multiplier between: [fibres, fibre-void, vois]
    cluster_fibres : numba dict
            Dictionary with the position where there must be a fiber cluster and the minimum position between them
    N_cycles : integer
            Maximum number of cycles that the routine runs before starting all over again
    Vec_mem : float32 numpy array of shape (N_fibre,N_change)
            Determines the neighbour not to use for moving the fibres in the first
            heuristic
    N_change : integer
            Number of cycles before changing criteria on 1st heuristic
    First_Heur_op : integer
            0 = intrayarn and non-hybrid composites use this option as default
            1 = layer-by-layer (interlayer) or Bundle-by-bundle (intralayer)

    Kwargs
    -----
        none

    Return
    --------
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
        File "Rand_uSTRU_f_overlap.py", f_overlap(...) function
    '''
    
    print('1st Heuristic')
    
    fibre_jump = 0 #This flag is to jump some fibres in the next loop. Used to jump the fibres on vertices.
    for i in range(1,N_fibre+1):
        if fibre_jump != 0: #If we did some fibre that was a quarter, we jump the next quarter fibres
            fibre_jump -= 1 
            continue

        if i>N_fibre:
            break

        XC = Fibre_pos[i-1,2-1] #Get XC coordinate of fibre i
        YC = Fibre_pos[i-1,3-1] #Get YC coordinate of fibre i
        Rf_i=Fibre_pos[i-1,6-1] #Get radius of fibre i
        Ft_i=Fibre_pos[i-1,4] #Get type of fibre i
        MIN = a*2 #Value for comparing, at a start is left as a large value
        IMIN = 0 #Fibre identitiy of one of the closest neighbours to fibre i that is used to stir fibre i
        
        for jl in range(1,N_fibre+1): #Loop to all fibres to find the fibre jl to use to stir fibre i
            if i != jl: #If not the same fibre
                if First_Heur_op==1: #Option for interlayer and intralayer composites
                    Ft_jl=Fibre_pos[jl-1,4] #Get type of fibre i
                    if Ft_i!=Ft_jl:
                        continue #If not the same type of fibre, do not use it to move the fibre
                    
                x_delta = num.absolute(Fibre_pos[jl-1,2-1]-XC) #Get the X distance between both fibres
                y_delta = num.absolute(Fibre_pos[jl-1,3-1]-YC) #Get the Y distance between both fibres
                
                #Compare now the distances with a threshold
                #Determine the value of the distmin according to the type of fibres
                if Fibre_pos[jl-1,4] == 0. and Ft_i == 0.:
                    Distmin_ = DISTMIN[0]
                elif Fibre_pos[jl-1,4] == 1. and Ft_i== 0. or Fibre_pos[jl-1,4] == 0. and Ft_i == 1.:
                    Distmin_ = DISTMIN[1]
                elif Fibre_pos[jl-1,4] == 1. and Ft_i == 1.:
                    Distmin_ = DISTMIN[2]

                if (x_delta < (4*(Rf_i+Fibre_pos[jl-1,6-1]+(Distmin_)*(Rf_i+Fibre_pos[jl-1,6-1])/2))) and (y_delta < (4*(Rf_i+Fibre_pos[jl-1,6-1]+(Distmin_)*(Rf_i+Fibre_pos[jl-1,6-1])/2))):
                    DIST_TMP = num.sqrt(x_delta**2 + y_delta**2) #Distance between fibre centers
                    if DIST_TMP < MIN: #If the distance is smaller than the current one known then
                        if N_cycles == 1: #At first iteration stir the fibre to the closest neighbour
                            IMIN = jl #Neighbour fibre identitity
                            MIN = DIST_TMP #Centre-to-centre distance
                            Vec_mem[i-1,2+1-1] = jl #Save identitiy into vector memory
                        elif num.mod(N_cycles,N_change) == 0: #At any num.mod(N_cycles,N_change) == 0, do not stir to the fibre used in previous two cycles
                            if Vec_mem[i-1,2-1] != jl or Vec_mem[i-1,2-1-1] != jl:
                                IMIN = jl
                                MIN = DIST_TMP
                                Vec_mem[i-1,2+1-1] = jl 
                        else: #Else stir to the second most closest neighbour
                            if Vec_mem[i-1,2-1] != jl:
                                IMIN = jl
                                MIN = DIST_TMP
                                Vec_mem[i-1,2+1-1] = jl 

        Delta = num.random.uniform(0,1) #Random number to stir the fibre i
        if IMIN != 0: #If some neighbour was chosen to stir the fibre 
            x_delta = Fibre_pos[IMIN-1,2-1]-XC #Get x distance between fibre i and the fibre IMIN 
            y_delta = Fibre_pos[IMIN-1,3-1]-YC  #Y distance

            # Determine the value of the distmin according to the type of fibres
            if Fibre_pos[IMIN-1,4] == 0. and Ft_i == 0.:
                Distmin_ = DISTMIN[0]
            elif (Fibre_pos[IMIN-1,4] == 1. and Ft_i == 0.) or (Fibre_pos[IMIN-1,4] == 0. and Ft_i == 1.):
                Distmin_ = DISTMIN[1]
            elif Fibre_pos[IMIN-1,4] == 1. and Ft_i == 1.:
                Distmin_ = DISTMIN[2]
            k = 1.0 - ((Rf_i+Fibre_pos[IMIN-1,6-1]+(Distmin_)*(Rf_i+Fibre_pos[IMIN-1,6-1])/2.0)/(num.sqrt(x_delta**2 + y_delta**2))) #A vector
            X_TMP = XC + Delta*k*x_delta #Stir the fibre a distance Delta*k*x_delta (if possible)
            Y_TMP = YC + Delta*k*y_delta #Stir the fibre a distance Delta*k*y_delta (if possible)
            check = f_overlap(X_TMP,Y_TMP,i,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres) #Now, check if it is possible or not
            check_boundary = f_close_to_boundary(X_TMP, Y_TMP, Rf_i, a, b)  # Check if the fibre is very close to a boundary
            if i != N_fibre: #If not the last fibre
                if (((num.abs(XC - Fibre_pos[i+1-1,2-1])) <= (1e-08 + 1e-05 * num.abs(Fibre_pos[i+1-1,2-1]))) == 1) or (((num.abs(YC - Fibre_pos[i+1-1,3-1])) <= (1e-08 + 1e-05 * num.abs(Fibre_pos[i+1-1,3-1]))) == 1): #Check wether the pair of fibre i is the next or the previous fibre, in case fibre i has a pair of course
                    ics = 1 #This is the pair fibre of fibre i. Then, the pair fibre is simply i+ics
                else:
                    ics = -1 
            else:
                ics = -1 #If the fibre does not have a pair, ics=-1 will be produced (and will have no effect)
           
            if check == 0 and check_boundary == 0: #If the fibre does not overlap, then it may be stirred

                if (X_TMP >= Rf_i) and (X_TMP <= a-Rf_i) and (Y_TMP >= Rf_i) and (Y_TMP <= b-Rf_i): #If fibre is moved anywhere in domain
                    Fibre_pos[i-1,2-1] = X_TMP #New XC for fibre i
                    Fibre_pos[i-1,3-1] = Y_TMP #New YC for fibre i
                    #Now, two scenarios may occur. If the fibre i was full before moving, it has remained full, then noting else to do with fibre i.
                    #Otherwise, if the fibre was half, the pair needs to be deleted. Similarly, if it was a quarter, the other 3 quarter fibres must be deleted:
                    if Fibre_pos[i-1,4-1] == 2: #If Fibre i was a pair before being stirred, then we must delete the pair
                        Fibre_pos[i-1,4-1] = 0 #Now the fibre is not a half anymore
                        N_fibre -= 1 #We need to delete the pair that was on the domain. This pair is either the next or the previous fibre to i, which is given by variable ics.
                        #Thus, now we shall delete the fibre in position i+ics.
                        #IndexFibre=num.concatenate((num.arange(0,i+ics-1),num.arange(i+ics,Fibre_pos.shape[0])))
                        IndexFibre=num.concatenate((num.arange(0,i+ics),num.arange(i+ics,Fibre_pos.shape[0])))
                        #indexMem=num.concatenate((num.arange(0,i+ics-1),num.arange(i+ics,Vec_mem.shape[0])))
                        Fibre_pos=Fibre_pos[IndexFibre,:]
                        #Vec_mem=Vec_mem[indexMem,:]
                        Vec_mem=Vec_mem[IndexFibre,:]
                    elif Fibre_pos[i-1,4-1] == 4: #If Fibre i was a quarter, then we need to delete the three remaining parts
                        Fibre_pos[i-1,4-1] = 0
                        N_fibre -= 3
                        
                        for QuarID in range(1,4):
                            Del=(num.where(Fibre_pos[:,3] == 4)[0]) #Succesive 3 pairs to delete
                            #Index=num.concatenate((num.arange(0,Del[0]),num.arange(Del[0]+1,Fibre_pos.shape[0]))) 
                            Index=num.concatenate((num.arange(0,Del[0]),num.arange(Del[0],Fibre_pos.shape[0])))     # BSC
                            #indexMem=num.concatenate((num.arange(0,Del[0]),num.arange(Del[0]+1,Vec_mem.shape[0])))
                            Fibre_pos=Fibre_pos[Index,:]
                            #Vec_mem=Vec_mem[indexMem,:]
                            Vec_mem=Vec_mem[Index,:]
                    continue
                elif (X_TMP >= Rf_i and X_TMP <= a-Rf_i and (Y_TMP < Rf_i or Y_TMP > b-Rf_i)) or (Y_TMP >= Rf_i and Y_TMP <= b-Rf_i and (X_TMP < Rf_i or X_TMP > a-Rf_i)): #If fibre is moved to an edge
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
                    
                    #Now three scenarios may happen again. If the fibre was full, now it becomes a half, and a pair needs to be added. If the fibre was already a half, the position of the pair must be updated.
                    #And finally, if the fibre was a quarter, two fibres must be deleted. 
                    if Fibre_pos[i-1,4-1] == 0:
                        check = f_overlap(X_TMP+marginX,Y_TMP+marginY,i,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres) #Check if the new pair may be placed
                        check_boundary = f_boundary(X_TMP+marginX, Y_TMP+marginY, Rf_i, a, b)  # Check if the fibre is in a boundary very small
                    elif Fibre_pos[i-1,4-1] == 2 or Fibre_pos[i-1,4-1] == 4: #If the fibre i was on and edge or was a quarter
                        check = f_overlap(X_TMP+marginX,Y_TMP+marginY,i+ics,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres) #Check now if the pair can also be moved
                        check_boundary = f_boundary(X_TMP+marginX, Y_TMP+marginY, Rf_i, a,
                                                    b)  # Check if the fibre is in a boundary very small
                    if check == 0 and check_boundary == 0: #If the analog fibre does not overlap, then add the new fibre and update fibre i
                        Fibre_pos[i-1,2-1] = X_TMP #Update XC of fibre i
                        Fibre_pos[i-1,3-1] = Y_TMP #Update YC of fibre i
                        if Fibre_pos[i-1,4-1] == 0: #If fibre i was full before moving, now we need to add the corresponding pair
                            Fibre_pos[i-1,4-1] = 2 #Update AC of fibre i
                            N_fibre += 1 #Add the pair
                            #To add the new fibre, we do a loop to copy all fibres one row later, thus, we can add the new fibre at row i+1-1
                            for jl in range(N_fibre,i+2-1,-1): 
                                Fibre_pos[jl-1,1:] = Fibre_pos[jl-1-1,1:] 
                                Vec_mem[jl-1,0:] = Vec_mem[jl-1-1,0:] 
    
                            Fibre_pos[i+1-1,2-1] = X_TMP+marginX #XC of new pair
                            Fibre_pos[i+1-1,3-1] = Y_TMP+marginY #YC of new pair
                            Fibre_pos[i+1-1,4-1] = 2  #AC of new pair
                            Fibre_pos[i+1-1,5-1]=Ft_i #ft of new pair
                            Fibre_pos[i+1-1,6-1]=Rf_i #Radius of new pair
                        elif Fibre_pos[i-1,4-1] == 2: #If the fibre i was on and edge
                            Fibre_pos[i-1,4-1] = 2
                            Fibre_pos[i+ics-1,4-1] = 2
                            Fibre_pos[i+ics-1,2-1] = X_TMP+marginX #Update data of fibre ics (the pair)
                            Fibre_pos[i+ics-1,3-1] = Y_TMP+marginY
                            Fibre_pos[i+ics-1,5-1]=Ft_i #ft of new fibre
                            Fibre_pos[i+ics-1,6-1]=Rf_i #Radius of new fibre
                        elif Fibre_pos[i-1,4-1] == 4: #If the fibre i was on and edge or was a quarter
                                Fibre_pos[i-1,4-1] = 2
                                Fibre_pos[i+ics-1,4-1] = 2
                                Fibre_pos[i+ics-1,2-1] = X_TMP+marginX #Update data of fibre ics (the pair)
                                Fibre_pos[i+ics-1,3-1] = Y_TMP+marginY
                                Fibre_pos[i+ics-1,5-1]=Ft_i #ft of new fibre
                                Fibre_pos[i+ics-1,6-1]=Rf_i #Radius of new fibre
                                N_fibre -= 2 #And now the fibres not being i neither ics must be deleted:
                                
                                for QuarID in range(1,3):
                                    Del=(num.where(Fibre_pos[:,3] == 4)[0]) #Succesive 3 pairs to delete
                                    FibDel=Del[0]
                                    Index=num.concatenate((num.arange(0,FibDel),num.arange(FibDel+1,Fibre_pos.shape[0])))
                                    #indexMem=num.concatenate((num.arange(0,FibDel),num.arange(FibDel+1,Vec_mem.shape[0])))
                                    Fibre_pos=Fibre_pos[Index,:]
                                    #Vec_mem=Vec_mem[indexMem,:]
                                    Vec_mem=Vec_mem[Index,:]
                            
                        continue
                elif ((X_TMP < Rf_i or X_TMP > a-Rf_i) and Y_TMP < Rf_i) or ((X_TMP > a-Rf_i or X_TMP < Rf_i) and Y_TMP > b-Rf_i): #If fibre is in a vertex
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
                    
                    #Like in the previous conditions, three scenarios again occur here, depending if fibre i was full, was a half or a quarter.
                    #If it was full, then 3 new fibres must be added. If it was half, then 2 new fibres are added. If it was already a quarter, the coordinates are all updated.
                    if MaxDist<Rf_i:
                        check = f_overlap(X_TMP,Y_TMP+marginY,i+1,Rf_i,Ft_i,N_fibre,Fibre_pos,DISTMIN, cluster_fibres) #CHeck if all other 3 quarter parts can also be moved
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
                                if check == 0 and check_boundary == 0: #If true, then update all quarters
                                    if Fibre_pos[i-1,3]==0: #If the fibre was full:
                                        StartFib=i #Start position in Fibre_pos matrix for the 4 vertex fibres
                                        N_fibre += 3 #Add the pairs
                                        for jl in range(N_fibre,i+2-1,-1): #Copy all fibres to allow adding the 3 new fibres
                                            Fibre_pos[jl-1,1:] = Fibre_pos[jl-1-3,1:] 
                                            Vec_mem[jl-1,0:] = Vec_mem[jl-1-3,0:] 
                                    elif Fibre_pos[i-1,3]==2: #If the fibre was half:
                                        if ics==1: #Adjust the start position to be coherent with the already pair of fibre i
                                            StartFib=i
                                        elif ics==-1:
                                            StartFib=i-1
                                    
                                        N_fibre += 2 #Add the two new fibres
                                        for jl in range(N_fibre,StartFib+2-1,-1): #Copy all fibres but leaving space for the two new fibres
                                            Fibre_pos[jl-1,1:] = Fibre_pos[jl-1-2,1:] 
                                            Vec_mem[jl-1,0:] = Vec_mem[jl-1-2,0:] 
                                    elif Fibre_pos[i-1,3]==4: #If the fibre was a quarter:
                                        StartFib=i
                                    
                                    #Now update the coordinates
                                    Fibre_pos[StartFib-1,2-1] = X_TMP 
                                    Fibre_pos[StartFib-1,3-1] = Y_TMP
                                    Fibre_pos[StartFib-1,4-1] = 4
                                    Fibre_pos[StartFib+1-1,2-1] = X_TMP 
                                    Fibre_pos[StartFib+1-1,3-1] = Y_TMP+marginY
                                    Fibre_pos[StartFib+1-1,4-1] = 4
                                    Fibre_pos[StartFib+1-1,5-1]=Ft_i #ft of new fibre
                                    Fibre_pos[StartFib+1-1,6-1]=Rf_i #Radius of new fibre
                                    Fibre_pos[StartFib+2-1,2-1] = X_TMP+marginX
                                    Fibre_pos[StartFib+2-1,3-1] = Y_TMP
                                    Fibre_pos[StartFib+2-1,4-1] = 4
                                    Fibre_pos[StartFib+2-1,5-1]=Ft_i #ft of new fibre
                                    Fibre_pos[StartFib+2-1,6-1]=Rf_i #Radius of new fibre
                                    Fibre_pos[StartFib+3-1,2-1] = X_TMP+marginX 
                                    Fibre_pos[StartFib+3-1,3-1] = Y_TMP+marginY
                                    Fibre_pos[StartFib+3-1,4-1] = 4
                                    Fibre_pos[StartFib+3-1,5-1]=Ft_i #ft of new fibre
                                    Fibre_pos[StartFib+3-1,6-1]=Rf_i #Radius of new fibre
                                    fibre_jump = 3 #The loop will jump the three next fibres (since they have been already moved now)
                                    continue
    
    Vec_mem[:,0:(N_change-1)]=Vec_mem[:,1:N_change] #Move vector memory one cycle
    Vec_mem[:,(N_change-1)]=0.0    
        
    return(N_fibre, Fibre_pos, Vec_mem) 
    
