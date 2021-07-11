"""                               _    _ _   _ _                                     """
"""                              | |  | | | (_) |                                    """
"""                              | |  | | |_ _| |___                                 """
"""                              | |  | | __| | / __|                                """
"""                              | |__| | |_| | \__ \                                """
"""                               \____/ \__|_|_|___/                                """
"""                                                                                  """
"""                                                                                  """
""" Module Name: utils.py                                                            """
""" Author: Luo Zhong-qi                                                             """
""" Last modified: 2021-06-04                                                        """
"""                                                                                  """
""" Description: Just some utilities.                                                """
"""                                                                                  """
""" Importing: from utils import *                                                   """
"""                                                                                  """
""" Exported methods:                                                                """
"""     search_dict_by_value(dict, val)                                              """

def search_dict_by_value(dict, val):
    return [key for key, value in dict.items() if value == val]

def constrain(val, thrL, thrH):
    if(val < thrL):
        return thrL
    elif(val > thrH):
        return thrH
    else:
        return val

def constrain_by_cycle(val, pha, cyc):
    if(pha <= val <= (pha + cyc)):
        return val
    else:
        return (val % cyc - pha % cyc) + pha