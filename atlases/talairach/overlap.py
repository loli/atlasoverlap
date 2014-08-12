import numpy
from scipy.stats import itemfreq
from medpy.io import load
from icbm_spm2tal import icbm_spm2tal

ATLAS_FILE = "/data_humbug1/maier/Temp_Pipeline/AtlasOverlap/atlases/talairach/talairach.nii"

def overlap(img):
    """
    Compute the overlap between an binary image in MNI (SPM) space an the Talairach atlas.
    """
    # parse input argument and load atlas
    img = numpy.asarray(img).astype(numpy.bool)
    atl, atlh = load(ATLAS_FILE)
    # transform indices
    indices_mni = numpy.asarray(img.nonzero()).T
    indices_tal = icbm_spm2tal(indices_mni)
    indices_tal = __round_indices(indices_tal, atl)
    # get intersection with atlas areas and return
    area_ids = atl[tuple(indices_tal.T)]
    return itemfreq(area_ids)
    
def __round_indices(indices, trg_img):
    indices = numpy.around(indices)
    for dim in range(indices.shape[1]):
        mask_upper = indices[:,dim] >= trg_img.shape[dim]
        indices[:,dim][mask_upper] = trg_img.shape[dim] - 1
        mask_lower = indices[:,dim] < 0
        indices[:,dim][mask_lower] = 0
    return indices.astype(numpy.uint)
    
