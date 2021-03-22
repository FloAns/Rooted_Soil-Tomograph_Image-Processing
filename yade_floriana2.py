from yade import pack, plot,export
import numpy as np
#yade.qt.View(), yade.qt.Controller()

###############################################
####       simulation parameters           ####
###############################################

key='test' # put your simulation's name here

########## for the soil ##########
normalStiffnessS=5.0e8
stiffnessRatioS=0.3
compFricDegreeS=19
adhesionS=20000
rollingStiffnessRatioS=5
rollingfrictionS=0.55

########## for the root ##########
normalStiffnessR=5.0e8
stiffnessRatioR=0.3
compFricDegreeR=19
adhesionR=0
rollingStiffnessRatioR=5
rollingfrictionR=0.55

########## number of spheres for the sand sample ##########
num_spheres = 10000 


########## size of the simulation domain ##########

prismH = 0.01 ## height of the prismatic domain
prismL = 0.02 ## length of the prismatic domain
rootR = 0.0005 ## root radius
rootL = 0.02 ## root length

########## numerical parameters ##########
damp=0.05 # damping coefficient
stabilityThreshold=0.001 # we test unbalancedForce against this value in different loops (see below)
confiningPressure = 50000
growRate = 0.001 # growing factor of the soil particles for compaction of the sample

###############################################
####       CREATE MATERIAL parameters      ####
###############################################
####   CREATE MATERIAL FOR SOIL   ###
O.materials.append(CohFrictMat(
	young=normalStiffnessS,
	poisson=stiffnessRatioS,
	frictionAngle=radians(compFricDegreeS),
	isCohesive=True,
	normalCohesion=adhesionS,
	shearCohesion=adhesionS,
	alphaKr=rollingStiffnessRatioS,
	alphaKtw=0,
	etaRoll=rollingfrictionS,
	etaTwist=0,
	momentRotationLaw=True,
	density=3000,
	label='soil',
	fragile=False,
)) 
####   CREATE MATERIAL FOR ROOT   ###
O.materials.append(CohFrictMat(
	young=normalStiffnessR,
	poisson=stiffnessRatioR,
	frictionAngle=radians(compFricDegreeR),
	isCohesive=True,
	normalCohesion=adhesionR,
	shearCohesion=adhesionR,
	alphaKr=rollingStiffnessRatioR,
	alphaKtw=0,
	etaRoll=rollingfrictionR,
	etaTwist=0,
	momentRotationLaw=True,
	density=3000,
	label='root',
	fragile=False,
)) 
####   CREATE MATERIAL FOR WALLS   ###
O.materials.append(CohFrictMat(
	young=normalStiffnessS,
	poisson=stiffnessRatioS,
	frictionAngle=0,
	isCohesive=True,
	normalCohesion=0,
	shearCohesion=0,
	alphaKr=0,
	alphaKtw=0,
	etaRoll=0,
	etaTwist=0,
	momentRotationLaw=True,
	density=3000,
	label='walls',
	fragile=False,
))


#### Walls (made with boxes) surrounding the numerical sample ####
##            
## ^ y        |
## |        bx|
## |--> x     |
##            |_______
##               by

#by=box(center=[prismH/2,0,0],extents=[1.05*prismH/2,0,1.05*prismL/2],color=[1,0,0],wire=True,fixed=True,material='walls')
#bx=box(center=[0,prismH/2,0],extents=[0,1.05*prismH/2,1.05*prismL/2],color=[1,0,0],wire=True,fixed=True,material='walls')
by=box(center=[prismH/2,0,0],extents=[prismH/2,0,prismL/2],color=[1,0,0],wire=True,fixed=True,material='walls')
bx=box(center=[0,prismH/2,0],extents=[0,prismH/2,prismL/2],color=[1,0,0],wire=True,fixed=True,material='walls')

#bxy=box(center=[prismH/2,prismH/2,0],extents=[0,1.05*prismH*(2**0.5)/2,1.05*prismL/2],color=[1,0,0],wire=True,fixed=True,material='walls')
bxy=box(center=[prismH/2,prismH/2,0],extents=[0,prismH*(2**0.5)/2,prismL/2],color=[1,0,0],wire=True,fixed=True,material='walls')
bxy.state.ori=((0,0,1),pi/4)

