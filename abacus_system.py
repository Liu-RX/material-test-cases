import dpdata
import warnings
from func import *

class AbacusSystem(dpdata.System):
    """
    The class is meant to maintain an instance of input files of abacus
    in dictionary format in abacus,
    in which way conversion and installation of massive ABACUS test cases
    would be easier and more fluent.

    The class inherit from dpdat.System with fmt="stru".

    """
    def __init__(self, 
                 file_name=None, 
                 submit_file_name = None,
                 fmt="stru", 
                 type_map=None, 
                 begin=0, 
                 step=1, 
                 data=None, 
                 input_dict = {},
                 kpt_dict = {},
                 submit_dict = {},
                 convergence_check=True, 
                 **kwargs) -> None:
        super().__init__(file_name, fmt, type_map, begin, step, data, convergence_check, **kwargs)
        # Mainly to read in the STRU file 




        # initialize input_dict, kpt_dict and submit_dict

        self.input_dict = input_dict
        
        self.kpt_dict = kpt_dict
        
        self.submit_dict = submit_dict

        
        if file_name is not None:
            work_dir = os.path.dirname(file_name)   
            input_dir = os.path.join(work_dir, "INPUT")
            kpt_dir = os.path.join(work_dir, "KPT")
            if submit_file_name is not None:
                submit_dir = os.path.join(work_dir, submit_file_name)
            
            orb_pp = self.read_orb_pp(file_name)
            self.data.update(orb_pp)


            if os.path.exists(input_dir):
                if self.input_dict == {}:
                    self.input_dict = self.read_input(input_dir)
                else:
                    print(input_dict)
                    print("Your INPUT parameters are read in from your input_dict, rather than the INPUT file under STRU dir. Please note that.")
            else:
                warnings.warn("File %s does not exists. By default this means no INPUT parameter is read in. Make sure this is what you want.")
            
            if os.path.exists(kpt_dir):
                if self.kpt_dict == {}:
                    self.kpt_dict = self.read_kpt(kpt_dir)
                else:
                    print("Your KPT parameters are read in from your kpt_dict, rather than the KPT file under STRU dir. Please note that.")
            else:
                warnings.warn("File %s does not exists. By default this means no KPT parameter is read in. Make sure this is what you want.")



    def read_input(self, file_name:str, **kwargs) -> dict:
        """
        Read parameters from input file.
        """
        if os.path.exists(file_name):
            with open(file_name) as fp:
                input_dict = grep_key_val(fp, skip_=True)
        else:
            raise ValueError("File %s does not exists. Please check!"%file_name)
        return input_dict

    def read_kpt(self, file_name:str, **kwargs) -> dict:
        """
        Read nkx, nky, nkz, sx, sy, sz
        Note that only auto-generated K-points are readable.
        Manually set K-points are not supported yet!
        """
        kpt_dict = {}
        if os.path.exists(file_name):
            with open(file_name) as fp:
                lines = fp.readlines()
                for iline, line in enumerate(lines):
                    line_components = re.split("\s+", line.strip())
                    #print(line_components)
                    if len(line_components) >= 6 and re.split("\s+", lines[iline-1])[0].lower() == "gamma":
                        kpt_dict = {
                            "nx": line_components[0],
                            "ny": line_components[1],
                            "nz": line_components[2],
                            "sx": line_components[3],
                            "sy": line_components[4],
                            "sz": line_components[5]
                        }
                        break
        else:
            raise ValueError("File %s does not exists. Please check!"%file_name)
        return kpt_dict
    
    def read_orb_pp_descrp(self, file_name:str, **kwargs) -> dict:
        """
        Read in orbital files and pseudopotential files from STRU file.
        """
        keywords_list = [
            "ATOMIC_SPECIES",
            "LATTICE_CONSTANT",
            "LATTICE_VECTORS",
            "NUMERICAL_ORBITAL",
            "ATOMIC_POSITIONS",
            "NUMERICAL_DESCRIPTOR"
        ]
        orb_pp = {
                "orbs": [],
                "pps": [],
                "masses": [],
                "descr": ""
                  }
        with open(file_name) as fp:
            lines = fp.readlines()
            nline = len(lines)
            for iline, line in enumerate(lines):
                line_strip = line.strip()
                if "ATOMIC_SPECIES" == re.split("\s+", line_strip)[0]:
                    for iline2 in range(iline+1, nline):
                        line_strip2 = lines[iline2].strip()
                        if line_strip2 != "" and line_strip2[0] != "#":
                            if re.split("\s+", line_strip2)[0] not in keywords_list:
                                atom_line = re.split("\s+", line_strip2)
                                pp_file = os.path.basename(atom_line[2])
                                orb_pp['pps'].append(pp_file)
                                orb_pp['masses'].append(atom_line[1])
                            elif re.split("\s+", line_strip2)[0] in keywords_list:
                                break
                if "NUMERICAL_ORBITAL" == re.split("\s+", line_strip)[0]:
                    for iline2 in range(iline+1, nline):
                        line_strip2 = lines[iline2].strip()
                        if line_strip2 != "" and line_strip2[0] != "#":
                            if re.split("\s+", line_strip2)[0] not in keywords_list:
                                orb_file = os.path.basename(re.split("\s+", line_strip2)[0])
                                orb_pp['orbs'].append(orb_file)
                            elif re.split("\s+", line_strip2)[0] in keywords_list:
                                break
                if "NUMERICAL_DESCRIPTOR" == re.split("\s+", line_strip)[0]:
                    orb_pp['descr'] = re.split("\s+", lines[iline+1].strip())[0]
        return orb_pp
    
    def as_dict(self, fmt: str, **kwargs) -> dict:
        """
        fmt: "json/abacus"
        The function returns dict containing the system info.
        """
        if fmt == "json":
            d = self.__dict__
            return d
        elif fmt == "abacus":
            d = {}
            d["input"] = "INPUT_PARAMETERS/n"+make_key_val_str(self.input_dict)
            d["kpt"] = make_kpt_str(self.kpt_dict)
            d["stru"] = 

    def dump(self, fmt: str, **kwargs):
        return

if __name__ == "__main__":
    system = AbacusSystem(file_name="tests/STRU")
    #orb_pp = system.read_orb_pp(file_name="tests/STRU")
    #print(orb_pp)
    # print(system.data)
    # print(system.input_dict)
    # print(system.kpt_dict)
    print(system.__dict__)



