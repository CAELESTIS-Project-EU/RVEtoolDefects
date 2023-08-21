# RVE_solver

## Overview
This module generates the inputs required to use Alya Multiphysics computational mechanics solver. However, you are welcome to integrate any other computational solver.

## Boundary codes

          2-d                  3-d             

          4   
    o-----------o           o----------o            
    |           |           |\         |\          
    |           |           | \    4   | \           
  1 |           | 2         |  \  5    |  \      
    |           |           |   o------+---o     
    |           |           | 1 |      | 2 |  
    o-----------o           o---+------o   | 
          3                  \  |    6  \  | 
                              \ |   3    \ |
   ^ y                         \|         \| 
   |                            o----------o
   |      x                     
   o----->
    \
    _\/ z 

Boundary codes:

CODE 1: LEFT,  X= 0
CODE 2: RIGHT, X= 1
CODE 3: BOT,   Y= 0
CODE 4: TOP,   Y= 1

CODE 5: BACK,  Z= 0 (only for 3-d)
CODE 6: FRONT, Z= 1 (only for 3-d)


## Periodic Boundary Conditions (PBCs)

The periodic boundary conditions are based on [Garoz et al. 2018](https://doi.org/10.1016/j.compositesb.2018.12.023). For microscale models the PBCs are applied at all faces. 

          2-d                  3-d             

   D             C         D            C
    o-----------o           o----------o            
    |           |           |\         |\          
    |           |           | \        | \           
    |           |           |  \ H     |  \ G     
    |           |           |   o------+---o     
    |           |           |   |      |   |  
    o-----------o           o---+------o   | 
   A             B         A \  |     B \  | 
                              \ |        \ |
   ^ y                         \|         \| 
   |                            o----------o
   |      x                    E            F 
   o----->                     
    \
    _\/ z

     Edges          Vertices\n')
  ------------------------------------------------\n')
  Slave Master    Slave Master\n')
    DC    AB         B     A\n')
    BC    AD         C     A\n')
                     D     A\n')
                     
     Faces           Edges          Vertices
  ------------------------------------------------ 
  Slave Master    Slave Master    Slave Master
   BCGF  ADHE      EF    AB         B     A
                   DC    AB         D     A
                   HG    AB         E     A  
   DHGC  AEFB      BF    AE         C     A
                   DH    AE         H     A
                   CG    AE         F     A
   EFGH  ABCD      BC    AD         G     A
                   EH    AD        
                   FG    AD

## References

D. Garoz, F.A. Gilabert, R.D.B. Sevenois, S.W.F. Spronk, W. Van Paepegem, Consistent application of periodic boundary conditions in implicit and explicit finite element simulations of damage in composites, Composites Part B: Engineering, Volume 168, 2019, Pages 254-266, ISSN 1359-8368, [https://doi.org/10.1016/j.compositesb.2018.12.023](https://doi.org/10.1016/j.compositesb.2018.12.023). 




