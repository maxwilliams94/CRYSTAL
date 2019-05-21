"""
Read in tolerances and other global setting from-json style file
"""
from os import path

# TASK FULLOPTG, OPTGEOM
# GEOM_TOLDEE
# BASIS
# CHUNKS
# GRID XXLGRID, XLGRID, LGRID
# FUNCTIONAL
# SHRINK
# FMIXING
# TOLINTEG
# SCF_TOLDEE
# BIPOLAR
# MAXCYCLE
# NOLOWMEM
# SYMADAPT
# BIOPSIZE

# GENERAL STRUCTURE
# -----------------
# COMMENT
# GEOMETRY (MANUAL OR EXTERNAL)
# GEOMETRY MODIFICATIONS
# JOB TYPE
# JOB TOLERANCES
# BASIS
# DFT SETTINGS
# SCF TOLERANCES

class Crystal:
    def __init__(self):
        self.locations = {'BULK' : None,
                          'LAYERS' : None,
                          'CRADICAL' : None,
                          'CRADICAL2' : None,
                          'HSCAN' : None}
        self.files = {'BULK' : None,
                      'LAYERS' : None,
                      'CRADICAL' : None,
                      'CRADICAL2' : None,
                      'HSCAN' : None}
        self.comment = None

        self.geometryBlock = {'SOURCE' : 'EXTERNAL',
                              'TASK'   : 'OPTGEOM',
                              'TOLDEE' :  6}


        self.basisBlock = {'BASIS'  : '6-31G',
                           'SPECIES': ['C','H']}


        self.scfBlock = {'DFT' : {'SPIN' : 'FALSE',
                                  'GRID' : 'XLGRID',
                                  'FUNCTIONAL' : 'PBEXC'},
                         'ATOMSPIN' : None,
                         'SHRINK' : [2, 2],
                         'TOLINTEG' : [7, 7, 7, 7, 14],
                         'BIPOLAR' : [25, 20],
                         'TOLDEE' : 8,
                         'MAXCYCLE' : 50,
                         'BIPOSIZE' : 10000000}

    def readGeometry(self):
        pass


    def readBasis(self):
        pass

    def readSCF(self):
        pass

    def openFiles(self):
        for key,value in self.locations.items():
            if value:
                self.files[key] = open(path.join('.',value),'w')

    def writeGeometryBlock(self):
        if not self.comment:
            self.comment = "CRYSGEN"

        # WRITE COMMENT TO FILE:
        for f in self.files.values():
            f.write('{}\n'.format(self.comment))



