import numpy

def icbm_spm2tal(inpoints):
    """
    Convert coordinates from MNI space (normalized using the SPM software package) to
    Talairach space using the icbm2tal transform developed and validated by Jack
    Lancaster at the Research Imaging Center in San Antonio, Texas.
    
    http://www3.interscience.wiley.com/cgi-bin/abstract/114104479/ABSTRACT
    
    Modelled after icbm_spm2tal.m from http://www.talairach.org/.
    
    Implemented by:
        Oskar Maier
        August 2014
        maier@imi.uni-luebeck.de
        
    @param inpoints a list or MNI (SPM) coordinates
    @return the coordinates transformed to talairach space
    """
    inpoints = numpy.asarray(inpoints).T
    
    # check input array
    if not 2 == inpoints.ndim:
        raise Exception("Input array must have dimensionality of 2.")
    if not 3 == inpoints.shape[0]:
        raise Exception("Input array must be of shape (3, x).")

    # transformation matrices, different for each software package
    icbm_spm = [[ 0.9254, 0.0024, -0.0118, -1.0207],
                [-0.0048, 0.9316, -0.0871, -1.7667],
                [ 0.0152, 0.0883,  0.8924,  4.0926],
                [ 0.0000, 0.0000,  0.0000,  1.0000]]
    icbm_spm = numpy.asarray(icbm_spm)
                                
    # apply and return
    inpoints = numpy.vstack((inpoints, numpy.ones((1,inpoints.shape[1]))))
    return numpy.dot(icbm_spm, inpoints).T[:,:3]

