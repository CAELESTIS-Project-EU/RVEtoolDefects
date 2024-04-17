#Import libraries
import numpy as N
import os
import shutil
import glob
#Import local libraries


#MISCELLANEOUS FUNCTIONS


def delete_fibers_boundary(name):
    '''
    The Python function removes the fibers/voids that are in a boundary of a npz file

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    name : str
            Name of the npz file that must be modified

    Kwargs
    -----
    none

    Return
    --------
    name_new : npz file
            File with all the coordinates of the RVE but without fibers/voids on the boundaries

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
        none

    Program calls
    -----
        none
    '''

    #Load the npz file
    old_npz = N.load(name+'.npz')
    #Convert the file to a dictionary to be modified
    old_npz_dict = dict(old_npz)
    old_Fibre_pos = old_npz['Fibre_pos']
    #Get only the fibers/voids that are not in a boundary
    Fibre_pos=[]
    for i in range(0, len(old_Fibre_pos)):
        if old_Fibre_pos[i][3] == 0.0:
            Fibre_pos.append(old_Fibre_pos[i])
    #Actualize the dictionary
    new_npz_dict = old_npz_dict
    new_npz_dict['Fibre_pos'] = Fibre_pos
    #Save the new npz file without fibers on the boundaries
    N.savez(name+'_no_bounds', **new_npz_dict)


def write_summary(Summary_name, dir_path, Project_name, inp_name, model_name,
                  Fibre_material_sys, Void_material_sys, Matrix_material_sys, Coh_material_sys,
                  mesh, global_seeds, element_size, length, num_elements_length,
                  ff_strain,
                  inner_rectangle=None):
    '''
    The Python function writes a new summary file with all the infroamtion of the model and the numerical simulation

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    Summary_name : str
            Name of the npz file that must be modified
    dir_path : str
            Path of the directory
    Project_name : str
            Name of the project from the Inputs file
    inp_name : str
            Name of the input file (.inp)
    model_name : str
            Name of the Abaqus model
    Fibre_material_sys : str
            Name of the fibre material
    Void_material_sys : str
            Name of the void material
    Matrix_material_sys : str
            Name of the matrix material
    Coh_material_sys : str
            Name of the cohesive material
    global_seeds : boolean
            To define if all the assembly have the same seeds (True) or each part has different mesh sizes (False)
    mesh : str
            Variable to know if the mesh is done part by part or in the assembly
    element_size : Dict
            Dictionary with the information of the elemnet_size for the fibers, matrix and voids
    length : float
            Length of the RVE
    num_elements_length : int
            Number of elements in the length direction
    ff_strain : array of shape (3, 3)
            Far field strain tensor: E11, E12, E13
                                     E21, E22, E23
                                     E31, E32, E33

    Kwargs
    -----
    inner_rectangle : int
            Number of elements in half of the square of the inner rectangle
            Thus: length_square=2*inner_rectangle*element_size

    Return
    --------
    Summary_name : txt file
            File with all the information of the model and the numerical simulation

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
        Abaqus_generator_main.py

    Program calls
    -----
        none
    '''

    #Read the file with all the summary of the model
    for file in os.listdir(dir_path):
        if file.startswith(Project_name) and file.endswith('summary.txt'):
            Summary_file = file
    #
    #Create a new file with the data of the summary file
    #Copy the data of the summary file
    with open(dir_path + '/' + Summary_file, 'r') as f:
        Data = f.read()
    #Add more information about the numerical simulation
    with open(Summary_name, 'w') as f:
        f.write(Data)
        f.write('########################################### \n')
        f.write('DESCRIPTION OF THE NUMERICAL SIMULATION \n')
        f.write('Name of the simulation \n')
        f.write('Input_file_name:               %s\n' % inp_name)
        f.write('Model_name:                    %s\n' % model_name)
        f.write('Materials used \n')
        f.write('Fiber_material:                %s\n' % Fibre_material_sys)
        f.write('Void_material:                 %s\n' % Void_material_sys)
        f.write('Matrix_material:               %s\n' % Matrix_material_sys)
        f.write('Coh_material:                  %s\n' % Coh_material_sys)
        f.write('Mesh \n')
        f.write('Mesh_type:                     %s\n' % mesh)
        f.write('Global_seeds:                  %s\n' % global_seeds)
        f.write('Element_size_fibre:            %s\n' % element_size['element_size_fibre'])
        f.write('Element_size_matrix:           %s\n' % element_size['element_size_matrix'])
        f.write('Element_size_void:             %s\n' % element_size['element_size_void'])
        f.write('Length [mm]:                   %s\n' % length)
        f.write('Element_in_length:             %s\n' % num_elements_length)
        if mesh != 'ASSEMBLY':
            f.write('Inner_rectangle:           %s\n' % inner_rectangle)
        f.write('Load applied \n')
        f.write('Far_field_strain:              %s\n' % ff_strain)
    #


