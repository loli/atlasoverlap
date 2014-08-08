#!/bin/bash

#####
# Uses elastic to register images to a template.
#####

## Changelog
# 2014-08-08 created

# include shared information
source $(dirname $0)/include.sh

# functions
###
# Execture registration
###
function register ()
{
	# grab parameters
	i=$1

	# continue if target file already exists
	if [ -f "${mnispace}/${i}.${imgfiletype}" ]; then
		return
	fi
	# register
	log 1 "Registering ${originals}/${i}/${basesequence}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/orig2mni.sh ${originals}/${i}/${basesequence}.${imgfiletype} ${mnispace}/${i}_rigid.${imgfiletype} ${mnispace}/${i}.${imgfiletype} ${mnispace}/${i}_rigid.txt ${mnispace}/${i}_moving.txt ${brainmasks}/${i}.nii.gz" "logs/register${i}.log"
}

# main code
log 2 "Registering all sequences ${basesequence} to template" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize register ${threadcount} images[@]

