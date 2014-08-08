#!/bin/bash

#####
# Creates a head mask using the base sequence image.
#####

## Changelog
# 2014-08-08 created

# include shared information
source $(dirname $0)/include.sh

# functions
###
# Compute a head mask using the base sequence
###
function compute_headmask ()
{
	# grab parameters
	i=$1

	# continue if target file already exists
	if [ -f "${headmasks}/${i}.${imgfiletype}" ]; then
		return
	fi
	# compute head mask
	log 1 "Computing head mask for ${originals}/${i}/${basesequence}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/headmask.py ${originals}/${i}/${basesequence}.${imgfiletype} ${headmasks}/${i}.${imgfiletype}"
}

# main code
log 2 "Computing head masks on base sequence ${basesequence}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize compute_headmask ${threadcount} images[@]

