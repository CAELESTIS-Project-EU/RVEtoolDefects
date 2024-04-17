# Import libraries
import numpy as num
from numba import jit
#Import local libraries


@jit(cache=True, nopython=True)
def f_overlap(X_TMP,Y_TMP,fibre2test,r,ft,N_fibre,Fibre_pos,DISTMIN, cluster_fibres):
    '''
    The Python function checks if a fibre overlaps any other fibre in
    the RVE

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    X_TMP : float
            Possible X coordinate of the fibre to check
    Y_TMP : float
            Possible Y coordinate of the fibre to check
    fibre2test : integer
            Identity of the fibre to check
    r : float
            Fibre radius of the fibre to check
    ft : float
            Fibre type
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    DISTMIN : array [0,3]
            Minimum distance multiplier between: [fibres, fibre-void, voids]
    cluster_fibres : numba dict
            Dictionary with the position where there must be a fiber cluster and the minimum position between them

    Kwargs
    -----
        none

    Return
    --------
    fibre_overlap : integer
            Determines if overlap occurs or not (0: no, 1: yes)

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
        File "Rand_uSTRU_f_HardCoreModel.py", "Rand_uSTRU_f_FirstHeur.py", "Rand_uSTRU_f_SecHeur.py"

    Program calls
    -----
        none
    '''

    fibre_overlap = 0 #Flag to know if overlap happens or not (0=does not happen, 1=happens)
    for k in range(1,N_fibre+1):
        if k == fibre2test: #If the fibre k is itself, continue
            continue

        #Determine the value of the distmin according to the type of fibres
        if Fibre_pos[k - 1][4] == 0. and ft == 0.:
            Distmin_ = DISTMIN[0]
        elif Fibre_pos[k - 1][4] == 1. and ft == 0. or Fibre_pos[k - 1][4] == 0. and ft == 1.:
            Distmin_ = DISTMIN[1]
        elif Fibre_pos[k - 1][4] == 1. and ft == 1.:
            Distmin_ = DISTMIN[2]

        if cluster_fibres == None:
            pass
        else:
            for cluster_number in range(0, len(cluster_fibres['x'])):
                if X_TMP + r >= cluster_fibres['x'][cluster_number][0] and X_TMP - r <= \
                        cluster_fibres['x'][cluster_number][1] and Y_TMP + r >= cluster_fibres['y'][cluster_number][
                    0] and Y_TMP - r <= cluster_fibres['y'][cluster_number][1]:
                    # if is a void, it can be inside a fibre cluster
                    if ft == 1.:
                        fibre_overlap = 1
                        break
                    # if is a fibre, the distance is lower
                    else:
                        Distmin_ = cluster_fibres['dist'][cluster_number][0]

        DISTMIN_2=Fibre_pos[k-1,6-1]+r+(Distmin_)*(Fibre_pos[k-1,6-1]+r)/2 #Possible min distance
        xlim0 = X_TMP - 4*DISTMIN_2 #Limits
        xlim1 = X_TMP + 4*DISTMIN_2
        ylim0 = Y_TMP - 4*DISTMIN_2
        ylim1 = Y_TMP + 4*DISTMIN_2
        xx = Fibre_pos[k-1,2-1]
        yy = Fibre_pos[k-1,3-1]
        if xx > xlim0 and xx < xlim1 and yy > ylim0 and yy < ylim1:
            new_dist = num.sqrt((xx-X_TMP)**2 + (yy-Y_TMP)**2) #Distance between both
            if new_dist < DISTMIN_2: #if smaller than the minimum, there is overlap, else no.
                fibre_overlap = 1
                break

    return(fibre_overlap)


