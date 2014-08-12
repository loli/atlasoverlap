#!/usr/bin/python

"""
Performs binary closing on an image in place.
arg1: the input image to close
"""

import sys
import numpy
from scipy.ndimage import binary_closing, binary_fill_holes

from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	
	i = i.copy()
	i = binary_closing(i, iterations=1)
	i = morphology2d(binary_closing, i, iterations=4)
	i = fill2d(i)
	

	save(i, sys.argv[1], h)
	
def morphology2d(operation, arr, structure = None, iterations=1, dimension = 2):
	res = numpy.zeros(arr.shape, numpy.bool)
	for sl in range(arr.shape[dimension]):	
		res[:,:,sl] = operation(arr[:,:,sl], structure, iterations)
	return res
	
def fill2d(arr, structure = None, dimension = 2):
	res = numpy.zeros(arr.shape, numpy.bool)
	for sl in range(arr.shape[dimension]):	
		res[:,:,sl] = binary_fill_holes(arr[:,:,sl], structure)
	return res	

if __name__ == "__main__":
	main()
