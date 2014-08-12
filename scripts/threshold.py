#!/usr/bin/python

"""
Thresholds an image according to a value (True where intensity >= value) in place.
arg1: the input image
arg2: the threshold
"""

import sys
import numpy

from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	thr = float(sys.argv[2])
	
	i = i.copy()

	save(i >= thr, sys.argv[1], h)

if __name__ == "__main__":
	main()