@jit(cache=True, nopython=True)
def f_overlap_min(X_TMP,Y_TMP,fibre2test,r,ft,N_fibre,Fibre_pos,DISTMIN,a, cluster_fibres):
    '''
    The Python function checks if a fibre overlaps any other fibre in
    the RVE and calculates the minimum distance between each fibre and
    the closest neighbour. This is the same function as the previous
    one, but with an extra term.

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    X_TMP : float
            Possible X coordinate of the fibre to check
    Y_TMP : float
            Possible Y coordinate of the fibre to check
    fibre2test : integer
            Identity of the fibre to check
    r : float
            Fibre radius of the fibre to check
    ft : float
            Fibre type
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates
    DISTMIN : array [0,3]
            Minimum distance multiplier between: [fibres, fibre-void, voids]
    a : float
            RVE width
    cluster_fibres : numba dict
            Dictionary with the position where there must be a fiber cluster and the minimum position between them

    Kwargs
    -----
        none

    Return
    --------
    fibre_overlap : integer
            Determines if overlap occurs or not (0: no, 1: yes)
    Min : float
            Distance between the fibre and the closest neighbour

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
        File "Rand_uSTRU_f_SecHeur.py"

    Program calls
    -----
        none
    '''

    fibre_overlap = 0 #Flag to know if overlap happens or not (0=does not happen, 1=happens)
    Min = a*2
    for k in range(1,N_fibre+1):
        if k == fibre2test: #If the fibre k is itself, continue
            continue

        # Determine the value of the distmin according to the type of fibres
        if Fibre_pos[k - 1][4] == 0. and ft == 0.:
            Distmin_ = DISTMIN[0]
        elif Fibre_pos[k - 1][4] == 1. and ft == 0. or Fibre_pos[k - 1][4] == 0. and ft == 1.:
            Distmin_ = DISTMIN[1]
        elif Fibre_pos[k - 1][4] == 1. and ft == 1.:
            Distmin_ = DISTMIN[2]

        if cluster_fibres == None:
            pass
        else:
            for cluster_number in range(0, len(cluster_fibres['x'])):
                if X_TMP + r >= cluster_fibres['x'][cluster_number][0] and X_TMP - r <= \
                        cluster_fibres['x'][cluster_number][1] and Y_TMP + r >= cluster_fibres['y'][cluster_number][
                    0] and Y_TMP - r <= cluster_fibres['y'][cluster_number][1]:
                    # if is a void, it can be inside a fibre cluster
                    if ft == 1.:
                        fibre_overlap = 1
                        break
                    # if is a fibre, the distance is lower
                    else:
                        Distmin_ = cluster_fibres['dist'][0][0]

        DISTMIN_2=Fibre_pos[k-1,6-1]+r+(Distmin_)*(Fibre_pos[k-1,6-1]+r)/2 #Possible min distance
        xlim0 = X_TMP - 4*DISTMIN_2 #Limits
        xlim1 = X_TMP + 4*DISTMIN_2
        ylim0 = Y_TMP - 4*DISTMIN_2
        ylim1 = Y_TMP + 4*DISTMIN_2
        xx = Fibre_pos[k-1,2-1]
        yy = Fibre_pos[k-1,3-1]
        if xx > xlim0 and xx < xlim1 and yy > ylim0 and yy < ylim1:
            new_dist = num.sqrt((xx-X_TMP)**2 + (yy-Y_TMP)**2) #Distance between both
            if new_dist < DISTMIN_2: #if smaller than the minimum, there is overlap, else no.
                fibre_overlap = 1
                # This break here greatly reduces cpu time.
                # However, it causes the stirring angle not to be the minimum
                # in some cases.
                break
                #
            else:
                if new_dist < Min:
                    Min = new_dist

    return(fibre_overlap, Min)


@jit(cache=True, nopython=True)
def f_boundary(X_TMP, Y_TMP, r, RVE_width, RVE_height, tol=0.00035):
    '''
    The Python function checks if a fibre is cut by a boundary and one of the pieces is very small so then
    we could have some problems while meshing it

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    X_TMP : float
            Possible X coordinate of the fibre to check
    Y_TMP : float
            Possible Y coordinate of the fibre to check
    r : float
            Fibre radius of the fibre to check
    RVE_width : float
            Width of the RVE
    RVE_height : float
            Height of the RVE

    Kwargs
    -----
    tol : float
            Minimum distance between the cylinder and the boundary

    Return
    --------
    fibre_boundary : integer
            Determines if the cylinder is very close (distance < tol) )to a boundary (0: no, 1: yes)

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
        File "Rand_uSTRU_f_HardCoreModel.py", "Rand_uSTRU_f_FirstHeur.py", "Rand_uSTRU_f_SecHeur.py"

    Program calls
    -----
        none
    '''

    fibre_boundary = 0 #Flag to know if is in a boundary very small (0=does not happen, 1=happens)

    #fiber in the left
    if (X_TMP + r) <= tol:
        fibre_boundary = 1
    #fiber in the right
    elif (RVE_width - (X_TMP - r)) <= tol:
        fibre_boundary = 1
    #fiber in the bottom
    elif (Y_TMP + r) <= tol:
        fibre_boundary = 1
    #fiber in the top
    elif (RVE_height - (Y_TMP - r)) <= tol:
        fibre_boundary = 1


    # if (X_TMP + r) <= tol or abs(X_TMP - r) <= tol:
    #     fibre_boundary = 1
    # elif (RVE_width - (X_TMP - r)) <= tol or ((X_TMP + r) - RVE_width) <= tol:
    #     fibre_boundary = 1
    # #fiber in the bottom
    # elif (Y_TMP + r) <= tol or abs(Y_TMP - r) <= tol:
    #     fibre_boundary = 1
    # #fiber in the top
    # elif (Y_TMP - r) >= (RVE_height - tol) or (Y_TMP + r) <= (RVE_height + tol):
    #     fibre_boundary = 1

    return(fibre_boundary)


