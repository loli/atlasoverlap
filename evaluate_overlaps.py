#!/usr/bin/python

"""
Evaluate the segmentation created by atals overlaps.
arg1: the segmentation result for each case, with a {} in place of the case number
arg2: the ground truth segmentation, with a {} in place of the case number
arg3: the cases mask file, with a {} in place of the case number
arg4+: the cases to evaluate
"""

import sys
import math
import time
from multiprocessing.pool import Pool
from atlases.talairach.overlap import overlap, size, regions
#from atlases.aal.overlap import overlap, size, regions

import numpy
from medpy.io import load, header

# constants
n_jobs = 6
silent = True

def main():

	# catch parameters
	segmentation_base_string = sys.argv[1]
	ground_truth_base_string = sys.argv[2]
	mask_file_base_string = sys.argv[3]
	cases = sys.argv[4:]	

	# load images and apply mask to segmentation and ground truth (to remove ground truth fg outside of brain mask)
	splush = [load(segmentation_base_string.format(case)) for case in cases]
	tplush = [load(ground_truth_base_string.format(case)) for case in cases]
	masks = [load(mask_file_base_string.format(case))[0].astype(numpy.bool) for case in cases]

	s = [s.astype(numpy.bool) & m for (s, _), m in zip(splush, masks)]
	t = [t.astype(numpy.bool) & m for (t, _), m in zip(tplush, masks)]
	hs = [h for _, h in splush]
	ht = [h for _, h in tplush]
	
	# compute overlaps
	ot = [overlap(_t) for _t in t]
	os = [overlap(_s) for _s in s]
	print 'Real region overlaps vs. found region overlaps:'
	print 'CaseID\treal\tfound\tintersection'
	intersection = [set(map(lambda x: x[0], _ot)).intersection(map(lambda x: x[0], _os)) for _ot, _os in zip(ot, os)]
	for cid, tol, sol, ints in zip(cases, map(lambda x: len(x), ot), map(lambda x: len(x), os), intersection):
	    print '{}\t{}\t{}\t{}'.format(cid, tol, sol, len(ints))

	# compute metrics (Pool-processing)
	pool = Pool(n_jobs)
	rws = numpy.asarray(pool.map(regionwise, zip(ot, os)))
	#pws = numpy.asarray(pool.map(pointwise, zip(ot, os)))
	
	# collect and compute metrics
	rtp = rws[:,0]
	rtn = rws[:,1]
	rfp = rws[:,2]
	rfn = rws[:,3]	
	rtpr = numpy.divide(rtp.astype(numpy.float), numpy.add(rtp, rfn))
	rtnr = numpy.divide(rtn.astype(numpy.float), numpy.add(rfp, rtn))	
	rfnr = numpy.divide(rfn.astype(numpy.float), numpy.add(rtp, rfn))
	rfpr = numpy.divide(rfp.astype(numpy.float), numpy.add(rfp, rtn))
	
	#ptp = rws[:,0]
	#pfp = rws[:,1]
	#pfn = rws[:,2]
	#ptpr = numpy.divide(ptp.astype(numpy.float), numpy.add(ptp, pfn))
	#ptnr = numpy.divide(ptn.astype(numpy.float), numpy.add(pfp, ptn))
	#pfnr = numpy.divide(pfn.astype(numpy.float), numpy.add(ptp, pfn))
	#pfor = numpy.divide(pfn.astype(numpy.float), numpy.add(ptn, pfn))
	#pnpv = numpy.divide(ptn.astype(numpy.float), numpy.add(ptn, pfn))	

	# print case-wise results
	print 'Metrics:'
	#print 'Case\trTPR\trFNR\trFOR\trNPV\tpTPR\tpFNR\tpFOR\tpNPV\t'
    #	for x in zip(cases, rtpr, rfnr, ffor, fnpv, ptpr, pfnr, pfor, pnpv):
    #    	print '{}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}'.format(*x)
	print 'Case\trTPR\trTNR\trFNR\trFPR'
    	for x in zip(cases, rtpr, rtnr, rfnr, rfpr): #, ptpr, pfnr):
        	print '{}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}'.format(*x)        	
        
	# check for nan/inf values of failed cases and signal warning
	mask = numpy.isfinite(rtpr)
	if not numpy.all(mask):
	    print 'WARNING: Average values only computed on {} of {} cases!'.format(numpy.count_nonzero(mask), mask.size)

	# print averages
	print 'rTPR average\t{} +/- {} (Median: {})'.format(numpy.asarray(rtpr)[mask].mean(), numpy.asarray(rtpr)[mask].std(), numpy.median(numpy.asarray(rtpr)[mask]))
	print 'rTNR average\t{} +/- {} (Median: {})'.format(numpy.asarray(rtnr)[mask].mean(), numpy.asarray(rtnr)[mask].std(), numpy.median(numpy.asarray(rtnr)[mask]))
	print 'rFNR average\t{} +/- {} (Median: {})'.format(numpy.asarray(rfnr)[mask].mean(), numpy.asarray(rfnr)[mask].std(), numpy.median(numpy.asarray(rfnr)[mask]))
	print 'rFPR average\t{} +/- {} (Median: {})'.format(numpy.asarray(rfpr)[mask].mean(), numpy.asarray(rfpr)[mask].std(), numpy.median(numpy.asarray(rfpr)[mask]))
	
	#print 'pTPR average\t{} +/- {} (Median: {})'.format(numpy.asarray(ptpr)[mask].mean(), numpy.asarray(ptpr)[mask].std(), numpy.median(numpy.asarray(ptpr)[mask]))
	#print 'pFNR average\t{} +/- {} (Median: {})'.format(numpy.asarray(pfnr)[mask].mean(), numpy.asarray(pfnr)[mask].std(), numpy.median(numpy.asarray(pfnr)[mask]))
	#print 'pFOR average\t{} +/- {} (Median: {})'.format(numpy.asarray(pfor)[mask].mean(), numpy.asarray(pfor)[mask].std(), numpy.median(numpy.asarray(pfor)[mask]))
	#print 'pNPV average\t{} +/- {} (Median: {})'.format(numpy.asarray(pnpv)[mask].mean(), numpy.asarray(pnpv)[mask].std(), numpy.median(numpy.asarray(pnpv)[mask]))				

def regionwise(x):
    """Computes the t/n rates in terms of regions."""
    t, s = x
    # consider only region ids, not frequency
    t = set(t[:,0])
    s = set(s[:,0])
    allr = set(regions())
    # compute measures
    tp = len(t.intersection(s))
    tn = len(allr - t - s)
    fp = len(s - t)
    fn = len(t - s)
    # return
    return tp, tn, fp, fn

def pointwise(x):
    """Computes the t/n rates in terms of voxels."""
    t, s = x
    # get all region ids
    allr = set(regions())
    # prepare collectors
    tp = []
    fp = []
    tn = []
    fn = []
    # for each region, compute tp, fp, tn and fn
    for r in allr:
        
        # compute measures
        tp = len(t.intersection(s))
        tn = len(allr - t - s)
        fp = len(s - t)
        fn = len(t - s)
    
    for i, n in t:
        if not i in s[:,0]:
            fn += n
        else:
            d = n - s[numpy.where(s[:,0] == i)[0][0]][1]
            tp += n - max(0, d)
            if d > 0:
                fn += n
            else:
                fp += n
    
    for i, n in s:
        if not i in t[:,0]:
            fp += n
    
    return tp, fp, fn

if __name__ == "__main__":
	main()
