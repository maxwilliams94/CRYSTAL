import re
from sys import argv, exit

if len(argv) == 1:
    print("Usage: OUTPUT_FILE")
    exit()

class SCF:
    def __init__(self, line):
        
        line = line.split()
        self.cycle = int(line[1])
        self.energy = float(line[3])
        self.dEnergy = float(line[5])


    def get_string(self):
        return "{} {} {}".format(self.cycle,self.energy,self.dEnergy)



with open(argv[1],'r') as f:
    cycles = []
    for line in f:
        if "CYC " in line:
            cycles.append(SCF(line))


with open('SCF_ENERGIES.txt','w') as f:
    print("Output to: {}".format(f.name))
    for cycle in cycles:
        f.write("{}\n".format(cycle.get_string()))