def move_files(path_origin, path_destination, dir_name, list_of_files):
    '''
    The Python function moves the files in a new directory

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    path_origin : str
            Path of the directory where the files are
    path_destination : str
            Path of the directory where the folder to move the files is
    dir_name : str
            Name of the directory where the files must be moved
    list_of_files : list of dimension n with arrays of dimension [0, 2]
            List of the files that must be moved. The first position is the name of the file and the second defines if
            the file must be copied or cut

    Kwargs
    -----
        none

    Return
    --------
        none

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
        Abaqus_generator_main.py
        POST_abaqus_script.py
        POST_python_script.py

    Program calls
    -----
        none
    '''

    #
    #Check if the directory exists and, otherwise, creates it:
    os.chdir(path_destination)
    create_directory(path_destination, dir_name)
    #Path to move the files
    path = path_destination + '/' + str(dir_name)
    #
    #Move to the origin directory
    os.chdir(path_origin)
    #
    #Move the files
    for file in list_of_files:
        if file[0][0] == '*':
            for file_with_extension in glob.glob(file[0]):
                if file[1] == 'copy':
                    shutil.copy(file_with_extension, path)
                if file[1] == 'cut':
                    shutil.move(file_with_extension, path)
        else:
            #if the file needs to be copied
            if file[1] == 'copy':
                shutil.copy(file[0], path)
            #if the files needs to be cut
            if file[1] == 'cut':
                shutil.move(file[0], path+'/'+file[0])
    #


def create_directory(dir_path, directory):
    '''
    The Python function check if the directory already exists and if not, it creates a new folder in the corresponding path
    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia
    Args
    -----
    dir_path : str
            Path of the directory where the new folder must be created
    directory : str
            Name of the new folder
    Kwargs
    -----
        none
    Return
    --------
        none
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
        none
    Program calls
    -----
        none
    '''

    #Move to the corresponding directory
    os.chdir(dir_path)
    #If there is more than one directory
    directory.split('/')
    for i in directory.split('/'):
        #Create the directory if it not exists
        if os.path.isdir('./'+str(i)) is False:
            os.mkdir(i)
        dir_path = dir_path + '/' + i
        os.chdir(dir_path)



def remove_files(dir_path, list_of_files=None, list_of_extensions=None, list_of_folders=None):
    '''
    The Python function try to remove all the files, extensions and folders specified by the user

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    dir_path : str
            Path of the directory where to remove files

    Kwargs
    -----
    list_of_files : list of dimension n with str
            List of the files that must be removed
    list_of_extensions : list of dimension n with str
            List of the files with a specific extension that must be removed
    list_of_folders : list of dimension n with str
            List of the folders that must be removed

    Return
    --------
        none

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
        Abaqus_generator_main.py
        POST_abaqus_script.py
        POST_python_script.py

    Program calls
    -----
        none
    '''

    os.chdir(dir_path)
    #
    #Remove the files
    if list_of_files is not None:
        for file in list_of_files:
            try: os.remove(file)
            except: pass
    #
    #Remove all the files with an extension
    if list_of_extensions is not None:
        for extension in list_of_extensions:
            for file in glob.glob(extension):
                try: os.remove(file)
                except: pass
    #
    #Remove all the folders
    if list_of_folders is not None:
        for folder in list_of_folders:
            try: shutil.rmtree(folder)
            except: pass
    #



def create_inps(ff_strain, dir_path, inp_name):
    '''
    The Python function modifies the input file to create all the necessary ones according to the strains to analyse

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    ff_strain : array of shape (3, 3)
            Far field strain tensor: E11, E12, E13
                                     E21, E22, E23
                                     E31, E32, E33
            Binary {1:apply, 0:not-apply}
    dir_path : str
            Path of the directory where the main input file is
    inp_name : str
            Title of the input file to be modified

    Kwargs
    -----
        none

    Return
    --------
        none

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
        Abaqus_generator_main.py

    Program calls
    -----
        none
    '''

    #Move to the path with the input file
    path = os.path.join(dir_path, inp_name + '.inp')
    #
    #Read the strains that should be analyzed
    ff_strain_flat = [item for sublist in ff_strain for item in sublist]
    strains_list = ['e11', 'e12', 'e13', 'e21', 'e22', 'e23', 'e31', 'e32', 'e33']
    for i in range(len(ff_strain_flat)):
        if ff_strain_flat[i] ==  0.:
            strains_list[i] = None
        else:
            pass
    #Dictionary with the line to be modified for each strain
    corresponding_line = {
        'e11' : 'RF_EX1, 1, 1',
        'e12' : 'RF_EX2, 1, 1',
        'e13' : 'RF_EX3, 1, 1',
        'e21' : 'RF_EX1, 2, 2',
        'e22' : 'RF_EX2, 2, 2',
        'e23' : 'RF_EX3, 2, 2',
        'e31' : 'RF_EX1, 3, 3',
        'e32' : 'RF_EX2, 3, 3',
        'e33' : 'RF_EX2, 3, 3',
    }
    #
    #Check the far field strains and modified the input file
    for pos, value in enumerate(strains_list):
        input = open(path)
        data = input.read()
        if value is not None:
            strain_2_apply = ff_strain_flat[pos]
            # if value[1] == value[2]: #if is a normal strain
            #     strain_2_apply = 1.0
            # else: #if is a shear strain
            #     strain_2_apply = 0.5
            #Modify the corresponding line
            new_data = data.replace(corresponding_line[value], (corresponding_line[value] + ', ' + str(strain_2_apply)))
            #Create the new input file
            new_path = os.path.join(dir_path, inp_name + '_' + str(value) + '.inp')
            fileNew = open(new_path, 'w')
            fileNew.writelines(new_data)
            fileNew.close()
        input.close()
    #


