import sys, os
import numpy
import tifffile

# Pixel size in microns per pixel
pixelSize = 80.0

meanWaterGreyValue = 27146.0
meanAirGreyValue = 16336.0

# Lire le tif 
g = sys.argv[1]
b = sys.argv[2]
grey = tifffile.imread( g )
bina = tifffile.imread( b ) 
#bina2 = tifffile.imread( sys.argv[3] ) 

print "The size of the image in pixels (Z-Y-X) is:", grey.shape
# Rememeber: in python we access memory in Z-Y-X
print "The size of the image in mm is:", numpy.array( grey.shape )*pixelSize/1000.0



step = 20
boxHalfSize = 10
boxVolume = numpy.power( 2*boxHalfSize + 1, 3)

Zsteps = numpy.arange( step-boxHalfSize,  grey.shape[0], step )
Ysteps = numpy.arange( step-boxHalfSize,  grey.shape[1], step )
Xsteps = numpy.arange( step-boxHalfSize,  grey.shape[2], step )

#volumeFractionMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
SaturationDegreeMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
SaturationDegreeMatrix2 = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
#masseGrosMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
#SaturationDegreeMatrix = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )
Porosity = numpy.zeros( ( len(Zsteps), len(Ysteps), len(Xsteps)  ) ,dtype='f4' )

#mwTOT=0
#mcTOT=0
#masswater = 0
for nZ, Z in enumerate( Zsteps ):
    print Z
    for nY, Y in enumerate( Ysteps ):
        for nX, X in enumerate( Xsteps ):
            subVolumeSlice = (  slice( Z-boxHalfSize, Z+boxHalfSize+1),
                                slice( Y-boxHalfSize, Y+boxHalfSize+1),
                                slice( X-boxHalfSize, X+boxHalfSize+1) )
            
            
	    #greyPoints = grey[ subVolumeSlice ][ (bina[ subVolumeSlice ] != 0) & ( grey[ subVolumeSlice ] != 0 )]
            greyPoints = grey[ subVolumeSlice ][ (bina[ subVolumeSlice ] == 0) & ( grey[ subVolumeSlice ] != 0 )]

            if len( greyPoints ) > 0:
                

                mw = (( greyPoints - meanAirGreyValue ) / float( meanWaterGreyValue - meanAirGreyValue)).mean() 
                masswater = ((( greyPoints - meanAirGreyValue ) / float( meanWaterGreyValue - meanAirGreyValue))*(numpy.power((pixelSize/1000),3))*(0.000998)).sum()
               # mw1 = (( greyPoints - meanAirGreyValue ) / float( meanWaterGreyValue - meanAirGreyValue)).mean()-1
                
                #masse de fines pour chaque cube en gramme 
                #mw = (( greyPoints - meanWaterGreyValue ) / float( meanAirGreyValue - meanWaterGreyValue ))
                #mw = (solidVolumeFraction * ( numpy.power( 0.09, 3 )) * 0.00265).sum()
               
                SaturationDegreeMatrix[ nZ, nY, nX ] = mw
                #SaturationDegreeMatrix1[ nZ, nY, nX ] = mw1
                realmw = ((( greyPoints - meanAirGreyValue ) / (float( meanWaterGreyValue - meanAirGreyValue )) * ( numpy.power( 0.08, 3 )) * 0.00099)).sum()
                SaturationDegreeMatrix2[ nZ, nY, nX ] = realmw
            binaPoints = bina[ subVolumeSlice ][( bina[ subVolumeSlice ] != 0 ) & ( grey[ subVolumeSlice ]  != 0 )] 
	    vides = bina[ subVolumeSlice ][( bina[ subVolumeSlice ] == 0 ) & ( grey[ subVolumeSlice ]  != 0 )] 

            if len( binaPoints ) > 0 :
                ##print binaPoints 
                ##mc = ((binaPoints - 254) * ( numpy.power( 0.09, 3 )) * 0.00265).sum() #masse de gros grains pour chaque cube en gramme
		#mc = len( binaPoints ) * ( numpy.power( 0.09, 3 )) * 0.00265 #une autre maniere de calculer la masse des gros grains qui donne le meme resultat que la ligne du dessus.
                ##print ( "%.5f" %mc )
		##mcTOT=mcTOT+mc

		#masseGrosMatrix[ nZ, nY, nX ] = mc
#porosity#
		eg =  len( vides )/(float(len( binaPoints ))+float(len( vides)))
		#print eg             
		#eg = (boxVolume * ( numpy.power( 0.09, 3 ))) / (len(binaPoints) * ( numpy.power( 0.09, 3 ))) - 1 #indice des vides entres gros grains
                #print ( "%.5f" %eg )
		
		Porosity[ nZ, nY, nX ] = eg


#greyPointsMassTOT = grey[ (bina == 0) & ( grey != 0 )]
#mwTOT = ((( greyPointsMassTOT - meanWaterGreyValue ) / float( meanAirGreyValue - meanWaterGreyValue )) * ( numpy.power( 0.08, 3 )) * 0.00099).sum()
#mcTOT = len( grosTOT ) * ( numpy.power( 0.09, 3 )) * 0.00265
por0 = (Porosity).mean()
por = (Porosity>0).mean()
tifffile.imsave( g +"SatMap.tif", SaturationDegreeMatrix)
#tifffile.imsave( "H10-0WSaturationMap1-hws10.tif", SaturationDegreeMatrix1) 
#tifffile.imsave( "masseGrosMatrix.tif", masseGrosMatrix)  
tifffile.imsave( g +"PorField.tif", Porosity)  
#print masswater
print "porosity in average is:", por, por0
print "max Value Saturation Degree", SaturationDegreeMatrix.max(),SaturationDegreeMatrix.max()
print "min Value Saturation Degree", SaturationDegreeMatrix.min(), SaturationDegreeMatrix.min()
print "mean Value Saturation Degree", SaturationDegreeMatrix.mean(), SaturationDegreeMatrix.mean()
greyPointMassTOT = grey[ (bina == 0)&( grey !=0)]

mwTOT = ((( greyPointMassTOT - meanAirGreyValue)/(float (meanWaterGreyValue - meanAirGreyValue)) * (numpy.power(0.008,3))*0.99)).sum()
mwTOT2 = ((SaturationDegreeMatrix*16*16*16)*(numpy.power(0.008,3))*0.99).sum()
print "water mass=" , mwTOT, mwTOT2
#print "porosity", Porosity
