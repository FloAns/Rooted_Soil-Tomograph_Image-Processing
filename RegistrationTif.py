import tifffile
import sys
import numpy
import spam.DIC.correlate
import spam.helpers
import spam.DIC.deformationFunction

im0 = sys.argv[1]
im1 = sys.argv[2]
print "reading images"
imref = tifffile.imread(im0)
imdef = tifffile.imread(im1)
im0r = im0[1200:,:,:]
print im0r.shape
im1r = im1[1200:,:,:]
print im1r.shape
print "computing initial Phi"
transformation01 = {'t':[0,0,0], 'r':[3,0,0]}
F01 = spam.DIC.computePhi(transformation01)
reg01=spam.DIC.correlate.lucasKanade(im0r, im1r, deltaPhiMin=0.00001, margin=50, maxIterations=100, PhiInit= F01, verbose=True)
spam.helpers.writeRegistrationTSV("/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/registration-tsv/H11_Registration00-02.tsv",(1400,325,325),reg01)
registratrion = spam.helpers.readCorrelationTSV("/mnt/tomo2/SCAN/GEO/Floriana/RESULTS_c/registration-tsv/H11_Registration00-02.tsv")
regF = registratrion['PhiField'][0]
regCentre = registratrion['fieldCoords'][0]

regFcomponents= spam.deformation.decomposePhi(regF.copy())
regFrigid = spam.deformation.computePhi({'t':regFcomponents['t'], 'r': regFcomponents['r']})
Finv = numpy.linalg.inv(regFrigid)
imDef = spam.DIC.applyPhi(im1,Finv,regCentre)
tifffile.imsave("/mnt/tomo2/SCAN/GEO/Floriana//RESULTS_c/gv_images/Registered/H11-02-Registered.tif", imDef.astype('<u2'))
