#!//mnt/storage/home/mw12315/.local/bin/python3
"""
Find hydrogen 69 in fort.34 file inside directory 1
Insert position of hydrogen 69 into INPUT FILE (scan final position) in directory 2
Insert 2 hydrogens 3A above final position in fort.34 inside directory 2
"""

from sys import argv, exit
from os import path,remove
from shutil import copyfile

class LineAtom:
    def __init__(self, line):
        line = line.split()

        self.at_number = int(line[0])
        self.x = float(line[1])
        self.y = float(line[2])
        self.z = float(line[3])

class Atom:
    def __init__(self, anum, x, y, z):
        self.anum = anum
        self.x = x
        self.y = y
        self.z = z


if len(argv) != 4:
    print("Usage: LAYERS_DIR CRADICAL_DIR HSCAN_DIR")
    exit()

LAYERSDIR = argv[1]
CRADDIR = argv[2]
HSCANDIR = argv[3]

# Get position of hydrogen 69 in fort.34

with open(path.join(LAYERSDIR,'fort.34'),'r') as f:
    # Read to start of atom list
    for n in range(4):
        f.readline()
    nsymms = int(f.readline())
    for n in range(nsymms*4):
        f.readline()
    natoms = int(f.readline())
    for n in range(natoms):
        line = f.readline()
        if (n+1) == 69:
            a69 = LineAtom(line)
            print("Found atom {}".format(n+1))

print("{} {} {} {}".format(a69.at_number, a69.x, a69.y, a69.z))

# Insert H position into SCAN_H

with open(path.join(HSCANDIR,'INPUT'),'r') as f:
    with open(path.join(HSCANDIR,'tmp_INPUT'),'w') as tmp:
        while True:
            line = f.readline()
            tmp.write(line)
            if "SCANATOM" in line:
                tmp.write(f.readline())
                tmp.write("{} {} {}\n".format(a69.x, a69.y, a69.z))
                f.readline()
                break

        # Contine writing file to tmp
        while True:
            line = f.readline()
            tmp.write(line)
            if "ENDSCF" in line:
                break

print("Written temporary INPUT file with new HSCAN final position inserted")

copyfile(path.join(HSCANDIR,'tmp_INPUT'),path.join(HSCANDIR,'INPUT'))
remove(path.join(HSCANDIR,'tmp_INPUT'))

print("Copied tmp_INPUT to INPUT and deleted tmp_INPUT")

# Copy CRADICAL fort.34 to HSCANDIR and add 2 atoms at the bottom 3A away from FINAL POSITION

copyfile(path.join(CRADDIR,'fort.34'),path.join(HSCANDIR,'fort.34'))

with open(path.join(HSCANDIR,'fort.34'),'r') as f:
    with open(path.join(HSCANDIR,'tmp_fort.34'),'w') as tmp:
        for n in range(4):
            tmp.write(f.readline())
        symms = int(f.readline())
        tmp.write("{}\n".format(symms))
        for n in range(4*symms):
            tmp.write(f.readline())
        total_atoms = int(f.readline())
        tmp.write("{}\n".format(total_atoms+2))
        for n in range(total_atoms):
            tmp.write(f.readline())

        # Write new atoms to tmp file
        scanned_atom = Atom(1, a69.x, a69.y, a69.z + 3.0)
        top_atom = Atom(1, a69.x, a69.y, a69.z + 3.8)

        tmp.write("{} {} {} {}\n".format(scanned_atom.anum, scanned_atom.x, scanned_atom.y, scanned_atom.z))
        tmp.write("{} {} {} {}\n".format(top_atom.anum, top_atom.x, top_atom.y, top_atom.z))
        tmp.write("{} {}".format(0,0))


print("Coped fort.34 from C_RADICAL to HSCAN and added 2 hydrogens")
copyfile(path.join(HSCANDIR,'tmp_fort.34'),path.join(HSCANDIR,'fort.34'))
remove(path.join(HSCANDIR,'tmp_fort.34'))

print("Coped tmp_fort.34 to fort.34 and remove tmp_fort.34")








            
