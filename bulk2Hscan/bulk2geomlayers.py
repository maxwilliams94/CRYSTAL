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
if len(argv) != 3:
    print("Usage: {} BULK_DIR LAYER_GEOM_DIR ".format(argv[0]))
    sys.exit()

bulk_dir = argv[1]
geom_dir = argv[2]


# Get final a value from BULK DIRECTORY OUTPUT FILE
with open(path.join(bulk_dir,'OUTPUT'),'r') as f:
    while True:
        if "FINAL OPTIMIZED GEOMETRY" in f.readline():
            for n in range(5):
                f.readline()
            
            a = round(float(f.readline().strip().split()[0]),4)
            break

Atom = namedtuple('Atom',['x', 'y', 'z'])
hydrogen = Atom(2*a/8,6*a/8,3.5)

# Insert a and H_position into INPUT within GEOM DIRECTORY
with open(path.join(geom_dir,'INPUT'),'r') as f:
    with open(path.join(geom_dir,'temp_INPUT'),'w') as tmp:
        total_lines = len(f.readlines())
        f.seek(0,0)
        for iline in range(total_lines):
            line = f.readline()
            if iline == 0:
                tmp.write('GEOM_LAYERS\n')
            elif iline == 4:
                tmp.write('{}\n'.format(round(a,4)))
            elif "ATOMINSE" in line:
                tmp.write(line)
                f.readline()
                tmp.write("1\n")
                f.readline()
                tmp.write("1 {:7.5f} {:7.5f} {:7.5f}\n".format(*hydrogen))
            else:
                tmp.write(line)

# Delete Old INPUT FILE and Replace with new one
copyfile(path.join(geom_dir,'temp_INPUT'),path.join(geom_dir,'INPUT'))
remove(path.join(geom_dir,'temp_INPUT'))

