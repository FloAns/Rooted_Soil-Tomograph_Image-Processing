#FA: 3D Root diameter distriburion 
import sys
import tifffile
import scipy.ndimage
import spam.helpers
import skimage.morphology 

root = sys.argv[1]
skeleton = skimage.morphology.skeletonize_3d(root) 
DistanceMap = scipy.ndimage.distance_transform_edt(root)
tifffile.imsave("/mnt/tomo2/SCAN/GEO/Floriana/Organized/2018-06/H10-MaizeinHN31Loose/Root Vectorialization/H10-0W-DistanceM.tif", DistanceMap)
spam.helpers.writeGlyphsVTK(numpy.array(numpy.where(skeleton==255)).T,{'diam':DistanceMap [skeleton==255]},fileName="/mnt/tomo2/SCAN/GEO/Floriana/Organized/2018-06/H10-MaizeinHN31Loose/Root Vectorialization/H10-0W-RootBin2DistanceMap_onTheSkeleton.vtk") 
