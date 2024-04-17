#Import libraries
from collections import OrderedDict
#Import local libraries
from Scripts.Misc import str_is_numeric
from Scripts.Misc import Field
from MaterialDataBase.Material_data_base import Material


def read_nested_list_from_str(ls):
    '''
    The Python function reads a list/list of list inside (nested) a string and converts it to the corresponding array

    Author
    -----
        L. F. Pereira (lfpereira@fe.up.pt)
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)

    Args
    -----
    ls : str
            String with a list or list of list (one-nested level)

    Kwargs
    -----
        none

    Return
    --------
    new_ls : list
            List from the string with one or two levels (one-nested level)

    Examples
    -----
        none

    Raises
    -----
        none

    Note
    -----
        - Works fine until one-nested level.
        # TODO: verify veracity
        - Interesting function which it calls ownself

    Program called by
    -----
        POST_abaqus_script
        Post_python_script
        Abaqus_generator_main

    Program calls
    -----
        read_list_from_str (Read_txt)
    '''

    #Check how many lists are inside
    if ls.count('[') == 1:              #if is a unique list
        return read_list_from_str(ls)
    else:                               #if is one-nested level
        index_1 = ls.index('[') + 1
        index_2 = len(ls) - 1 - ls[::-1].index(']')
        new_lists = ls[index_1:index_2].split('],')
        new_lists = [ls + ']' for ls in new_lists]
        new_ls = []
        for new_list in new_lists:
            new_ls.append(read_nested_list_from_str(new_list))
        return new_ls


def read_list_from_str(ls):
    '''
    The Python function converts a list in a string to a list of items in the corresponding type (int, float, boolean, str)

    Author
    -----
        L. F. Pereira (lfpereira@fe.up.pt)
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)

    Args
    -----
    ls : str
            String with a single list

    Kwargs
    -----
        none

    Return
    --------
    new_ls : list
            List from the string with each item in the corresponding type (int, float, boolean, str)

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
        read_nested_list_from_str (Read_txt)

    Program calls
    -----
        change_str_type (Read_txt)
    '''

    #Remove brackets
    if '[' in ls and ']' in ls:
        index_1 = ls.index('[') + 1
        index_2 = ls.index(']')
        ls = ls[index_1:index_2]
    #
    #Remote spaces between values and split members
    members = ls.split(',')
    #
    #Get new list
    new_ls = [change_str_type(member) for member in members]

    return new_ls


def change_str_type(value):
    '''
    The Python function converts a string to the corresponding type (int, float, boolean, str)

    Author
    -----
        L. F. Pereira (lfpereira@fe.up.pt)
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)

    Args
    -----
    value : str
            String with a value

    Kwargs
    -----
        none

    Return
    --------
    new_value : int, float, boolean, None, str
            Value in its corresponding type

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
        read_list_from_str (Read_txt)
        read_inputs_from_txt (Read_txt)

    Program calls
    -----
        str_is_numeric (Misc)
    '''

    #Check the type of the string
    if value.lstrip('-+').isdigit(): #strip the left side, remove '+' or '-' symbols and check if is a number
        new_value = int(value)
    elif str_is_numeric(value):      #try to convert it to a float to check if is a real number
        new_value = float(value)
    else:
        if value.lower() == 'true':
            new_value = True
        elif value.lower() == 'false':
            new_value = False
        elif value.lower() == 'none':
            new_value = None
        else:
            new_value = str(value)

    return new_value


def read_inputs_from_txt(filename, separator = ':', ignore_units=False, lower_case=True, ignore_material=True):
    '''
    The Python function read the inputs from a txt file and creates a dictionary with all the values

    Author
    -----
        L. F. Pereira (lfpereira@fe.up.pt)
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)

    Args
    -----
    filename : str
            String with the filename to be read

    Kwargs
    -----
    separator : str
            String with the symbol used to separate the name from the value
    ignore_units : boolean
            Boolean to definie if the units must be saved (False) or can be ignored (True)
    lower_case : boolean
            Boolean to define if all the names must be saved in lower case (True) or as they are (False)
    ignore_material : boolean
            Boolean to define if the material is saved as a class with all the properties (True) or only the name (True)

    Return
    --------
    inputs : OrderedDict
            Dictionary with all the inputs read in the same order as they were read

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
        POST_abaqus_script
        POST_python_script

    Program calls
    -----
        read_nested_list_from_str (Read_txt)
        change_str_type (Read_txt)
        read_material (Read_txt)
        Field (Misc)
    '''

    #Initialization of the dictionary
    inputs = OrderedDict()
    #
    #Read the file with the inputs
    with open(filename, 'r') as f:
        data = f.readlines()
    #
    #Manipulate the variables
    for line in data:
        try:
            name, value = line.split(separator, 2) #split according to the separator and maximum 2 plits
            value = value.strip()
            splitted_name = name.split('[')  #to get units
            description = splitted_name[0].strip()
            if len(splitted_name) == 1:
                unit = None
            else:
                unit = splitted_name[1].replace(']', '').strip()
        except ValueError: #if it is not: 'name [unit] = value', pass
            continue
        #
        if '[' in value and ']' in value:               #if it is a list / list of list
            new_value = read_nested_list_from_str(value)
        else:
            new_value = change_str_type(value)          #if it is a unique value
        #
        name_ = description.lower() if lower_case else description    #save the name according to lower case or not
        if ignore_material or 'material' not in description.lower():  #if we only want to save the material name
            field = new_value if ignore_units else Field(new_value, unit) #save the value according to save the units or not
        else: #if we want to save the material as a class
            field = read_material(new_value) if ignore_units else Field(read_material(new_value), unit)
        inputs[name_] = field

    return inputs


def read_material(material):
    '''
    The Python function read a material from a txt file

    Author
    -----
        Oriol Vallmajo Martin (oriol.vallmajo@udg.edu)

    Args
    -----
    material : str
            String with the name of the material
            This name must be the same as the tzt file

    Kwargs
    -----
    none

    Return
    --------
    mat : class
            Material read

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
        read_inputs_from_txt (Read_txt)

    Program calls
    -----
        MaterialDataBase.Material_data_base
    '''

    #Create the class material
    mat = Material(material)
    #Read the material to have all the values
    mat.read_material()

    return mat