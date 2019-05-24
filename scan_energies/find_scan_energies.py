#!/mnt/storage/home/mw12315/.local/bin/python3
from sys import argv

if len(argv) == 1:
    fileIn = "OUTPUT"
else:
    fileIn = argv[1]


print("Scan Energies for {}".format(fileIn))
print("{:5s}\t{:19s}\t{:6}\t{:10}\t{:10}".format("SCAN","Energy / AU","Points","Time / min", "min/scan"))

last_time = 0
with open(fileIn,'r') as f:
    o = open("{}_Escan.csv".format(fileIn),'w')
    o.write("{:5s},{:19s},{:6}\n".format("SCAN","Energy / AU","Points"))
    nScans = 0
    for line in f:
        if "TELAPSE" in line:
            splitLine = line.strip().split()
            try:
                te_lapse = float(splitLine[3])
            except ValueError:
                print(splitline)

        if "OPT END - CONVERGED" in line:
            nScans += 1
            splitLine = line.strip().split()
            nums = []
            for part in splitLine:
                try:
                    float(part)
                    nums.append(part)
                except ValueError:
                    pass

            print("{:5}\t{:15.10e}\t{:6d}\t{:10.1f}\t{:10.1f}".format(nScans,float(nums[0]),int(nums[1]),round(te_lapse/60,1),round((te_lapse - last_time)/60,1)))
            o.write("{:5},{:15.10e},{:6d}\t{:10.1f}\t{:10.1f}\n".format(nScans,float(nums[0]),int(nums[1]),round(te_lapse/60,1),round((te_lapse - last_time)/60,1)))
            last_time = te_lapse

print("Output to: {}".format(o.name))
o.close()
