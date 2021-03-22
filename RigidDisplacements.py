import tifffile
import numpy
import spam.helpers
import spam.DIC.transformationOperator
import spam.label.toolkit as ltk

im1 = tifffile.imread("/home/fanselmucci/Desktop/DIC8bin/bin8/Labelsfrombin8ofLabels.tif")

numberOfLabels = (im1.max() + 1).astype('u4')
print("Number of labels = {}\n".format(numberOfLabels))
print("Calculating Bounding Boxes and Centres of Mass of all labels.")
boundingBoxes = ltk.boundingBoxes(im1)
centresOfMass = ltk.centresOfMass(im1, boundingBoxes=boundingBoxes)
print("\n  ")

Ffield = numpy.zeros((centresOfMass.shape[0], 4, 4))
for node in range(centresOfMass.shape[0]):
            Ffield[node] = numpy.eye(4)
 
rigidDisp = numpy.zeros((centresOfMass.shape[0], 3))
reg = spam.helpers.readTSV("/home/fanselmucci/Desktop/DIC8bin/bin8/Fbin8-00-01.tsv")
if reg['fieldCoords'].shape[0] == 1:
               regF = reg['Ffield'][0]
               regCentre = reg['fieldCoords'][0]
               registrationSuccessful = True
               print("\tI read a registration from a file in binning 8 at centre {} at this scale".format( regCentre) )
  
for node in range(centresOfMass.shape[0]):
                Ffield[node] = regF.copy()
                Ffield[node][0:3, -1] = spam.DIC.transformationOperator.FtoTransformation(regF.copy(), Fcentre=regCentre, Fpoint=centresOfMass[node])["t"]

regFComponents = spam.DIC.transformationOperator.FtoTransformation(regF.copy())

regFrigid = spam.DIC.transformationOperator.computeTransformationOperator( {'t': regFComponents['t'],'r': regFComponents['r']} )

for node in range(centresOfMass.shape[0]):
                   rigidDisp[node] = spam.DIC.transformationOperator.FtoTransformation(regFrigid.copy(), Fcentre=regCentre, Fpoint=centresOfMass[node])["t"]     
for node in range(centresOfMass.shape[0]):
                Ffield[node][0:3,-1] -= rigidDisp[node]


TSVheader = "Label\tZpos\tYpos\tXpost\tZdisp\tYdisp\tXdisp\tF11\tF12\tF13\tF21\tF22\tF23\tF31\tF32\tF33"
outMatrix = numpy.array([numpy.array(range(centresOfMass.shape[0])),centresOfMass[:,0],centresOfMass[:,1], centresOfMass[:,2],Ffield[:,0,3],Ffield[:,1,3], Ffield[:,2,3],Ffield[:,0,0], Ffield[:,0,1],Ffield[:,0,2], Ffield[:,1,0], Ffield[:,1,1], Ffield[:,1,2], Ffield[:,2,0], Ffield[:,2,1], Ffield[:,2,2]]).T

numpy.savetxt("rigidbodydisp00-01.tsv",outMatrix, fmt='%.7f', delimiter='\t',newline='\n', comments='', header=TSVheader)
