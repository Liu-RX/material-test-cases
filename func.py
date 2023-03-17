import os
import re

def grep_key_val(fp, skip_=True) -> dict:
    """
    Convert file context such as 
    '
    input_parameters 
    a   1
    b   123
    c   1.23
    '
    to dictionary as 
    {'a': '1', 'b': '123', 'c': '1.23'}
    """
    input_dict = {}
    for iline, line in enumerate(fp.readlines()):
        line_str = line.strip()
        line_components = re.split("\s+", line_str)
        if len(line_components) >= 2:
            if skip_:
                if line_components[0][0] == "#":
                    # # in INPUT means comment
                    continue
            if line_components[0].lower() == "input_parameters":
                continue
            input_dict[line_components[0]] = line_components[1]
    return input_dict

def make_key_val_str(input_dict: dict) -> str:
    """
    Convert dictionary such as {'a': '1', 'b': '123', 'c': '1.23'}
    
    to string as 
    ' 
    a   1
    b   123
    c   1.23
    '
    """
    out = ""
    for k in input_dict.keys():
        out += "%s    %s\n"%(k, input_dict[k])
    return out

def make_kpt_str(kpt_dict: dict) -> str:
    """
    Convert kpt_dict such as {
    "nx": "2",
    "ny": "2",
    "nz": "2",
    "sx": "0",
    "sy": "0",
    "sz": "0"
    }
    to
    K_POINTS
    0
    Gamma
    2 2 2 0 0 0 
    """
    assert("nx" in kpt_dict)

    out = """
    K_POINTS
0
Gamma
%s %s %s %s %s %s
    """
    return out %(kpt_dict["nx"], kpt_dict["ny"], kpt_dict["nz"], kpt_dict["sx"], kpt_dict["sy"], kpt_dict["sz"])
