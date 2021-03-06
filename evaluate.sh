#!/bin/bash

####
# Evaluate the results of a segmentation
####

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Compute overall evaluation" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
#runcond "${scripts}/evaluate.py ${segmentationsorig}/{}.${imgfiletype} ${groundtruthorig}/{}.${imgfiletype} ${brainmasksorig}/{}.${imgfiletype} $(joinarr " " ${images[@]})"
runcond "${scripts}/evaluate.py ${segmentationsmni}/{}.${imgfiletype} ${groundtruthmni}/{}.${imgfiletype} templates/brainmask_binary.nii.gz $(joinarr " " ${images[@]})"

