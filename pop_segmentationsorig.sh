#!/bin/bash

#####
# Resample the segmentations into original space
#####

## Changelog
# 2014-08-08 created

# include shared information
source $(dirname $0)/include.sh

# functions
###
# Execture registration
###
function resample ()
{
	# grab parameters
	i=$1

	# continue if target file already exists
	if [ -f "${segmentationsorig}/${i}.${imgfiletype}" ]; then
		return
	fi

	log 1 "Resampling ${segmentationsorig}/${i}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	# get target voxel spacing
	vs=( $(voxelspacing "${origspacereferences}/${i}/${basesequence}.${imgfiletype}") )
	
	# resample
	runcond "medpy_resample.py -o1 ${segmentationssub}/${i}/segmentation_post.${imgfiletype} ${segmentationsorig}/${i}.${imgfiletype} $(joinarr "," ${vs[@]})"
	
	# correct image size
	runcond "${scripts}/fitin.py ${segmentationsorig}/${i}.${imgfiletype} ${origspacereferences}/${i}/${basesequence}.${imgfiletype}"
}

# main code
log 2 "Resampling all segmentation to original space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize resample ${threadcount} images[@]