#bzmax=box(center=[prismH/2,prismH/2,prismL/2],extents=[1.05*prismH/2,1.05*prismH/2,0],color=[1,0,0],wire=True,fixed=True,material='walls')
#bzmin=box(center=[prismH/2,prismH/2,-prismL/2],extents=[1.05*prismH/2,1.05*prismH/2,0],color=[1,0,0],wire=True,fixed=True,material='walls')
bzmax=box(center=[prismH/2,prismH/2,prismL/2],extents=[prismH/2,prismH/2,0],color=[1,0,0],wire=True,fixed=True,material='walls')
bzmin=box(center=[prismH/2,prismH/2,-prismL/2],extents=[prismH/2,prismH/2,0],color=[1,0,0],wire=True,fixed=True,material='walls')

wallIds=O.bodies.append([bx,by,bxy,bzmin,bzmax])


#### the root made of a clump of spheres ####
start = prismL/2+rootR
stop = start + rootL
num = ceil(rootL/rootR*20)
print "Number of spheres composing the root: ", num
centers = np.linspace(start, stop, num)  
#root is a vector contaning the centers of the spheres composing the roots 
root=[]
for c in centers:
    root=root+O.bodies.append([sphere((0,0,c),rootR,color=(0.5,0.5,0.5),material='root')]) 
	
ClumpR=O.bodies.clump(root)    ## creatoin of the clump for the root
O.bodies[ClumpR].state.blockedDOFs="xyzXYZ"            ## the root is initially blocked

for b in O.bodies:
  if b.isClumpMember:
    b.dynamic=False
	
###########################################
###  GENERATE A LOOSE PACKING OF GRAINS ###
###########################################
mn,mx=Vector3(0,0,-prismL/2),Vector3(prismH,prismH,prismL/2) # corners of the initial packing

sp0=pack.SpherePack()
#sp0.fromSimulation() ???
sp0.makeCloud(mn,mx,psdSizes=[0.125,0.160,0.2,0.25,0.315,0.4,0.5,0.63], psdCumm=[0,0.0325,0.0725,0.1875,0.365,0.605,0.85,1.0],distributeMass=True, num=num_spheres, porosity=0.7,seed=1) #granulo Hostun RF
#sp0.toSimulation(material='soil')


#### Remove the grains outside the prismatic sample 

soil=[] ## creation of an empty list of soil

for x,rad in sp0:
	yLimit = prismH - x[0] 
	if (x[1]+rad)<yLimit:
		soil.append(O.bodies.append(sphere(x,rad,material='soil')))
		
print "Number of soil grains: ", len(soil)

###########################################
###  Function to compute stresses       ###
###########################################		   
def stress():
	Fx = O.forces.f(bx.id)[0]
	Sbx = O.bodies[bx.id].shape.extents[1] * O.bodies[bx.id].shape.extents[2] * 4 ## FIXME: extent of the wall is 5 percent too large!
	sigmaX = Fx/Sbx
	
	Fy = O.forces.f(by.id)[1]
	Sby = O.bodies[by.id].shape.extents[0] * O.bodies[by.id].shape.extents[2] * 4 ## FIXME: idem
	sigmaY = Fy/Sby
	
	Fzmin = O.forces.f(bzmin.id)[2]
	Sbzmin = O.bodies[bzmin.id].shape.extents[0] * O.bodies[bzmin.id].shape.extents[1] * 2 ## FIXME: idem  ## times 2 only because only half of the square wall is used to define the prism
	sigmaZ = Fzmin/Sbzmin
	
	meanP = (sigmaX + sigmaY + sigmaZ)/3.0
	
	print "sigmaX: ", sigmaX 
	print "sigmaY: ", sigmaY 
	print "sigmaZ: ", sigmaZ
	print "meanP: ", meanP 
	
	#a=getStress(volume=prismH*prismH*prismL/2.0)  # another way to obtain the full stress tensor with a Yade function
	#print "getStress: ", a 
	
	return meanP


