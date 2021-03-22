import tifffile
import numpy
from numpy import inf, nan
import matplotlib.pyplot as plt
import matplotlib
for i in range(1,8):
    im = '/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/l_strain/ls/H10/tif-volumetric/H10-00-0{}-SF-NoMF-volumetric-largeStrains'.format(i)
    root = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/RSA/Root/H10/Rescaled/H10-0{}-B2-Root-1.tif'.format(i))
    Strain = tifffile.imread(im+'.tif')
    Logscale = numpy.zeros_like(Strain)
    for z in numpy.arange(Strain.shape[0]):
        for y in numpy.arange(Strain.shape[1]):
            for x in numpy.arange(Strain.shape[2]):
                if Strain[z][y][x] < 0:
                    Logscale[z][y][x] = -(4+numpy.log10(abs(Strain[z][y][x])))
                if Strain[z][y][x] > 0:
                    Logscale[z][y][x] =  (4+numpy.log10(abs(Strain[z][y][x])))
    inf_array = numpy.array(numpy.where(Logscale == inf))
    nan_array = numpy.array(numpy.where(Logscale == nan))
    if inf_array.shape[1] > 0:
        print ('there are inf!!!')
    if nan_array.shape[1] > 0:
        print ('there are nan!!!')
    else:
        print ('ok.')
    Strain  [root[0:Strain.shape[0],0:Strain.shape[1],0:Strain.shape[2]] !=0] = nan    
    Logscale[root[0:Strain.shape[0],0:Strain.shape[1],0:Strain.shape[2]] !=0] = nan
    tifffile.imsave(im + 'Mask.tif',Strain)
    tifffile.imsave(im + 'Mask_LOGSCALE.tif',Logscale)


##Print png with Masked root ##
epsv_F = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/l_strain/ls/H10/tif-volumetric/Linscale/H10-00-01-SF-NoMF-volumetric-largeStrainsMask.tif')
#epsv_F = numpy.reshape(epsv_F.shape[0], epsv_F.shape[1], epsv_F.shape[2])
sec1 = epsv_F[44]
sec1 = sec1.reshape(39,39)
cmap = matplotlib.cm.bwr
cmap.set_bad('green')   
plt.imshow(sec1[18:30,14:26], cmap='bwr',vmin=-0.02, vmax=0.02);plt.colorbar();plt.show()


#DeviatoricStrain
for i in range(1,8):
    imd = '//mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/l_strain/ls/H10/glt-root/tif-deviatoric/Linscale/H10-00-0{}-SF-NoMF-deviatoric-largeStrains'.format(i)
    root = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/RSA/Root/H10/Rescaled/H10-0{}-B2-Root-1.tif'.format(i))
    StrainD = tifffile.imread(imd+'.tif')
    StrainD  [root[0:StrainD.shape[0],0:StrainD.shape[1],0:StrainD.shape[2]] !=0] = nan  
    tifffile.imsave(imd + 'Mask.tif',StrainD)

epsd_F = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/l_strain/ls/H10/glt-root/tif-deviatoric/H10-00-01-SF-NoMF-deviatoric-largeStrainsMask.tif')
sec1 = epsd_F[39,:,:]
sec1 = sec1.reshape(39,39)
cmap = matplotlib.cm.plasma
cmap.set_bad('green')   
plt.imshow(sec1[18:30,14:26], cmap='plasma',vmin=0.0, vmax=0.1);plt.colorbar();plt.show()
