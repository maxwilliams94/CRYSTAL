#!/mnt/storage/home/mw12315/.local/bin/python3
"""
copy fort.34 file into 7_LAYERS FOLDER
move some carbons and hydrogen to correct atom values
"""
from shutil import copyfile
import sys
from sys import argv
from os import path, remove

class Atom:
    def __init__(self, iatom, anum, x, y, z):
        self.index = iatom + 1 # Allow for fact that python counts for 0 but crystal counts from 1
        self.atomic_number = int(anum)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

        self.carbon_surface = list(range(1,9))
        self.carbon_subsurface = list(range(9,25))
        self.carbon_bulk = list(range(25,57))
        self.hydrogen_surface = [57,58,61,62,65,66,69,70]
        self.hydrogen_bulk = [59,60,63,64,67,68,71,72]

        if self.atomic_number == 1:
            if self.index in self.hydrogen_bulk:
                self.atomic_number += 0
                # 100
        elif self.atomic_number == 6:
            if self.index in self.carbon_surface:
                self.atomic_number += 0
                # 1000
            elif self.index in self.carbon_subsurface:
                self.atomic_number += 0
                # 100

    def __str___(self):
        return "{:5d}\t{:18.12f}\t{:18.12f}\t{:18.12f}\n".format(self.atomic_number, self.x, self.y, self.z)

    def write_atom(self):
        return "{:5d}\t{:18.12f}\t{:18.12f}\t{:18.12f}\n".format(self.atomic_number, self.x, self.y, self.z)

# Inputs
if len(argv) != 3:
    print("Usage: {} GEOM_LAYERS_DIR 7_LAYERS_DIR".format(argv[0]))
    sys.exit()

geom_dir = argv[1]
layers_dir = argv[2]

copyfile(path.join(geom_dir,'fort.34'), path.join(layers_dir,'fort.34'))

# Edit atomic number within new fort.34 file

with open(path.join(layers_dir,'fort.34'),'r') as f:
    with open(path.join(layers_dir,'tmp_fort.34'),'w') as tmp:
        # Get past lattice vectors and symmetries
        other_lines = []
        for n in range(4):
            other_lines.append(f.readline())
        symms = int(f.readline())
        other_lines.append("{}\n".format(symms))
        for n in range(symms * 4):
            other_lines.append(f.readline())
        total_atoms = int(f.readline())
        print("Total atoms",total_atoms)
        # Read Atoms
        atoms = []
        for iatom in range(total_atoms):
            atom_line = f.readline().split()
            atom_line = list(map(str.strip,atom_line))
            atoms.append(Atom(iatom, atom_line[0], atom_line[1], atom_line[2], atom_line[3]))
            
        for line in other_lines:
            tmp.write(line)
        
        # Write atoms
        tmp.write("{}\n".format(total_atoms))
        for atom in atoms:
            tmp.write(atom.write_atom())
        tmp.write("{}\t{}".format(0,0))

# Copy temporary to fort.34

copyfile(path.join(layers_dir,'tmp_fort.34'),path.join(layers_dir,'fort.34'))
remove(path.join(layers_dir,'tmp_fort.34'))

print("Copied {} ({} atoms) to {} with updated atomic numbers".format(path.join(geom_dir,'fort.34'),
                                                                      total_atoms,
                                                                      path.join(layers_dir,'fort.34')))

