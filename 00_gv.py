import tifffile
import numpy
import matplotlib.pyplot as plt
filename = "/home/3S-LAB/fanselmucci/Desktop/H10-03-CorrectedGVRegBin2-RIGID.tif"
sample0 = tifffile.imread(filename)
z = sample0.shape[0]  
DesideredMedian_sample = numpy.median(sample0)
sample_median = []                                               
for i in numpy.arange(z):                                        
    sample_median.append(numpy.median(sample0[i]))   
sample_median = numpy.asarray(sample_median).astype('<f4')
difference_median_sample = DesideredMedian_sample - sample_median
sample_correct0 = numpy.zeros_like(sample0).astype('<f4')
for i in numpy.arange(z):
    sample_correct0[i] = sample0[i] + difference_median_sample[i]
sample_correct_median = []
sample_correct_mean = []
mask_container = tifffile.imread("/home/3S-LAB/fanselmucci/Desktop/H10-mask.tif")
sample_correct = sample_correct0.copy().astype('<f4') * mask_container.copy().astype('<f4')
plt.imshow(sample_correct[:,300,:]);plt.show()
for i in numpy.arange(z):
    sample_correct_median.append(numpy.median(sample_correct[i]))
    sample_correct_mean.append(numpy.mean(sample_correct[i]))
plt.plot(sample_correct_mean);plt.plot(sample_correct_median);plt.show()
Peaks = numpy.zeros_like(sample_correct).astype('<f4')
for i in numpy.arange(sample_correct.shape[0]):
    hist = numpy.histogram(sample_correct[i], bins = 65535, range = [0,65535])
    freq = hist[0]
    PP = float((numpy.where(freq[15000:25000] == freq[15000:25000].max()))[0][0])
    PP = PP + 10000.0
    GP = float((numpy.where(freq[35000:50000] == freq[35000:50000].max()))[0][0])
    GP = GP + 40000.0
    Peaks[i] = sample_correct[i].copy().astype('<f4') - float(PP)
    Peaks[i] = Peaks[i].copy().astype('<f4')/ (float(2.0*(float(GP-PP))))
    Peaks[i] = Peaks[i].copy().astype('<f4') + 0.25
    print i
plt.imshow(Peaks[:,300,:]); plt.show()

Peak2 = numpy.zeros_like(sample0).astype('<f4')
Peak2 = (Peaks.astype('<f4') + abs(Peaks.min()))
Peak2 = Peak2.astype('<f4') / abs(Peak2.max())
Peak3 = Peak2 * 65535.0
Peak_target_mean = numpy.mean(Peak3)
Peak_target_stdv = numpy.std(Peak3)
Peak_mean = []
Peak_stdv = []
Peak_stdR = []
for i in numpy.arange(z):
    Peak_mean.append(numpy.mean(Peak3[i]))
    Peak_stdv.append(numpy.std(Peak3[i]))
Peak_mean = numpy.asarray(Peak_mean).astype('<f4')
Peak_stdv = numpy.asarray(Peak_stdv).astype('<f4')
for i in numpy.arange(z):
    Peak_stdR.append(float(Peak_target_stdv/Peak_stdv[i]))
Peak_stdR = numpy.asarray(Peak_stdR).astype('<f4')
Peak_correct = numpy.zeros_like(Peak3).astype('<f4')
for i in numpy.arange(z):
    Peak_correct[i] = Peak_target_mean + (Peak3[i] - Peak_mean[i])*Peak_stdR[i]
plt.imshow(Peak_correct[:,200,:]);plt.show()
grain_threshold = 0.6 * 65535.0
mask_grains = Peak_correct < grain_threshold
grains = numpy.ma.array(Peak_correct, mask = mask_grains)
plt.imshow(grains[:,200,:]); plt.show()
tifffile.imsave(filename+'step1.tif', Peak_correct)

mean_grains = []
medi_grains = []

