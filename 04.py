"""
2019-09-06 FA
Load vectors, and looks at, for example, greylevels in the plane perpendicular to the root axis
"""

import numpy
import spam.DIC
import sys
import tifffile
import matplotlib.pyplot as plt
import scipy.ndimage

# Number of pixels + and - to extract along the root
imSize = 150

interpolationOrder = 1
#for i in range(0,8):
    #data = numpy.load("H10-0{}-skeleton.tif-output-vectors.npy".format(i), allow_pickle=True, encoding='bytes')
    #greys = tifffile.imread("H10-0{}-CorrectedOK2-BIN2-Root-NoSEED.tif".format(i))
for i in range(0,8):
    print "image:"
    print i
    data = numpy.load("/media/fanselmucci/TOSHIBA EXT/H7Porosity/skeleton/H7-06-sk-extendedR4.tif-output-vectors.npy", allow_pickle=True, encoding='bytes')
    greys = tifffile.imread("/media/fanselmucci/TOSHIBA EXT/H7Porosity/correct/Trin/H7-0{}-Bin2-Registered.tifcorrectTrin.tif".format(i))

    # unpack data into variables
    points  = data[:, 0:3]
    vectors = data[:, 3:6]
    rootN   = data[:, 6]
    segmN   = data[:, 7]
    rootMax = rootN.max()+1
    print(rootMax)

    imPointsOrig = []
    imPointsOrigVec = numpy.array((1,0,0))
    z = 0
    for y in range(-imSize,imSize+1):
        for x in range(-imSize,imSize+1):
            imPointsOrig.append((z,y,x))
    imPointsOrig = numpy.array(imPointsOrig)

    # compute mask -- square imPointsOrig to have x**2 and y**2, then sum and sqrt
    circ = (numpy.sqrt(numpy.sum(numpy.square(imPointsOrig), axis=1)) <= imSize)
    #for r in range(1,rootMax):
    for r in range(1,2):
        print "root:"
        print r
        root = r

        rootRows = numpy.where(rootN==root)[0]

        ims = []

        for row in rootRows:
            point  = points[ row]
            vector = vectors[row]

        # Make the root orientation vector a unit vector
            vectorNormed = vector/numpy.linalg.norm(vector)

        # Compute angle between -Z (the normal to our plane of points called imPointsOrig)
            angleDeg = numpy.rad2deg(numpy.arccos(numpy.dot(imPointsOrigVec, vectorNormed)))    
        #print(angleDeg)

            if angleDeg < 0.1:
            # No rotation Necessary
                R = numpy.eye(3)

            else:
            # Compute cross product (this will be our rotation axis)
                rotationAxis = numpy.cross(imPointsOrigVec, vectorNormed)
            #print(rotationAxis)
        
            # Compute Rotation matrix R:
                R = spam.DIC.computePhi({'r':rotationAxis*angleDeg})[0:3,0:3]

            im = numpy.zeros(((2*imSize+1)*(2*imSize+1)), dtype='<u2')

            if interpolationOrder == 0:
            # Now deform the imPointsOrig with rotation matrix, and also add "point"
                for n, p in enumerate(imPointsOrig):
                # Very bad nearest neighbour interpolation
                    pDefRounded = tuple(numpy.round(numpy.dot(R, p) + point).astype(numpy.uint))
                
                #print pDefRounded
                    if circ[n]: # Add "and" condition on point being outside the shape of greys
                        im[n] = greys[pDefRounded]

            elif interpolationOrder == 1:
            # In this case we'll use a one-shot function (map coordintes) to lookup all the coordinates in one go
            # First create a mask array for which points we're looking up
                pointsLookup = numpy.zeros((2*imSize+1)*(2*imSize+1), dtype='bool')
            
            #  For each point, check whether it is in the circular mask, and within the image, add it to list of points to lookup
                imPointsDef = []
                for n, p in enumerate(imPointsOrig):
                    if circ[n]:
                        pointDef = numpy.dot(R, p) + point
                    
                        if pointDef[0] > 0 and pointDef[0] < greys.shape[0] and\
                        pointDef[1] > 0 and pointDef[1] < greys.shape[1] and\
                        pointDef[2] > 0 and pointDef[2] < greys.shape[2]:
                            # In this case we're both in the circular mask and in the image...
                            pointsLookup[n] = True
                            imPointsDef.append(pointDef)
                imPointsDef = numpy.array(imPointsDef)

            # Better interpolation
                im[pointsLookup] = scipy.ndimage.interpolation.map_coordinates(greys, imPointsDef.T, order=1)
        
            im = im.reshape((2*imSize+1, 2*imSize+1))
            ims.append(im)
        # print ims

        #plt.imshow(im)
        #plt.show()

        tifffile.imsave("H07-0{}-FinalRoot4-trin.tif".format(i,r), numpy.array(ims))
        
