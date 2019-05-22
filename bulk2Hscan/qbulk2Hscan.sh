#!/bin/bash

#SBATCH --job-name=6311G**
#SBATCH -p cpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=28
#SBATCH --mem-per-cpu=4G
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00

#SBATCH --mail-type=ALL
#SBATCH --mail-user=mw12315@bristol.ac.uk

WORKDIR="$SLURM_SUBMIT_DIR"
BULKDIR="$WORKDIR/${1}"
GEOMDIR="$WORKDIR/${2}"
LAYERSDIR="$WORKDIR/${3}"
CRADICALDIR="$WORKDIR/${4}"
CRADICAL2DIR="$WORKDIR/${5}"
HSCANDIR="$WORKDIR/${6}"

echo $WORKDIR
echo $BULKDIR
echo $GEOMDIR
echo $LAYERSDIR
echo $CRADICALDIR
echo $CRADICAL2DIR
echo $HSCANDIR

cd "${WORKDIR}"

module add OpenMPI/3.0.0-GCC-7.2.0-2.29
module load ifort/2017.1.132-GCC-5.4.0-2.26 
export OMPI_FC=ifort
CRYSTAL="mpirun -np 112 /mnt/storage/home/mw12315/CRYSTAL17/bin/Linux-ifort17_XE_emt64/v1.0.2/Pcrystal"

eval "touch ${WORKDIR}/OUTPUT_ALL"
###################
# BULK OPTIMISATION
###################
echo "BULK FULLOPTGEOM START"
cd "${BULKDIR}"
eval "${CRYSTAL}"
eval "cp ${WORKDIR}/slurm* ${BULKDIR}/OUTPUT "
# Reset main output file
eval "cat ${WORKDIR}/slurm* >> ${WORKDIR}/OUTPUT_ALL"
eval "cp /dev/null ${WORKDIR}/slurm*"
# Remove pe files etc
eval "rm -f *pe*"

# Update Lattice Parameter in GEOM INPUT FILE (and hydrogen insertion position
eval "python3 $HOME/scripts/bulk2geomlayers.py ${BULKDIR} ${GEOMDIR}"

#############################
# CHEAP GEOMETRY OPTIMISATION
#############################
echo "CHEAP GEOM OPT LAYERS START"
cd "${GEOMDIR}"
eval "${CRYSTAL}"
eval "cp ${WORKDIR}/slurm* ${GEOMDIR}/OUTPUT "
# Copy optimised structure to 7_LAYERS DIR
eval "cp ${GEOMDIR}/fort.34 ${LAYERSDIR}"
# Remove pe files etc
eval "rm -f *pe*"
eval "cat ${WORKDIR}/slurm* >> ${WORKDIR}/OUTPUT_ALL"
# Reset main output file
eval "cp /dev/null ${WORKDIR}/slurm*"

###################
# 7 LAYERS GEOM OPT
###################
echo "7 LAYERS OPT START"
cd "${LAYERSDIR}"
eval "${CRYSTAL}"
eval "cp ${WORKDIR}/slurm* ${LAYERSDIR}/OUTPUT "
# Remove pe files etc
eval "rm -f *pe*"
# Reset main output file
eval "cat ${WORKDIR}/slurm* >> ${WORKDIR}/OUTPUT_ALL"
eval "cp /dev/null ${WORKDIR}/slurm*"

###########
# C_RADICAL
###########
echo "C RADICAL OPT START"
cd "${CRADICALDIR}"
eval "cp ${LAYERSDIR}/fort.34 ${CRADICALDIR}"

eval "${CRYSTAL}"

eval "cat ${WORKDIR}/slurm* >> ${WORKDIR}/OUTPUT_ALL"
eval "cp ${WORKDIR}/slurm* ${CRADICALDIR}/OUTPUT"
eval "rm -f ${WORKDIR}/*pe*"
eval "cp /dev/null ${WORKDIR}/slurm*"
############
# C_RADICAL2
############
echo "C RADICAL2 OPT START"
cd "${CRADICAL2DIR}"
eval "cp ${CRADICALDIR}/fort.34 ${CRADICAL2DIR}"

eval "${CRYSTAL}"
eval "cat ${WORKDIR}/slurm* >> ${WORKDIR}/OUTPUT_ALL"
eval "cp ${WORKDIR}/slurm* ${CRADICAL2DIR}/OUTPUT"
eval "rm -f ${CRADICAL2DIR}/*pe*"

########
# H_SCAN
########
eval "cp /dev/null ${WORKDIR}/slurm*"
echo "H SCAN START"
cd "${HSCANDIR}"
eval "python3 /mnt/storage/home/mw12315/scripts/layers-rad2HScan.py ${LAYERSDIR} ${CRADICAL2DIR} ${HSCANDIR}"
eval "mv ${WORKDIR}/slurm* OUTPUT"
eval "rm -f ${HSCANDIR}/*pe*"

echo "FINISHED"
