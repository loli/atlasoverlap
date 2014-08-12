#!/bin/bash

#####
# Uses transformix and the transformation files from the image2mni registration to transform the ground truth.
#####

## Changelog
# 2014-08-11 created

# include shared information
source $(dirname $0)/include.sh

# functions
###
# Execute transfromation
###
function transform ()
{
	# grab parameters
	i=$1

	# continue if target file already exists
	if [ -f "${groundtruthmni}/${i}.${imgfiletype}" ]; then
		return
	fi
	# register
	log 1 "Transforming ${groundtruthorig}/${i}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/applytransformation.sh  ${groundtruthorig}/${i}.${imgfiletype} ${groundtruthmni}/${i}.${imgfiletype} 3 ${mnispace}/${i}_rigid.txt ${mnispace}/${i}_moving.txt" "logs/transform${i}.log"
	runcond "${scripts}/threshold.py ${groundtruthmni}/${i}.${imgfiletype} 0.5"
	runcond "${scripts}/closing.py ${groundtruthmni}/${i}.${imgfiletype}"
}

# main code
log 2 "Transfroming all segmentations to template space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize transform ${threadcount} images[@]

