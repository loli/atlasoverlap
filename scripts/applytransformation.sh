#!/bin/bash

# arg1: the image to transfrom
# arg2: the transformed target image
# arg3: FinalBSplineInterpolationOrder (1 for bin, 3 otherwise)
# arg4+: the transformations to apply in order (composition type will always be Compose; inherent predecessors will be overwritten)

# FUNCTIONS
# strips an elastix parameter file from all information about previous parameter files
function strip_initial_transform () {
    parfile=$1
    sed -i '/InitialTransformParametersFileName/d' ${parfile}
    sed -i '/HowToCombineTransforms/d' ${parfile}
}
# removes all information about the creation of the final image format
function strip_file_creation () {
    parfile=$1
    sed -i '/ResampleInterpolator/d' ${parfile}
    sed -i '/FinalBSplineInterpolationOrder/d' ${parfile}
    sed -i '/ResultImageFormat/d' ${parfile}
}
# appends information about an initial transformation file to an elastix transformation file
function add_initial_transform () {
    parfile=$1
    transfile=$2
    echo "(InitialTransformParametersFileName \"${transfile}\")" >> ${parfile}
    echo "(HowToCombineTransforms \"Compose\")" >> ${parfile}
}
# appends information about the final file creation, format and interpolation order to an elastix transformation file
function add_file_creation () {
    parfile=$1
    order=$2
    echo "(ResampleInterpolator \"FinalBSplineInterpolator\")" >> ${parfile}
    echo "(FinalBSplineInterpolationOrder ${order})" >> ${parfile}
    echo "(ResultImageFormat \"nii.gz\")" >> ${parfile}
}

# MAIN
echo "TRANSFORMIX:APPLICATION"

tfid=1
END="$#"
typeset -i i tfid END # mark variables as integers

echo "Got $(($END-3)) transformation files."

echo "Preparing to transform ${1} and save it to ${2}..."
tmpdir=`mktemp -d`
echo "Temporary directory ${tmpdir} created..."

echo "Copying and chaining transformation files..."
# first one is simply copied and stripped
cp ${4} "${tmpdir}/${tfid}.txt"
strip_initial_transform "${tmpdir}/${tfid}.txt"
# iterate over remaining one
for ((i=5;i<=END;++i)); do
    # increase trans file identifier
    tfid=$((tfid+1))
    # copy and strip
    cp ${!i} "${tmpdir}/${tfid}.txt"
    strip_initial_transform "${tmpdir}/${tfid}.txt"
    # chain
    add_initial_transform "${tmpdir}/${tfid}.txt" "${tmpdir}/$((tfid-1)).txt"
done
# prepare last transformation file for file/image creations
strip_file_creation "${tmpdir}/${tfid}.txt"
add_file_creation "${tmpdir}/${tfid}.txt" ${3}

echo "Transforming..."
transformix -in ${1} -tp ${tmpdir}/${tfid}.txt -out ${tmpdir} >> logs/transformix.log
if [ -f "${tmpdir}/result.nii.gz" ]; then
    echo "Transformation successfull, copying..."
else
    echo "Registration failed, see transformix in ${tmpdir} for details."
    echo "Breaking."
    exit
fi
cp ${tmpdir}/result.nii.gz ${2}

echo "Cleaning up..."
if [ -d ${tmpdir} ]; then
    rm ${tmpdir}/*
    rmdir ${tmpdir}
else
    echo "Cleaning temporary directory ${tmpdir} failed. Please check manually."
fi

echo "Done."



