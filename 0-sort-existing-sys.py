import dpdata

file_dir = "/home/saber/work/03b01_peng_abacustest/liuyu_examples/2020_BeO/Be-BeO/2/Be_BeO/STRU"

dat = dpdata.System(file_dir, fmt="stru")
print(dat.data)