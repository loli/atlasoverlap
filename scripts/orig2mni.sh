#!/bin/bash

# arg1: the image to register
# arg2: where to save the resulting rigidly registered image
# arg3: where to save the resulting non-rigidly registered image
# arg4: where to save the resulting rigid transformation file
# arg5: where to save the resulting non-rigid transformation file
# arg6: head (not brain!) mask for moving image

TEMPLATE="/share/data_humbug1/maier/Temp_Pipeline/AtlasOverlap/templates/flair.nii.gz"
CNF_FILE_RIG="/share/data_humbug1/maier/Temp_Pipeline/AtlasOverlap/configs/orig2mni_rig.txt"
CNF_FILE_MOV="/share/data_humbug1/maier/Temp_Pipeline/AtlasOverlap/configs/orig2mni_mov.txt"

echo "ELASTIX:MOVING Registration"

echo "Preparing to register ${1} to ${TEMPLATE}..."
tmpdir=`mktemp -d`
echo "Temporary directory ${tmpdir} created..."

echo "Registering rigidly..."
elastix -f ${TEMPLATE} -m ${1} -p ${CNF_FILE_RIG} -out ${tmpdir} >> logs/elastix.rigid.log
if [ -f "${tmpdir}/result.0.nii" ]; then
    echo "Registration successfull, copying..."
else
    echo "Registration failed, see elastixlog in ${tmpdir} for details."
    echo "Breaking."
    exit
fi
medpy_convert.py -f ${tmpdir}/result.0.nii ${2}
cp ${tmpdir}/TransformParameters.0.txt ${4}

echo "Registering non-rigidly..."
elastix -f ${TEMPLATE} -m ${1} -mMask ${6} -p ${CNF_FILE_MOV} -out ${tmpdir} -t0 ${4} >> logs/elastix.moving.log
if [ -f "${tmpdir}/result.0.nii" ]; then
    echo "Registration successfull, copying..."
else
    echo "Registration failed, see elastixlog in ${tmpdir} for details."
    echo "Breaking."
    exit
fi
medpy_convert.py -f ${tmpdir}/result.0.nii ${3}
cp ${tmpdir}/TransformParameters.0.txt ${5}

echo "Cleaning up..."
if [ -d ${tmpdir} ]; then
    rm ${tmpdir}/*
    rmdir ${tmpdir}
else
    echo "Cleaning temporary directory ${tmpdir} failed. Please check manually."
fi

echo "Done."



