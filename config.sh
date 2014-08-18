#!/bin/bash

######################
# Configuration file #
######################

## changelog
# 2014-08-08 created

# image array
images=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '19' '20' '21' '23' '25' '26' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # NeuroImage

# ground truth set
gtset="GTG"

# evaluation ground truth set
evalgtset="GTG"

# sequence on which to perform
basesequence="flair_tra"

# sequence sub-sample space definition
isotropic=1 # 1/0 to signal that sub-sampling did or did not take place
isotropicspacing=3 # the target isotropic spacing in mm of the sub-sampling

