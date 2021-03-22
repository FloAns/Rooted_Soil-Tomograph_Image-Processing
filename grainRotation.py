## this is the code to extract the rotation component of each grain and then plot it in 2D or eventually save it as vtk an dhave the oveall rotation.##

import tifffile
import numpy
import spam.label as ltk
import spam.DIC.deformationFunction as defor
import matplotlib.pyplot as plt
from math import sqrt
for k in range(1,8):
    labelled = tifffile.imread("/media/fanselmucci/My Passport/RESULTS_c/grains/H05/Label/H5-0W-Bin2-BF-Labels.tif")
    DVC = numpy.genfromtxt("/media/fanselmucci/My Passport/RESULTS_c/ddic/H05/global/tsv/H5-0W-Bin2-H5-0{}-Bin2-Registered-discreteDVC.tsv".format(k),delimiter='\t',names=True)
    mx = int(labelled.max())
    rotation = numpy.zeros((int(labelled.max()),5))
    for i in range(0,mx):                                      
        print (i)                                                            
        Phi = numpy.array([[DVC['F11'][i],DVC['F12'][i],DVC['F13'][i],DVC['Zdisp'][i]],[DVC['F21'][i],DVC['F22'][i],DVC['F23'][i],DVC['Ydisp'][i]],[DVC['F31'][i],DVC['F32'][i],DVC['F33'][i],DVC['Xdisp'][i]],[0,0,0,1]])                                                      
        print (Phi )                                                       
        dec = defor.decomposePhi(Phi)    
        print (dec['r'] )                                               
        rotation[i][0]=i
        rotation[i][1]=dec['r'][0]                      
        rotation[i][2]=dec['r'][1]                        
        rotation[i][3]=dec['r'][2]            
        rotation[i][4]=sqrt((dec['r'][0]**2)+(dec['r'][1]**2)+(dec['r'][2]**2))
    TSVheader = "Label\tZrot\tYrot\tXrot\tOrderMagnitude"  
    outMatrix= numpy.array([numpy.array(range(mx)),rotation[0],rotation[1],rotation[2],rotation[3],rotation[4]]).T  
    #numpy.savetxt("/mnt/tomo2/SCAN/GEO/Floriana/Organized/2018-06/H4-MaizeinHN1.5-2Loose/DIC-GlobalDisplacementField/H4-00-06-Rotation.tsv",outMatrix,fmt='%.7f',delimiter='\t',newline='\n',comments='',header=TSVheader)  
    labelled1=labelled.astype(float)
    labelrot = ltk.label.convertLabelToFloat(labelled,rotation[:,4])
    labelrot[labelled1==0]=numpy.nan
    #plt.imshow(labelrot[:,:,500],cmap="plasma", vmin=0, vmax=60);plt.colorbar();plt.show()
    tifffile.imsave('/media/fanselmucci/My Passport/RESULTS_c/ddic/H05/global/H5-0{}-rotation.tif'.format(k),labelrot)
