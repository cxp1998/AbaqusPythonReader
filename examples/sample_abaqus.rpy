# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2026 replay file
# Internal Version: 2026_01_15
# Run by 77595 on Fri Oct 09 16:30:00 2026
#

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=320.0, 
    height=180.0)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)

# 1. Create 3D Solid Part
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-50.0, 20.0), point2=(50.0, -20.0))
p = mdb.models['Model-1'].Part(name='Beam_Part', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=25.0)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

# Useless viewport manipulation commands (should be filtered out when filter is ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=180.5, 
    farPlane=350.2, width=140.0, height=85.0, cameraPosition=(45.0, 
    85.0, 150.0), cameraUpVector=(0.0, 1.0, 0.0), cameraTarget=(0.0, 0.0, 0.0))
session.viewports['Viewport: 1'].view.pan(asPercentage=(0.05, -0.02))
session.viewports['Viewport: 1'].view.rotate(xAngle=15.0, yAngle=-30.0, zAngle=0.0)
session.viewports['Viewport: 1'].view.zoom(zoomFactor=1.2)

# 2. Material & Section Assignment
mdb.models['Model-1'].Material(name='Steel_Q345')
mdb.models['Model-1'].materials['Steel_Q345'].Elastic(table=((206000.0, 0.3), ))
mdb.models['Model-1'].materials['Steel_Q345'].Density(table=((7.85e-09, ), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Solid_Section', 
    material='Steel_Q345', thickness=None)

c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='Set-AllCells')
p.SectionAssignment(region=region, sectionName='Solid_Section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

# More camera movement during modeling
session.viewports['Viewport: 1'].view.rotate(xAngle=-5.0, yAngle=10.0, zAngle=2.0)
session.viewports['Viewport: 1'].view.fitView()

# 3. Create Assembly Instance
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name='Beam_Inst', part=p, dependent=ON)

# 4. Static Step
mdb.models['Model-1'].StaticStep(name='Step-Load', previous='Initial', 
    timePeriod=1.0, maxNumInc=100, initialInc=0.1, minInc=1e-05, maxInc=1.0)
