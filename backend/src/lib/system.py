#!/opt/homebrew/bin/python3.9
# coding=utf-8

import yaml, sys


class style:
    RED = '\33[31m'
    ORANGE = '\33[33m'
    GREEN = '\33[32m'
    NORMAL = '\033[0m'


def Read_Yaml(file):
    """
    ReadYAMLCfgFile(YAML_CFG_FILE)
    Read a YAML File and return Dictionnary
    Returns
    ----------
    Dictionnary of Yaml information
    Parameters
    ----------
    YAML_CFG_FILE : Str
        Name of YAML file
    args : list of args
    """
    # Open and treatment of a YAML config file
    try:
        with open(file, 'r') as ymlfile:
            global YAML_DICT_LOADED
            YAML_DICT_LOADED = yaml.load(ymlfile, Loader=yaml.FullLoader)
            if 'OUTPUT_FORMAT' not in YAML_DICT_LOADED:
                YAML_DICT_LOADED['OUTPUT_FORMAT'] = 'XLSX'
            return YAML_DICT_LOADED
    except Exception as e:
        print(style.RED + file + " not found in directory" + style.NORMAL)
        print(style.ORANGE + e + style.NORMAL)
        sys.exit(1)

def search_obj_in_list(list, key, name):
    for item in list:
        if getattr(item, key) == name:
            return item
        