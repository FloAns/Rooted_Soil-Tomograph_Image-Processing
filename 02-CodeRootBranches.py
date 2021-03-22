"""
2019-08-29 Edward Ando and Floriana Anselmucci
This programme has 2 main objectives: to label root segments and to
output a vectorised version of the roots for analysis.

Input:
List of starting points
Binarised 3D image of root skeleton (0 is background)

Output:
Ordered list of segments with root number and segment number
"""
import numpy
import tifffile
import sys
import Queue as queue
import time
import sys

q = queue.Queue()


if len(sys.argv) == 2:
    fileNameSkel = sys.argv[-1]
    skel = tifffile.imread(fileNameSkel)
    #print(skel.shape)
    skelN = numpy.zeros_like(skel)
    for point in numpy.array(numpy.where(skel==255)).T:
        nNeighbours = numpy.sum(skel[point[0]-1:point[0]+2,
                                     point[1]-1:point[1]+2,
                                     point[2]-1:point[2]+2] == 255)-1
        skelN[point[0], point[1], point[2]] = nNeighbours
else:
    print("Please run me like this: python rootWalker2.py skel.tif")
    exit()

# These points are attached to the seed and have only one 
#   neighbour in the skeleton
# This is defined in ZYX (i.e., numpy array order)
#starting points for 
####################################################### -- DATA -- ############################################################################################
## 
#H10-00[(340,298,324)], 
#H10-01[(349,299,335)], 
#H10-02[(367,308,329),(359,318,347),(262,273,344),(293,268,351)], 
#H10-03[(368, 309, 328),(363, 321, 347),(281,261,368),(322,261,366),(268,244,320),(265,248,350)], 
#H10-04[(377,312,323),(377,327,345),(263,267,354),(299,263,350),(288,241,318),(257,254,348),(189,241,322)], 
#H10-05[(373,313,323),(373,327,346),(264,268,354),(300,264,352),(290,240,313),(265,248,350),(189,241,322),(185,286,298),(197,293,360)] 
#h10-06[(346,285,346),(349,313,347),(261,269,355),(300,264,352),(290,240,313),(265,248,350),(189,241,322),(185,286,298),(196,293,358),(187,261,360),(188,263,285)]
#h10-07[(346,285,346),(349,313,347),(261,269,355),(300,264,352),(289,243,314),(267,244,355),(189,241,322),(185,286,300),(195,293,358),(187,261,360),(187,263,288)]
##
#############################################################################################################################################################
startingPoints = [(373,313,323),(373,327,346),(266,267,355),(300,264,352),(290,240,313),(265,248,350),(189,241,322),(185,286,298),(197,293,360)]

def neigh(p, im, imN=None):
    """
    This function returns a list of non-zero neighbour points
    in a 3x3x3 cube in "im" around point "p"
    """
    tmp = im[   p[0]-1:p[0]+2,
                p[1]-1:p[1]+2,
                p[2]-1:p[2]+2].copy()
    tmp[1,1,1] = 0
    points = []
    neighbours = numpy.array(numpy.where(tmp == 255)).T
    for neighbour in neighbours:
        points.append((neighbour[0]+p[0]-1,
                       neighbour[1]+p[1]-1,
                       neighbour[2]+p[2]-1))
    if imN is None:
        return points
    else:
        # flag a higher-connectivity point nearby
        v = imN[p]
        imNsub = imN[p[0]-1:p[0]+2,
                   p[1]-1:p[1]+2,
                   p[2]-1:p[2]+2]
        vMax = imNsub.max()
        if vMax > v and v > 2:
            flag = tuple(numpy.array(numpy.where(imNsub == vMax)).T[0] + numpy.array(p) - numpy.array((1,1,1)))
            #print("!!! Flag = ", flag)
        else:
            flag = None

        return [points, flag]

root = 1
segment = 1
output = []
#out = numpy.zeros_like(skel)

for startingPoint in startingPoints:
    # 1. check that this is indeed a starting Point (i.e., only 1 neighbour)
    p = tuple(startingPoint)
    neighbours = neigh(p, skel)
    if len(neighbours) != 1:
        print("This is not a starting point, it has {} neighbours".format(len(neighbours)))
        print(p)
        print(neighbours)
        exit()

    while True:
        #time.sleep(0.1)
        #print("p = {}".format(p))
        # sanity check -- current pixel should not be empty
        if skel[p] == 0:
            # If current pixel is already zero, this is a problem!!!
            print("noooooooo")
        else:
            # mark current point as done
            skel[p] = 0
            output.append((p,segment,root))
            #out[p] = segment

        # Where to go next?
        neighbours, flag = neigh(p, skel, skelN)
        #print(neighbours)

        # different conditions for number of neighbours
        if len(neighbours) == 0:
            #print("End point! Check Queue if there are other segments to check")
            newRoot = False

            # Try to find a valid new p.
            while True:
                # If no more candidates, move to next root
                if q.empty():
                    root += 1
                    segment = 1
                    newRoot = True
                    break
                pnext = q.get()

                # Necessary check for loops in skeleton
                if skel[pnext] != 0:
                    p = pnext
                    segment += 1
                    break

            # break out of while and do next root on outside while
            if newRoot: break

        elif len(neighbours) == 1:
            #print("Simple connector, keep walking")
            p = neighbours[0]

        elif flag is not None:
            #print("Flagged value, going there")
            p = flag
            # HACK: set all neighbours to current segment
            for e in neighbours:
                skel[e] = 0
                output.append((e,segment,root))
                #out[e] = segment

        elif len(neighbours) > 1:
            #print("junction, go down one, and add the rest to queue")
            for e in neighbours[1:]:
                q.put(tuple(e))
                skel[tuple(e)] = 128
            segment += 1
            p = neighbours[0]

numpy.save(sys.argv[1]+"-output.npy", output)
#tifffile.imsave("out.tif", out)
