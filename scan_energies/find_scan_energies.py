from sys import argv

if len(argv) == 1:
    fileIn = "OUTPUT"
else:
    fileIn = argv[1]


print("Scan Energies for {}".format(fileIn))
print("{:5s}\t{:19s}\t{:6}".format("SCAN","Energy / AU","Points"))

with open(fileIn,'r') as f:
    o = open("{}_Escan.csv".format(fileIn),'w')
    write("{:5s},{:19s},{:6}\n".format("SCAN","Energy / AU","Points"))
    nScans = 0
    for line in f:
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

            print("{:5}\t{:15.10e}\t{:6d}".format(nScans,float(nums[0]),int(nums[1])))
            o.write("{:5},{:15.10e},{:6d}\n".format(nScans,float(nums[0]),int(nums[1])))

