## INPUT: Set of 3D images of the same sample
## OUTPUT:Set of 3D images of the same sample and normalised Grey scale distribution

import tifffile as tif
import matplotlib.pyplot as plt
import numpy as np
import pylab as plb
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy.signal import find_peaks_cwt
from matplotlib import pyplot


import matplotlib.cm as cm

import scipy.misc


DETECT_PEAKS = False
GAUSSIAN_FIT = False
RESCALE      = True

# one day this will be automatic...
darkPeak  = [ 13823.789, 14591.777,15103.77, 14335.781, 14079.785,  14335.781, 14079.785 ]
lightPeak = [ 41727.363, 42751.384, 41215.371, 41983.359, 41727.363, 42751.384, 41471.367]

nSteps = float(len( lightPeak ))


def histogramOnMidBin( matrix, bins=255, range=(0,255) ):
    import numpy
    """
        Since numpy.histogram returns intervals and bin counts (and there is one more interval than the number of bins)
        here we will return bin counts and the middle of the bins
    """
    results = numpy.histogram( matrix, bins=bins, range=range )
    
    binWidth = ( range[1]-range[0] ) / float( bins )
    #print "binWidth = ",binWidth
    
    return [ results[0], results[1][0:-1]+ ( binWidth/2.0 ) ]


    
