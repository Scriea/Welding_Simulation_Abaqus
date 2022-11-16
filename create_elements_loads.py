# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
# Tolerance
Tol= 0.0001
#T = Welding Time in sec
T=50.0
# N_elements is the number of elements along the x axe (must be the same number in mesh)
N_elements= 50
# L is the length of the plate ; V is the Voltage ; I is the Current ; etta is the source heat efficiency
L=0.1
V=15
I=50
etta=0.75
# a, b, cf are the the dimensions of the double elipse check Goldak's paper
a=0.002
b=0.001
cf=0.002
# f const
f=0.6
V1=L/T
inc=0.0
inc=T/N_elements
V2= 0.0
V2= L/N_elements
Q=etta*V*I
C=(6*1.7320*f*Q)/(a*b*cf*3.1415*1.7724)
# create sets (groupes of elements) 
for i in range (1,N_elements+1):	
	mdb.models['Model-1'].rootAssembly.Set(elements=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].elements.getByBoundingBox(
	-Tol+V2*(i-1),-(a+Tol),-(b+Tol),(V2*i)+Tol,a+Tol,0.0+Tol), name='Set-'+str(i))
	
# create amplitudes
mdb.models['Model-1'].TabularAmplitude(data=((0.0, 1.0), (inc, 1.0), (inc+0.001, 
    0.0), (T, 0.0)), name='Amp-1', smooth=SOLVER_DEFAULT, timeSpan=STEP)
	
mdb.models['Model-1'].TabularAmplitude(data=((0.0, 0.0), (T-inc-0.001, 0.0), (T-inc, 
    1.0), (T, 1.0)), name='Amp-'+str(N_elements), smooth=SOLVER_DEFAULT, timeSpan=STEP)
	
for i in range (1,N_elements-1):
	mdb.models['Model-1'].TabularAmplitude(data=((0.0, 0.0), (i*inc-0.001, 0.0), (i*inc, 
    1.0), (i*inc+inc, 1.0), (i*inc+inc+0.001, 0.0), (T, 0.0)), name='Amp-'+str(i+1), smooth=
	SOLVER_DEFAULT, timeSpan=STEP)
	
# create body heat	
for i in range (1,N_elements+1):	
	mdb.models['Model-1'].BodyHeatFlux(createStepName='Step-1', magnitude=C
	, name='Load-'+str(i), region=Region(
	elements=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].elements.getByBoundingBox(
	-Tol+V2*(i-1),-(a+Tol),-(b+Tol),(V2*i)+Tol,a+Tol,0.0+Tol)), amplitude='Amp-'+str(i))
	
for i in range (1,N_elements+1):	
	mdb.models['Model-1'].loads['Load-'+str(i)].deactivate('Step-2')	
