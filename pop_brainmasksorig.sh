#!/bin/bash

#####
# Resample the brainmasks into original space
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
	if [ -f "${brainmasksorig}/${i}.${imgfiletype}" ]; then
		return
	fi

	log 1 "Resampling ${brainmasksorig}/${i}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	# get target voxel spacing
	vs=( $(voxelspacing "${origspacereferences}/${i}/${basesequence}.${imgfiletype}") )
	
	# resample
	runcond "medpy_resample.py -o1 ${brainmaskssub}/${i}.${imgfiletype} ${brainmasksorig}/${i}.${imgfiletype} $(joinarr "," ${vs[@]})"
	
	# correct image size
	runcond "${scripts}/fitin.py ${brainmasksorig}/${i}.${imgfiletype} ${origspacereferences}/${i}/${basesequence}.${imgfiletype}"
}

# main code
log 2 "Resampling all brainmasks to original space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize resample ${threadcount} images[@]