###########################################
###  Function to grow the particles     ###
###########################################
def growP(growFactor):
      #growFactor=1.005
      #for b in range(ClumpR+1, ClumpR+1+len(soil)):  # Be carefull 'growparticle' grow a single particle and do not update at all the contact properties
		#growParticle(b,1.005)
      growParticles(growFactor)  # 'growparticles' with a 's' grow all the dynamic particles (by default) at the same time but update only kn and ks, the other contacts properties are not updated!
      growFactor3=growFactor**3
      growFactor2=growFactor**2
      for i in O.interactions:
	  #i.phys.kn*=growFactor # useless when growparticleS is used
	  #i.phys.ks*=growFactor # useless when growparticleS is used
	  i.phys.kr*=growFactor3
	  i.phys.maxRollPl*=growFactor
	  i.phys.normalAdhesion*=growFactor2
	  i.phys.shearAdhesion*=growFactor2

###########################################
###  Function to compact the sample     ###
###  under a prescribed confining       ###
###   pressure by growing particles     ###
###########################################	  
def compaction():
  p = -stress()
  print "mean stress", p
  if p>confiningPressure*0.8:
     tempGrowRate=growRate/20.0
  else:
     tempGrowRate=growRate
  growP(1.0+(tempGrowRate*((confiningPressure-p)/(confiningPressure))))
  #growP(1.0+(growRate*((confiningPressure-p)/(confiningPressure))))
  #growP(1.0005)
  unb=unbalancedForce()
  print "unbalanced Force", unb
  if unb<stabilityThreshold and abs(confiningPressure-p)/confiningPressure<0.01:
      print "compaction finished"
      O.pause()

###########################################
###  Function to add data to a list     ###
###  to plot them and save them         ###
###########################################	
def addPlotData():
   plot.addData(unbalanced=utils.unbalancedForce(),i=O.iter,
      p=-stress(),
      #z=avgNumInteractions(),
      #zm=avgNumInteractions(skipFree=True),
      #Ek=utils.kineticEnergy(),
      #Etot=O.energy.total(),**O.energy
   )      
def saveData():
  plot.saveDataTxt('root_' + key + '.txt')
  plot.saveGnuplot('root_' + key)
		
#####################################
#### DEFINE of SIMULATION ENGINES ###
#####################################

O.engines=[
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom6D(),Ig2_Box_Sphere_ScGeom6D()],
		[Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(setCohesionOnNewContacts=True, setCohesionNow= False,label='Ip2')],
		[Law2_ScGeom6D_CohFrictPhys_CohesionMoment(always_use_moment_law=True,useIncrementalForm=True)],label="iloop"
	),
	GlobalStiffnessTimeStepper(active=1,timeStepUpdateInterval=1000,timestepSafetyCoefficient=0.8),
	NewtonIntegrator(label='newton',damping=damp),
	PyRunner(command='addPlotData()',iterPeriod=100),
	PyRunner(command='saveData()',iterPeriod=10000),
	PyRunner(command='compaction()',iterPeriod=100,label='compac'),  # Use this PyRunner only the grow particles in an interactive mode (i.e. via the graphical interface
	#PyRunner(command='growP()',iterPeriod=100),
	#PyRunner(command='stress()',iterPeriod=500)
]

O.run(1,True)

#####################################################
#### to define what to plot if simulation is run  ###
#### via the graphical interface                  ###
#####################################################
#### define what to plot  ###
#plot.plots={'i':('unbalanced',None,'p'),'i ':('sxx','syy','szz'),'i  ':('unbalanced',None,'n'), 'ezz':('q',None,'ev')}
plot.plots={'i':('unbalanced',None,'p')}
   
### show the plot ###
plot.plot()

####################################################################
#### loop to compact the sample without the graphical interface ####
#### (i.e. without the interactive mode                          ###
####################################################################
#while 1:
 # p = -stress()
  #print "mean stress", p
  #if p>confiningPressure*0.8:
   #  tempGrowRate=growRate/20.0
  #else:
   #  tempGrowRate=growRate
  #growP(1.0+(tempGrowRate*((confiningPressure-p)/(confiningPressure))))
  #growP(1.0+(growRate*((confiningPressure-p)/(confiningPressure))))
  #growP(1.0005)
  #O.run(100,True)
  #unb=unbalancedForce()
  #print "unbalanced Force", unb
  #if unb<stabilityThreshold and abs(confiningPressure-p)/confiningPressure<0.01:
   #   print "compaction finished"
    #  break

	