for n, step in enumerate( range(1,8) ):
    print "Working on step {step:02d}".format( step=step ) 

    # load a tiff image (this is 16b) load it as 32b
   # #image = tif.imread('/mnt/tomo2/SCAN/GEO/Floriana/2017-11/Maize/Maize2/Tomographies/SliceY_{step:02d}Maize2_16bit.tif'.format( step=step) ).astype(np.float32)
    image = tif.imread("SlicesY_01Maize2_16bit.tif".format( step=step) ).astype(np.float32)
                      


    imageHistogramCounts, imageHistogramMidBin = histogramOnMidBin( image, bins=255, range=(0,255) )

    #a = plt.hist(image.ravel(), bins = np.arange(0,260,1))
    plt.subplot( 1,2,1 )
    plt.plot( imageHistogramMidBin,
              imageHistogramCounts/float(imageHistogramCounts.max() ),
              label='Step = {step:02d}'.format( step=step ),
              color=(1.0-n*(1/(nSteps-1)),0.0,n*(1/(nSteps-1))) )
    plt.title('Original Histogram')
    plt.xlabel('Greyvalue (Middle of Bin)')
    plt.ylabel('Count')


    #filename = 'mean_var.txt'


    #print a[1].mean()
    #print a[1].var()
    #mean = a[1].mean()
    #std = a[1].std()
    #GV = a[1]
    #print GV.shape
    #GV = np.delete(GV,0)
    #print GV.shape
    #F = a[0]
    #print F.shape

    Hist = np.zeros((len(imageHistogramMidBin),2))
    print Hist.shape

    Hist[:,0] = imageHistogramCounts/float(imageHistogramCounts.max())
    Hist[:,1] = imageHistogramMidBin

    #print a[1].mean()
    #print Hist[:,1].mean()

    #with open(filename, "w") as f:
            #f.write('#Mean \t#Var \n')
            #f.write('{} \t  {}\n'.format(a[1].mean(),a[1].std()))
    #f.close()
    
    np.savetxt('Step01.txt'.format( step=step), Hist)
    ##np.savetxt('/mnt/tomo2/SCAN/GEO/Floriana/2017-11/Maize/Maize2/Tomographies/step{step:02d}.txt'.format( step=step), Hist)
    #plt.title ("histogram grey value-frequency 04")
    #plt.xlabel("grey values")
    #plt.ylabel("frequency")
    #plt.savefig('Histogram 03.png')
    #plt.show()

    #filename2 = 'mean_var.txt'

    if DETECT_PEAKS:
        import pypeaks
        import peakdetect

        import peakutils
        from peakutils.plot import plot as pplot
        
        indexes = peakutils.indexes(F, thres=0.5, min_dist=30)
        print(indexes)
        print(GV[indexes], F[indexes])
        pyplot.figure(figsize=(10,6))
        pplot(GV, F, indexes)
        pyplot.title('First estimate')
        plt.savefig('MainPeak3_2.png')
        pyplot.show()

        import peakutils.peak
        indexs = peakutils.peak.indexes(np.array(F),
            thres=1.0/max(F), min_dist=2)
        print('Peaks are: %s' % (indexs))
        pplot(GV, F, indexs)
        plt.savefig('allpeaks3_2.png')
        pyplot.show()

        peaks = peakdetect.peakdetect(np.array(F), lookahead=2, delta=2)
        indexes = []
        for posOrNegPeaks in peaks:
            for peak in posOrNegPeaks:
                indexes.append(peak[0])
        print('Peaks are: %s' % (indexes))
        pplot(GV, F, indexs)
        plt.savefig('peaks3.png')

        with open(filename2, "w") as f:
                f.write('Peak \t ')
                f.write('{} \t '.format(indexes))
        f.close()

        pyplot.show()


    if GAUSSIAN_FIT:
        GV1 = np.array(GV - 100)
        GV2 = np.array(GV1/ 2*200)
        GV3 = np.array(GV2 + 0.25)
        GV1.astype(float)
        GV2.astype(float)
        GV3.astype(float)

        array2 = np.zeros((len(GV),2))
        array2[:,0] = F
        array2[:,1] = GV3
        print array2

        plt.plot (GV1,F)
        plt.savefig('p03rescaleStep1.png')
        pyplot.show()
        plt.plot (GV2,F)
        plt.savefig('p03rescaleStep2.png')
        pyplot.show()
        plt.plot (GV3,F)
        plt.savefig('p03rescaleStep3.png')
        pyplot.show()
        #tranfor,m the negative value in 0
        GV4 = GV3.clip(0)
        plt.plot (GV4,F)
        plt.savefig('p03rescaleStep4.png')
        pyplot.show()


        def gaus(GV,a,x0,std):
            return a*exp(-(GV-x0)**2/(2*std**2))
        popt,pcov = curve_fit(gaus,GV,F,p0=[1,mean,std])

        plt.plot(GV,F,'b+:', label='data')
        plt.plot(GV,gaus(GV,*popt),'ro:',label='fit')
        plt.legend()
        plt.title('Gaussian Fit')
        plt.xlabel('grey values')
        plt.ylabel('frequency')
        plt.savefig('Gaussian3_2.png')
        plt.show()

        array3 = np.zeros((len(GV),2))
        array3[:,0] = F
        array3[:,1] = GV4

    if RESCALE:
        corrected_image = image.copy() - darkPeak[ n ]
        corrected_image = corrected_image / ( 2.0*( lightPeak[ n ] - darkPeak[ n ] ) )
        corrected_image += 14335.781
        imageHistogramCounts32b, imageHistogramMidBin32b = histogramOnMidBin( corrected_image, bins=255, range=(0.0,65535.0) )
        
        # remove zero counts ... this is cheating
        zeroCoords = np.where( imageHistogramCounts32b == 0 )
        imageHistogramCounts32b = np.delete( imageHistogramCounts32b, zeroCoords )
        imageHistogramMidBin32b = np.delete( imageHistogramMidBin32b, zeroCoords )
        
        plt.subplot( 1,2,2 )
        #a = plt.hist(image.ravel(), bins = np.arange(0,260,1))
        plt.plot( imageHistogramMidBin32b,
                  imageHistogramCounts32b/float(imageHistogramCounts32b.max()),
                  label='Step = {step:02d}'.format( step=step ),
                  color=(1.0-n*(1/(nSteps-1)),0.0,n*(1/(nSteps-1))))
        plt.title('Scaled Histogram')
        plt.xlabel('Greyvalue (Middle of Bin)')
        plt.ylabel('Count')
        #plt.show()
        
        HistResc = np.zeros((len(imageHistogramMidBin32b),2))
        print HistResc.shape

        HistResc[:,0] = imageHistogramCounts32b/float(imageHistogramCounts32b.max())
        HistResc[:,1] = imageHistogramMidBin32b        
        np.savetxt('Rescaledstep01.txt'.format( step=step), HistResc)
        ##np.savetxt('/mnt/tomo2/SCAN/GEO/Floriana/2017-11/Maize/Maize2/Tomographies/Rescaledstep{step:02d}.txt'.format( step=step), HistResc)
        
        tif.imsave( 'Maize2RescaledStep01.tif'.format( step=step), corrected_image)

        ##tif.imsave( '/mnt/tomo2/SCAN/GEO/Floriana/2017-11/Maize/Maize2/Tomographies/MAize2RescaledStep{step:02d}.tif'.format( step=step), corrected_image)



    #GV_1 = b[1]
    #F_1 = b[0]
    #GV_1 = np.delete(GV_1,0)
    #Hist1 = np.zeros((len(GV_1),2))
    #Hist1[:,0] = F_1
    #Hist1[:,1] = GV_1
    #np.savetxt('hist3_2Corr.txt', Hist1)
    #plt.savefig('HistogramRescaled3_2.png')
    #plt.show()

    #tif.imsave( "03_2CorrectedOk.tif", corrected_image)

plt.subplot( 1,2,1 )
plt.legend()
plt.subplot( 1,2,2 )
plt.legend()
plt.savefig('HistogramRescaled1stArea.png')
plt.show()
