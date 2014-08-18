#!/usr/bin/python

"""
Fits an image into the space of another one with possible extention of the space by zeros or cutting off sides.
arg1: the image to fit (in place)
arg2: the reference image
"""

# includes
import sys
import numpy
from medpy.io import load, save

# code
def main():
    i, h = load(sys.argv[1])
    r, _ = load(sys.argv[2])

    diff = numpy.asarray(r.shape) - numpy.asarray(i.shape)

    if numpy.any(diff < 0): # cut to fit
        slicers = [slice(None) if 0 == e else slice(abs(e) / 2, -1 * (abs(e) / 2 + abs(e) % 2)) for e in diff]
        o = i[slicers]
        
    else: # pad to fit
        padding = [(e / 2, e / 2 + e % 2) for e in diff]
        o = numpy.pad(i, padding, "constant")

    save(o, sys.argv[1], h, True)

if __name__ == "__main__":
	main()
