'''


    Programme pour charger et mesuerer des choses de bases dans une image 
    
    Hypothese: on commence d'une image 16-bit TIFF 3D, ou
        - l'exteriur de  l'echantillon vaut 65535
        - les vides dans l'echantillon vallent 0 
        - la phase solide dans l'echantillon vaut 1
        
    Ce programme ce lance de la maniere suivante:
        python doanTest.py /path/to/image.tif
'''

import sys, os
import numpy
import tifffile

# Pixel size in microns per pixel
pixelSize = 90.0

meanWaterGreyValue = 22444.0
meanGrainGreyValue = 35761.0

# Lire le tif 
grey = tifffile.imread( sys.argv[1] )
bina = tifffile.imread( sys.argv[2] ) 
bina2 = tifffile.imread( sys.argv[3] ) 

print "The size of the image in pixels (Z-Y-X) is:", grey.shape
# Rememeber: in python we access memory in Z-Y-X
print "The size of the image in mm is:", numpy.array( grey.shape )*pixelSize/1000.0

## Try to measure the volume of the sample
## Get all the pixels that are not the outside
#samplePixelsCoords = numpy.where( grey != 0 )
#numberOfSamplePixels = len( samplePixelsCoords[0] )
#print "Sample volume = ", numberOfSamplePixels*(pixelSize/1000.0/10.0)**3, "cm^3"
#print "Volume of cylinder d=7 h=14 = ", (numpy.pi*(7/2.0)**2)*14.0, "cm^3"

## For example, starting from a physically measured large-grain volume (expSolidVolumeMM3 )...
##expSolidVolumeMM3 = 0.4 * numberOfSamplePixels*(pixelSize/1000.0)**3
#expSolidVolumeMM3 = 259739.0
#expSolidVolumeVX  = expSolidVolumeMM3/((pixelSize/1000.0)**3 )

#print "expSolidVolumeVX", expSolidVolumeVX

## ...set the threshold that selects this volume starting from the brightest pixels,
## in the area of the sample.
#solidVolumeImageVX = 0
#currentThreshold = 33000
#while solidVolumeImageVX < expSolidVolumeVX:
    #currentThreshold -= 32
    #solidVolumeImageVX = len( numpy.where( grey[ samplePixelsCoords ] > currentThreshold )[0] )
    #print "Thres = ", currentThreshold, "Solid Vol Ratio = ", solidVolumeImageVX/float(expSolidVolumeVX)
 
## Output image of just solid phase without border
#imSolid = numpy.zeros_like( grey ).astype('<u1')
#imSolid[ numpy.where( grey > currentThreshold ) ] = 255
##imSolid[ numpy.where( grey == 65535 ) ] = 0
#tifffile.imsave( "doanTest-bigGrains.tif", imSolid )

#step = 10
#boxHalfSize = 5

step = 10
boxHalfSize = 5
boxVolume = numpy.power( 2*boxHalfSize + 1, 3)

Zsteps = numpy.arange( step-boxHalfSize,  grey.shape[0], step )
Ysteps = numpy.arange( step-boxHalfSize,  grey.shape[1], step )
Xsteps = numpy.arange( step-boxHalfSize,  grey.shape[2], step )

#volumeFractionMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
masseFineMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
masseGrosMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
#masseFineMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
egMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )

#mfTOT=0
#mcTOT=0

