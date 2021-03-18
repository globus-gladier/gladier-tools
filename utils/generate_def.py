from os.path import dirname, basename, isfile, join
from inspect import getmembers, isfunction
import importlib
import glob



##get gladier_tools folders

##get every python file on each folder

##get every function without _ in each file

##Create GladierBaseTool for each function

##How to find payload / container? 
##How to write on the __init__.py of each folder? 

fpath = dirname(__file__)
fname = basename(fpath)
pfiles = glob.glob(join(fpath,'[!_]*.py'))

funcs = []

for p in pfiles:
    mod_name = basename(p)
    mod_name = fname+'.'+mod_name.replace('.py','')
    mod = importlib.import_module(mod_name)
    mod_functions = getmembers(mod, isfunction)
    for f in mod_functions:
        funcs.append(mod_name+'.'+f[0])

print(funcs)

for f in funcs:
    print (f)
    globals()[f] = '32'


print(globals())