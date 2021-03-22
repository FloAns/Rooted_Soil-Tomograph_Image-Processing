##FA 12/17

##Apply variance 3D on Bilateral filteres 3D images
import tifffile
import numpy
import sys
import matplotlib.pyplot as plt
import scipy.ndimage

##choose the option file by file or set with for loop
im = sys.argv[1]
#for i in range(1,8):
var3D = tifffile.imread(im+".tif")
#var3D = tifffile.imread("{}.tif".format(i))
##choose threshold on Day 00.
##Apply same threshold Day 00 -> Day 07
upperlevel= sys.argv[2]
lowerlevel= sys.argv[3]
step1 = numpy.zeros_like(var3D)
step1[(var3D>lowerlevel)&(var3D<upperlevel)]=255
step2=scipy.ndimage.label(step1)
tifffile.imsave(im+"pixelconnected-labels.tif", step2[0].astype('<u2'))
##Look at the histogram
##Highest peak: background
plt.imshow(step3[:,300,:]);plt.show()
## Label = 0 is the background, the higest peak is the root - unless problem...(To double ckeck, always)
##choose label either manual input of by studying the histogram, the label is the modal value
#label= input("Please enter something: ")
#print("You entered: " + label)
hist = numpy.histogram(step3, bins = 65535, range = [0,65535])
freq = hist[0]
maxfreq = float((numpy.where(freq[1:65535] == freq[1:65535].max()))[0][0])
label= hist[1][maxfreq]
Root = numpy.zeros_like(var3D)
Root[step3==label]=255
tifffile.imsave(im+"RootSystem.tif",Root)