def str_is_numeric(s):
    '''
    The Python function check if a string is numeric

    Author
    -----
        L. F. Pereira (lfpereira@fe.up.pt)
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)

    Args
    -----
    s : str
            String to be checked

    Kwargs
    -----
        none

    Return
    --------
    numeric : Boolean
            True if is a float or False if it is not

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
        Read_txt

    Program calls
    -----
        none
    '''

    try:
        float(s)
        numeric = True
    except ValueError:
        numeric = False

    return numeric


def corresponding_STRAIN_STRESS(strain):
    '''
    The Python function gives the corresponding strains, stresses and stiffness tensor for each strain

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    strain : str
            Strain to be checked

    Kwargs
    -----
        none

    Return
    --------
    corresponding_E_S : Dictionary
            Dictionary with the information about the strain and the stresses and stiffness tensor to be checked for each strain

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
        Read_txt

    Program calls
    -----
        none
    '''

    # Dictionary with all the relations between each analysis (each strain)
    corresponding_E_S = {
        'e11': {'strain': 'E11', 'stress': ['S11', 'S22'], 'stiff_tensor': ['C1111', 'C1122']},
        'e12': {'strain': 'E12', 'stress': ['S12'], 'stiff_tensor': ['C4444']},
        'e13': {'strain': 'E13', 'stress': ['S13'], 'stiff_tensor': ['C4444']},
        'e21': {'strain': 'E12', 'stress': ['S12'], 'stiff_tensor': ['C4444']},
        'e22': {'strain': 'E22', 'stress': ['S11', 'S22', 'S33'], 'stiff_tensor': ['C1122', 'C2222', 'C2233']},
        'e23': {'strain': 'E23', 'stress': ['S23'], 'stiff_tensor': ['C2222_C2233']},
        'e31': {'strain': 'E13', 'stress': ['S13'], 'stiff_tensor': ['C4444']},
        'e32': {'strain': 'E23', 'stress': ['S23'], 'stiff_tensor': ['C2222_C2233']},
        'e33': {'strain': 'E33', 'stress': ['S11', 'S22', 'S33'], 'stiff_tensor': ['C1122', 'C2233', 'C2222']}
    }

    return corresponding_E_S[strain]


#Dictionary while creating the comparison graph for the elastic properties
dict_POST_vars = {
    'E11': {'Units': 'MPa', 'Description': "Longitudinal Young's Modulus",
            'Title': 'Distribution of the E11', 'Index' : 0, 'Latex' : '$E_{1}$'},
    'v12': {'Units': '-', 'Description': "Major Poisson's ratio", 'Title': 'Distribution of the v12', 'Index' : 1, 'Latex' : '$\\nu_{12}$'},
    'E22': {'Units': 'MPa', 'Description': "Transversal Young's Modulus", 'Title': 'Distribution of the E22', 'Index' : 2, 'Latex' : '$E_{2}$'},
    'G12': {'Units': 'MPa', 'Description': "In-plane shear Modulus", 'Title': 'Distribution of the G12', 'Index' : 3, 'Latex' : '$G_{12}$'},
    'G23': {'Units': 'MPa', 'Description': "Out-of-plane shear Modulus", 'Title': 'Distribution of the G23', 'Index' : 4, 'Latex' : '$G_{23}$'},
    'v23': {'Units': '-', 'Description': "Through thickness Poisson's ratio", 'Title': 'Distribution of the v23', 'Index' : 5, 'Latex' : '$\\nu_{23}$'}
}



class Field(object):
    '''
    Class to save a Field composed by a value and its units

    Author
    -----
        L. F. Pereira (lfpereira@fe.up.pt)
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)
    '''

    def __init__(self, value, unit=None):
        '''
        Initialization of the class Field
        Author
        -----
            L. F. Pereira (lfpereira@fe.up.pt)
            Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)
        Args
        -----
        value : int, float, boolean, None, str
                Value of the Field
        Kwargs
        -----
        unit : str
                String with the units
        Return
        --------
        self : attributes
                All the necessary attributes of the class Field
        '''
        self.value = value
        self.unit = unit


