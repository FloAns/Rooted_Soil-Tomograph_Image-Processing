#The code identifies the grey scale threshold corresponding to the correct sand grain volume within the system
#Accordingly the porosity Profile in displayed
# MAIN OUTPUT: the binarised 3D image 
# MAIN INPUT : the greyscale 3D image

import tifffile
import numpy
import sys
import matplotlib.pyplot as plt
import scipy.ndimage

############################
gv = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/gv_profiles-correct/H10/H10-01-CorrectedGVRegBin2-RIGID.tifcorrect.tif')
mask = tifffile.imre
############################
im = sys.argv[1]
mask = tifffile.imread(sys.argv[2])
root = tifffile.imread(sys.argv[3])
gvimage = tifffile.imread(im+'.tif')
print "gv read"
upperlevel = 130
lowerlevel = 1550
print "mask read"
#mask[mask==0]=1
#mask[mask==255]=0
plt.imshow(mask[:,300,:]);plt.show()
newImage = numpy.zeros(gvimage.shape)
newImage = gvimage.copy().astype('<f4')*mask.copy().astype('<f4')
plt.imshow(newImage[300,:,:]);plt.show()
bins = 65536
ran = [0,65535]
hist = numpy.histogram(newImage, bins, ran)
print "histogram", hist
freq = hist[0] 
gv= hist[1]
count = 0
ran = numpy.arange(0,65535)
#let's measure the grains volume in px
# V[cm3] = mass/ rho 
# V[px] = V[cm3] / micron3
grainsVolume= 522639590
for i in reversed(ran):
    count += freq[i]
    if count > grainsVolume:
        thresholdGrains = i
        print thresholdGrains
        break
print "threshold grains:", thresholdGrains
grains = newImage.copy().astype('<f4')>thresholdGrains
plt.imshow(grains[300,:,:]);plt.show()
#now grains is a boolean
grains = grains*1
plt.imshow(grains[300,:,:]);plt.show()
grains[grains==1]=255
#newImage[upperlevel:lowerlevel,:,:] = gvimage[upperlevel:lowerlevel,:,:]
#let's clean the image
newImage = grains.copy().astype('<f4')+mask.copy().astype('<f4')
#newImage = grains.copy().astype('<f4')*mask.copy().astype('<f4')
#apply the mask the pores became 1 and the outside remains 0
newImage[newImage==256]=255
plt.imshow(newImage[300,:,:]);plt.show()

print "new image done"
#plt.imshow(newImage[300,:,:]);plt.show()
tifffile.imsave(im+"Grains.tif", numpy.uint8(newImage))
root[root == 255] = 1
root[root == 0]=255
root[root == 1]=0
trin = numpy.zeros(gvimage.shape)
root = scipy.ndimage.morphology.binary_dilation(root)
root = root*1
root[root==1]=128
plt.imshow(root[:,300,:]);plt.show()

trin = newImage+root
plt.imshow(trin[:,500,:]);plt.show()
tifffile.imsave(im+"Trin.tif", numpy.uint8(trin))

porosity = numpy.zeros((newImage.shape[0]))
for i in range(300,1900):
    print i
    p = float((trin[i,:,:] == por).sum())
    print p
    g = float((trin[i,:,:] == gra).sum())
    print g
    porosity[i] = float((p/(p+g)))
    print porosity[i]
porosity
porosity.shape
slice = []
for i in range(0,2000):
    slice.append(i)
slice2 = numpy.array(slice)
plt.plot(porosity,slice2)
plt.show()
PorTr = numpy.column_stack((slice2, porosity))
numpy.savetxt(im+"P.txt", PorTr, delimiter='\t')
#2 grains step
porosityG = []
for i in range(300,1500,(2*D50)):
    print i
    p = float((trin[i,:,:] == por).sum())
    print p
    g = float((trin[i,:,:] == gra).sum())
    print g
    n = float((p/(p+g)))
    porosityG.append(n)
PorosityG=numpy.asarray(porosityG) 
slice = []
l = PorosityG.shape[0]
for i in range(0,l,(2*D50)):
    slice.append(i)
slice2 = numpy.array(slice)
plt.plot(PorosityG)
plt.show()
numpy.savetxt(im+"2g_step.txt", PorosityG, delimiter='\t')
trin = tifffile.imread("/media/fanselmucci/TOSHIBA EXT/M1/trin/M2-01-Bin2.tifcorrect-16Trin.tif")
#PorTr = numpy.column_stack((slice2, PorosityG))
porosityG = []
for i in range(300,1900,(D50)):
    print i
    p = float((trin[i,:,:] == por).sum())
    print p
    g = float((trin[i,:,:] == gra).sum())
    print g
    n = float((p/(p+g)))
    porosityG.append(n)
PorosityG=numpy.asarray(porosityG) 
slice = []
l = PorosityG.shape[0]
for i in range(0,l,(D50)):
    slice.append(i)
slice2 = numpy.array(slice)
plt.plot(PorosityG)
plt.show()
numpy.savetxt(im+"g_step.txt", PorosityG, delimiter='\t')



###For deformed Images###
for k in numpy.arange(1,7):
    root = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/RSA/Root/H10/H10-00-CorrectedGVRegBin2-Root.tif')
    #plt.imshow(root[300,:,:]);plt.show()
    root[root==255]=1
    #plt.imshow(root[300,:,:]);plt.show()
    mask = tifffile.imread('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/mask/H10-mask.tif')
    #plt.imshow(mask[300,:,:]);plt.show()
    mask[mask==1]=255
    #plt.imshow(mask[300,:,:]);plt.show()
    #plt.imshow(mask[300,:,:]);plt.show()
    mask[mask==0]=1
    #plt.imshow(mask[300,:,:]);plt.show()
    mask[mask==255]=0
    #plt.imshow(mask[300,:,:]);plt.show()
    newImage = mask + root
    #plt.imshow(newImage[300,:,:]);plt.show()

    im = '/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/Deformed_GV/H10-00-def0{}'.format(k)
    gvimage = tifffile.imread(im+'.tif')
    gvImage = gvimage.copy().astype('<f4')
    #plt.imshow(gvImage[300,:,:]);plt.show()
    bins = 65536
    ran = [0,65535]
    hist = numpy.histogram(gvImage, bins, ran)
    print( "histogram", hist)
    freq = hist[0] 
    gv= hist[1]
    count = 0
    ran = numpy.arange(0,65535)
    grainsVolume=228012547
    for i in reversed(ran):
        count += freq[i]
        if count > grainsVolume:
            thresholdGrains = i
            print( thresholdGrains)
            break
    print( "threshold grains:", thresholdGrains)
    grains = gvImage.copy().astype('<f4')>thresholdGrains
    #plt.imshow(grains[300,:,:]);plt.show()
    grains = grains*1
    #plt.imshow(grains[300,:,:]);plt.show()
    grains[grains==1]=255
    newImage = newImage+grains
    #plt.imshow(newImage[300,:,:]);plt.show()
    tifffile.imsave('/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/grains/H10/H10-00-def0{}_grains.tif'.format(k),numpy.int8(newImage))

