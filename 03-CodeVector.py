"""
2019-08-29 FA
After walking through root, build a vector representation of root
"""

vecStep = 1

import numpy
import spam.helpers
import sys

inp = numpy.load(sys.argv[1], allow_pickle=True, encoding='bytes')

nRoots = inp[-1,2]

points = []
vectors = []
rootN = []
segmentN = []

for root in range(1,nRoots+1):
    rootRows = numpy.where(inp[:,2] == root)
    nSegments = inp[rootRows][-1, 1]
    for segment in range(1,nSegments+1):
        segmentRows = numpy.where(inp[rootRows][:,1] == segment)[0]

        # Generate approximate vecStep skip
        rowsForVector = numpy.linspace(segmentRows[0], segmentRows[-1], (len(segmentRows))/vecStep).astype(numpy.int)

        # If step > len(segment )
        if len(rowsForVector) >= 2:
            startRows = rowsForVector[0:-1]
            stopRows  = rowsForVector[1:]
        else:
            startRows = [segmentRows[ 0]]
            stopRows  = [segmentRows[-1]]

        # loop through pairs of rows:
        for startRow, stopRow in zip(startRows, stopRows):
            points.append(  numpy.array(inp[rootRows][startRow,0]))
            vectors.append( numpy.array(inp[rootRows][stopRow,0])-numpy.array(inp[rootRows][startRow,0]))
            rootN.append(   root)
            segmentN.append(segment)

spam.helpers.writeGlyphsVTK(numpy.array(points), pointData={'vectors':numpy.array(vectors),
                                                            'root':   numpy.array(rootN),
                                                            'segment':numpy.array(segmentN)}, fileName=sys.argv[1][0:-4]+".vtk")

numpy.save(sys.argv[1][0:-4]+"-vectors.npy", numpy.array([numpy.array(points)[:,0],
                   numpy.array(points)[:,1],
                   numpy.array(points)[:,2],
                   numpy.array(vectors)[:,0],
                   numpy.array(vectors)[:,1],
                   numpy.array(vectors)[:,2],
                   numpy.array(rootN),
                   numpy.array(segmentN)]).T)
