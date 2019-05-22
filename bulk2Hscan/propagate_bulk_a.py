#!/mnt/storage/home/mw12315/.local/bin/python3
"""
Find lattice parameter from BULK FULLOPTGEOM OUTPUT file
Find position of top carbon in optimised 8 atom primitive
Replace lattice parameter and hydrogen addition coordinates in GEOM_7LAYERS INPUT FILE
"""
import sys
from sys import argv
from os import path, remove
from collections import namedtuple
from shutil import copyfile

# Inputs
if len(argv) not > 2:
    print("Usage: {} BULK_DIR TARGET_DIRS".format(argv[0]))
    sys.exit()

bulk_dir = argv[1]
target_dirs = argv[2:]


# Get final a value from BULK DIRECTORY OUTPUT FILE
with open(path.join(bulk_dir,'OUTPUT'),'r') as f:
    while True:
        if "FINAL OPTIMIZED GEOMETRY" in f.readline():
            for n in range(5):
                f.readline()
            
            a = round(float(f.readline().strip().split()[0]),4)
            break

for directory in target_dirs:
    with open(path.join(directory,'INPUT'),'r') as f:
        with open(path.join(directory,'temp_INPUT'),'w') as tmp:
            total_lines = len(f.readlines())
            f.seek(0,0)
            for iline in range(total_lines):
                line = f.readline()
                if iline == 4:
                    tmp.write('{}\n'.format(round(a,4)))
                else:
                    tmp.write(line)

    # Delete Old INPUT FILE and Replace with new one
    copyfile(path.join(directory,'temp_INPUT'),path.join(directory,'INPUT'))
    remove(path.join(directory,'temp_INPUT'))
    print("Copied lattice parameter to INPUT files in:")
    print("\n".join(target_dirs))
    

