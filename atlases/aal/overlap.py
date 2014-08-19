import numpy
from scipy.stats import itemfreq
from medpy.io import load

ATLAS_FILE = "/data_humbug1/maier/Temp_Pipeline/AtlasOverlap/atlases/aal/aal.nii.gz"

def overlap(img):
    """
    Compute the overlap between an binary image in MNI (SPM) space an the mricron AAL atlas.
    """
    # parse input argument and load atlas
    img = numpy.asarray(img).astype(numpy.bool)
    atl, atlh = load(ATLAS_FILE)
    # remove last slices along all dimensions in MNI image
    img = img[:-1,:-1,:-1]
    # get intersection with atlas areas and return
    area_ids = atl[img]
    # return all except zero-background-area
    return itemfreq(area_ids[area_ids != 0])
    
def size():
    """
    Return the atlas size.
    """
    atl, _ = load(ATLAS_FILE)
    return numpy.count_nonzero(atl != 0)
    
def regions():
    """Return all region ids.
    """
    atl, _ = load(ATLAS_FILE)
    return numpy.unique(atl[atl != 0])
