# From the displacement matrix in input, the code will give in output the matrix with the Rigid body mption components
import tifffile
import numpy
import spam.DIC.correlate
import spam.helpers
import spam.DIC.deformationFunction
im1 = tifffile.imread("/home/3S-LAB/fanselmucci/Desktop/M2-01-Bin2.tif")
im2 = tifffile.imread("/home/3S-LAB/fanselmucci/Desktop/M2-04-Bin2.tif")
#let's crop the image to see only ther bottom, which should not be that affected by the root
im1c =im1[1600:,200:700,200:700]
#print im1c
im2c =im2[1600:,200:700,200:700]
#print im2c
##let's measure an initial tranformation matrix, according to what we measured on FIji
InTrans = {'t':[2,0,0],'r':[3,0,0]}
#Phi = spam.DIC.deformationFunction.computePhi(InTrans)
Phi=numpy.array([[1.005,0.002,-0.006,0.723],[0.,0.966, -0.26, 65.458],[0.003, 0.259, 0.966, -51.],[0.,0.,0.,1.]])
##let's compute the registration
reg1_2=spam.DIC.correlate.lucasKanade(im1c,im2c,margin=50,maxIterations=100,PhiInit=Phi,verbose=True,deltaPhiMin=0.00001, imShowProgress=True)
##from this registration now we should only apply the rigid transformation to the image
spam.helpers.writeRegistrationTSV("/home/3S-LAB/fanselmucci/Desktop/M2-01-05registration2.tsv",(1800,450,450),reg1_2)
registration1_2= spam.helpers.readTSV("/home/3S-LAB/fanselmucci/Desktop/M2-01-05registration2.tsv")
regF1_2=registration1_2['PhiField'][0]
regCentre1_2=registration1_2['fieldCoords'][0]
regFcomponents1_2=spam.DIC.deformationFunction.decomposePhi(regF1_2.copy())
regFrigid1_2=spam.DIC.deformationFunction.computePhi({'t':regFcomponents1_2['t'],'r':regFcomponents1_2['r']})
Finv1_2= numpy.linalg.inv(regFrigid1_2)
imDef2=spam.DIC.deformationFunction.applyPhi(im=im2,Phi=Finv1_2,PhiPoint=regCentre1_2)
tifffile.imsave("/home/3S-LAB/fanselmucci/Desktop/M2-05-RigidReg2.tif",imDef2.astype('<u2'))