for i in numpy.arange(z):
    mean_grains.append(numpy.ma.mean(grains[i]))
    medi_grains.append(numpy.ma.median(grains[i]))
plt.plot(medi_grains);plt.show()
voids_threshold = 0.3 * 65535.0
mask_voids = Peak_correct > voids_threshold
voids = numpy.ma.array(Peak_correct, mask= mask_voids)
mean_voids = []
medi_voids = []
for i in numpy.arange(z):
    mean_voids.append(numpy.ma.mean(voids[i]))
    medi_voids.append(numpy.ma.median(voids[i]))
plt.plot(medi_voids);plt.plot(mean_voids);plt.show()
mask_water = numpy.zeros_like(mask_grains) 
mask_water[(Peak_correct >= voids_threshold) & (Peak_correct <= grain_threshold)]  = 1.0
water = numpy.ma.array(Peak_correct, mask = mask_water)
mean_water = []
medi_water = []
for i in numpy.arange(z):
    mean_water.append(numpy.ma.mean(water[i]))
    medi_water.append(numpy.ma.median(water[i]))
plt.plot(mean_water);plt.plot(medi_water);plt.show()
Desidered_median_grains = numpy.ma.median(grains[300:900,:,:])
medi_grains = numpy.asarray(medi_grains)
difference_median_grains = Desidered_median_grains - medi_grains
grains_correct = numpy.zeros_like(grains)
grains_correct = grains.copy()
for i in numpy.arange(z):
     grains_correct[i] = grains[i] +difference_median_grains[i]
medi_grains_correct = []
for i in numpy.arange(z):
    medi_grains_correct.append(numpy.ma.median(grains_correct[i]))
plt.plot(medi_grains_correct);plt.show()

Desidered_median_voids = numpy.ma.median(voids[300:900,:,:])
medi_voids = numpy.asarray(medi_voids)
difference_median_voids = Desidered_median_voids - medi_voids
voids_correct = numpy.zeros_like(voids)
voids_correct = voids.copy()
for i in numpy.arange(z):
     voids_correct[i] = voids[i] +difference_median_voids[i]
medi_voids_correct = []
for i in numpy.arange(z):
    medi_voids_correct.append(numpy.ma.median(voids_correct[i]))
plt.plot(medi_voids);plt.plot(medi_voids_correct);plt.show()

Desidered_median_water = numpy.ma.median(water[300:900,:,:])
medi_water = numpy.asarray(medi_water)
difference_median_water = Desidered_median_water - medi_water
water_correct = numpy.zeros_like(water)
water_correct = water.copy()
for i in numpy.arange(z):
    water_correct[i] = water[i] +difference_median_water[i]
medi_water_correct = []
for i in numpy.arange(z):
    medi_water_correct.append(numpy.ma.median(water_correct[i]))
plt.plot(medi_water_correct);plt.plot(medi_water);plt.show()
sample_new = numpy.zeros_like(sample0).astype('<f4')
for i in numpy.arange(z):
    sample_new[i] = grains_correct[i].astype('<f4') + voids_correct[i].astype('<f4')+ water_correct[i].astype('<f4')
plt.imshow(sample_new[:,400,:]);plt.show()
tifffile.imsave(filename +'correct.tif', sample_new)
gt = 0.6* 65535.0
mask = sample_new < gt
g = numpy.ma.array(sample_new, mask = mask)
gmean = []
gmedi = []
for i in numpy.arange(z):
    gmean.append(numpy.ma.mean(g[i]))
    gmedi.append(numpy.ma.median(g[i]))
    
mask2 = sample0 < gt
g2 = numpy.ma.array(sample0, mask = mask)
gmean2 = []
gmedi2 = []
for i in numpy.arange(z):
    gmean2.append(numpy.ma.mean(g2[i]))
    gmedi2.append(numpy.ma.median(g2[i]))
plt.plot(gmedi2);plt.plot(gmedi);plt.show()