for nZ, Z in enumerate( Zsteps ):
    print Z
    for nY, Y in enumerate( Ysteps ):
        for nX, X in enumerate( Xsteps ):
            subVolumeSlice = (  slice( Z-boxHalfSize, Z+boxHalfSize+1),
                                slice( Y-boxHalfSize, Y+boxHalfSize+1),
                                slice( X-boxHalfSize, X+boxHalfSize+1) )
            
            # exclude mask and solid grains
            #maskCoords = numpy.where[ grey[ subVolumeSlice ] == 0 ]
            #bigGrainsCoords = numpy.where[ bina[ subVolumeSlice ] != 0 ]
            
	    #greyPoints = grey[ subVolumeSlice ][ (bina[ subVolumeSlice ] != 0) & ( grey[ subVolumeSlice ] != 0 )]
            greyPoints = grey[ subVolumeSlice ][ (bina[ subVolumeSlice ] == 0) & ( grey[ subVolumeSlice ] != 0 )]

            if len( greyPoints ) > 0:
                #print greyPoints
                #solidVolumeFraction = (( greyPoints - meanWaterGreyValue ) / float( meanGrainGreyValue - meanWaterGreyValue )).mean()
                #if solidVolumeFraction < 0 :
                 #   solidVolumeFraction = 0
                #if solidVolumeFraction > 1 :
                 #   solidVolumeFraction = 1

                #solidVolumeFraction = (( greyPoints - meanWaterGreyValue ) / float( meanGrainGreyValue - meanWaterGreyValue ))
                #solidVolumeFraction[solidVolumeFraction < 0]  = 0
                #solidVolumeFraction[solidVolumeFraction > 1]  = 1

                mf = ((( greyPoints - meanWaterGreyValue ) / float( meanGrainGreyValue - meanWaterGreyValue )) * ( numpy.power( 0.09, 3 )) * 0.00265).sum() #masse de fines pour chaque cube en gramme 

                #mf = (solidVolumeFraction * ( numpy.power( 0.09, 3 )) * 0.00265).sum()
                #print ( "%.5f" %mf )
		#mfTOT=mfTOT+mf

                masseFineMatrix[ nZ, nY, nX ] = mf


            binaPoints = bina2[ subVolumeSlice ][( bina2[ subVolumeSlice ] != 0 ) & ( grey[ subVolumeSlice ]  != 0 )] 
	    vides = bina2[ subVolumeSlice ][( bina2[ subVolumeSlice ] == 0 ) & ( grey[ subVolumeSlice ]  != 0 )] 

            if len( binaPoints ) > 0 :
                #print binaPoints 
                #mc = ((binaPoints - 254) * ( numpy.power( 0.09, 3 )) * 0.00265).sum() #masse de gros grains pour chaque cube en gramme
		mc = len( binaPoints ) * ( numpy.power( 0.09, 3 )) * 0.00265 #une autre maniere de calculer la masse des gros grains qui donne le meme resultat que la ligne du dessus.
                #print ( "%.5f" %mc )
		#mcTOT=mcTOT+mc

		masseGrosMatrix[ nZ, nY, nX ] = mc

		eg =  len( vides )/float(len( binaPoints ))
		#print eg             
		#eg = (boxVolume * ( numpy.power( 0.09, 3 ))) / (len(binaPoints) * ( numpy.power( 0.09, 3 ))) - 1 #indice des vides entres gros grains
                #print ( "%.5f" %eg )
		
		egMatrix[ nZ, nY, nX ] = eg


videsTOT1 = bina2[(bina2 == 0) & ( grey != 0 )]
videsTOT2 = bina[(bina == 0) & ( grey != 0 )]
videsTOT = (len(videsTOT1) + len( videsTOT2))/2.0
grosTOT = bina2[(bina2 != 0) & ( grey != 0 )] 

egGlobalP = len( videsTOT1 )/float(len( grosTOT ))
egGlobalM = len( videsTOT2 )/float(len( grosTOT ))
egGlobalPM = videsTOT/float(len( grosTOT ))

print "indice des vides intergrains global (+) =", egGlobalP
print "indice des vides intergrains global (moy) =", egGlobalPM
print "indice des vides intergrains global (-) =", egGlobalM

greyPointsMassTOT = grey[ (bina == 0) & ( grey != 0 )]
mfTOT = ((( greyPointsMassTOT - meanWaterGreyValue ) / float( meanGrainGreyValue - meanWaterGreyValue )) * ( numpy.power( 0.09, 3 )) * 0.00265).sum()
mcTOT = len( grosTOT ) * ( numpy.power( 0.09, 3 )) * 0.00265


print "masse fine (vrai?) (g) =", mfTOT
print "masse gros (vrai?) (g) =", mcTOT
print "masse fine (faux? somme sur matrice) (g) =", masseFineMatrix.sum()
print "masse gros (faux? somme sur matrice) (g) =", masseGrosMatrix.sum()
print "fraction massique en fine =", mfTOT/(mfTOT+mcTOT)



tifffile.imsave( "masseFineMatrix.tif", masseFineMatrix) 
tifffile.imsave( "masseGrosMatrix.tif", masseGrosMatrix)  
tifffile.imsave( "egMatrix.tif", egMatrix) 


 