@jit(cache=True, nopython=True)
def f_close_to_boundary(X_TMP, Y_TMP, r, RVE_width, RVE_height, tol=0.00035*1.1):
    '''
    The Python function checks if a full fibre is very close to boundary so the distance within is very small so then
    we could have some problems while meshing it

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    X_TMP : float
            Possible X coordinate of the fibre to check
    Y_TMP : float
            Possible Y coordinate of the fibre to check
    r : float
            Fibre radius of the fibre to check
    RVE_width : float
            Width of the RVE
    RVE_height : float
            Height of the RVE

    Kwargs
    -----
    tol : float
            Minimum distance between the cylinder and the boundary

    Return
    --------
    fibre_boundary : integer
            Determines if the cylinder is very close (distance < tol) )to a boundary (0: no, 1: yes)

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
        File "Rand_uSTRU_f_HardCoreModel.py", "Rand_uSTRU_f_FirstHeur.py", "Rand_uSTRU_f_SecHeur.py"

    Program calls
    -----
        none
    '''

    fibre_boundary = 0 #Flag to know if is in a boundary very small (0=does not happen, 1=happens)

    if X_TMP - r <= tol:
        fibre_boundary = 1
    elif RVE_width - (X_TMP + r) <= tol:
        fibre_boundary = 1
    if Y_TMP - r <= tol:
        fibre_boundary = 1
    elif RVE_height - (Y_TMP + r) <= tol:
        fibre_boundary = 1

    return(fibre_boundary)


@jit(cache=True, nopython=True)
def f_area_voids_overlap(X_TMP,Y_TMP,r, N_fibre, Fibre_pos):
    '''
    The Python function calculates the area of two surposed circles (void + fiber)

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    X_TMP : float
            Possible X coordinate of the fibre to check
    Y_TMP : float
            Possible Y coordinate of the fibre to check
    r : float
            Fibre radius of the fibre to check
    N_fibre : integer
            Total number of fibres
    Fibre_pos : numpy array of shape (n,6) where n is the number of fibres in the RVE
            This corresponds to the matrix of fibres coordinates

    Kwargs
    -----
        none

    Return
    --------
    A_overlap : integer
            Missing area of the void due to overlap with a fiber

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
        File "Rand_uSTRU_f_HardCoreModel.py", "Rand_uSTRU_f_Loop.py"

    Program calls
    -----
        none
    '''

    # Void information
    Ax = X_TMP
    Ay = Y_TMP
    Ar = r
    A_overlap = 0.
    #
    for k in range(0,N_fibre):
        if Fibre_pos[k, 4] == 1: #If the circle is a void continue
            continue
        #
        # Fiber information
        Bx = Fibre_pos[k, 1]
        By = Fibre_pos[k, 2]
        Br = Fibre_pos[k, 5]
        #
        dist = num.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2)  # Distance between both
        if dist < (r+Br): #if smaller than the sum of radius then they overlap so the area must be recalculate
            # https://www.xarg.org/2016/07/calculate-the-intersection-area-of-two-circles/
            #
            #Calculate interesting parameters
            d = dist
            x = (Ar**2 - Br**2 + d**2) / (2*d)
            y = num.sqrt(Ar**2 - x**2)
            #
            area_s1 = Ar**2 * num.arcsin(y/Ar)
            area_s2 = Br**2 * num.arcsin(y/Br)
            area_t1 = y * num.sqrt(Ar**2 - y**2)
            area_t2 = y * num.sqrt(Br**2 - y**2)
            #
            A_intersection = area_s1 + area_s2 - area_t1 - area_t2
            #
            A_overlap = A_overlap + A_intersection

    return(A_overlap)